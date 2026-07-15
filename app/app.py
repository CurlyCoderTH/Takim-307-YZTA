"""CogniTrace — Bilişsel Yük ve Erişilebilirlik Analiz Ajanı (Sprint 2).

Çalıştırma:  streamlit run app.py   (app klasörünün içinden)
Gereksinim:  .env dosyasında GEMINI_API_KEY (bkz. .env.example)
             URL yakalama için bir kez: playwright install chromium
"""

import io

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

import gallery
from analyzer import analiz_et
from annotate import bolgeleri_isaretle
from coordinator import koordine_et
from dyslexia_sim import disleksi_metni
from personas import PERSONAS
from simulation import DONUSUM_MATRISLERI, simule_et

load_dotenv()

st.set_page_config(page_title="CogniTrace", page_icon="🧠", layout="wide")
st.title("🧠 CogniTrace")
st.caption("Bilişsel Yük ve Erişilebilirlik Analiz Ajanı — Takım 307 | YZTA Bootcamp")

durum = st.session_state  # kısaltma: yeniden çalıştırmalar arası hafıza


# ---------- Sonuç görünümleri (canlı analiz ve galeri aynı fonksiyonları kullanır) ----------
def persona_bolumu(anahtar: str, sonuc: dict) -> None:
    p = PERSONAS[anahtar]
    st.divider()
    st.subheader(f"{p['emoji']} {p['ad']}")
    c1, c2 = st.columns([1, 3])
    c1.metric("Bilişsel Yük", f"{int(sonuc.get('bilissel_yuk_skoru', 0))}/100")
    c2.write(sonuc.get("genel_degerlendirme", ""))
    if sonuc.get("sorunlu_alanlar"):
        st.markdown("**⚠️ Sorunlu Alanlar**")
        for alan in sonuc["sorunlu_alanlar"]:
            onem = {"yuksek": "🔴", "orta": "🟡", "dusuk": "🟢"}.get(alan.get("onem", ""), "⚪")
            st.markdown(f"- {onem} **{alan.get('bolge', '?')}** — {alan.get('sorun', '')}")
    if sonuc.get("oneriler"):
        st.markdown("**💡 Öneriler**")
        for oneri in sonuc["oneriler"]:
            st.markdown(f"- {oneri}")
    if sonuc.get("pozitif_yonler"):
        with st.expander("✅ Pozitif yönler"):
            for poz in sonuc["pozitif_yonler"]:
                st.markdown(f"- {poz}")


def koordinator_bolumu(rapor: dict) -> None:
    st.subheader("🧭 Koordinatör Ajan Raporu")
    if rapor.get("_yedek_mod"):
        st.info("Koordinatör LLM'e ulaşılamadı; deterministik birleştirme kullanıldı.")
    k1, k2 = st.columns([1, 3])
    genel = int(rapor.get("genel_skor", 0))
    k1.metric("🎯 Genel Bilişsel Yük", f"{genel}/100")
    k1.progress(min(max(genel, 0), 100) / 100)
    k2.write(rapor.get("yonetici_ozeti", ""))
    if rapor.get("skor_gerekcesi"):
        k2.caption(f"Skor gerekçesi: {rapor['skor_gerekcesi']}")
    if rapor.get("ortak_sorunlar"):
        st.markdown("**🔁 Birden Fazla Personayı Etkileyen Sorunlar**")
        for ortak in rapor["ortak_sorunlar"]:
            st.markdown(f"- {ortak}")
    if rapor.get("oncelikli_eylemler"):
        st.markdown("**🛠️ Öncelikli Eylem Planı**")
        for i, eylem in enumerate(rapor["oncelikli_eylemler"], 1):
            rozet = {"yuksek": "🔴", "orta": "🟡", "dusuk": "🟢"}.get(
                eylem.get("oncelik", ""), "⚪"
            )
            satir = f"{i}. {rozet} {eylem.get('sorun', '')}"
            if eylem.get("oneri"):
                satir += f" → **{eylem['oneri']}**"
            if eylem.get("etkilenen_personalar"):
                satir += f" *({', '.join(eylem['etkilenen_personalar'])})*"
            st.markdown(satir)
    if rapor.get("celiskiler"):
        with st.expander("⚖️ Personalar arası çelişkiler"):
            for celiski in rapor["celiskiler"]:
                st.markdown(f"- {celiski}")


def karsilastirma_bolumu(sonuclar: dict) -> None:
    st.divider()
    st.subheader("📊 Persona Karşılaştırması")
    kolonlar = st.columns(len(sonuclar))
    for kolon, (anahtar, sonuc) in zip(kolonlar, sonuclar.items(), strict=True):
        kolon.metric(
            f"{PERSONAS[anahtar]['emoji']} {PERSONAS[anahtar]['ad']}",
            f"{int(sonuc.get('bilissel_yuk_skoru', 0))}/100",
        )


def axe_bolumu(ihlaller: list) -> None:
    etki_rozet = {"critical": "🔴", "serious": "🟠", "moderate": "🟡", "minor": "🟢"}
    baslik = f"🧪 axe-core kural taraması — {len(ihlaller)} WCAG ihlali (çapraz doğrulama)"
    with st.expander(baslik):
        st.caption(
            "Kural tabanlı bağımsız denetim: LLM bulgularıyla örtüşen maddeler "
            "çapraz doğrulanmış demektir."
        )
        for ihlal in ihlaller:
            rozet = etki_rozet.get(ihlal["etki"], "⚪")
            st.markdown(
                f"- {rozet} **{ihlal['kural']}** ({ihlal['etki']}): {ihlal['aciklama']} "
                f"— {ihlal['eleman_sayisi']} eleman, örn. `{ihlal['ornek_hedef']}`"
            )


# ---------- Kenar çubuğu: girdi kaynağı ve ayarlar ----------
with st.sidebar:
    # Tema anahtarı: Streamlit'in resmî çalışma anı tema API'si olmadığı için
    # dahili config kancası kullanılır (st._config). Sürüm güncellemesinde
    # kırılırsa uygulama düşmez; sadece anahtar etkisiz kalır ve tema
    # .streamlit/config.toml'daki varsayılanda (koyu) sabitlenir.
    st.session_state.setdefault("koyu_tema", True)
    koyu_secim = st.toggle("🌙 Koyu tema", value=st.session_state["koyu_tema"])
    if koyu_secim != st.session_state["koyu_tema"]:
        st.session_state["koyu_tema"] = koyu_secim
        try:
            st._config.set_option("theme.base", "dark" if koyu_secim else "light")
        except Exception:
            pass
        st.rerun()
    try:
        st._config.set_option(
            "theme.base", "dark" if st.session_state["koyu_tema"] else "light"
        )
    except Exception:
        pass

    st.header("Analiz Ayarları")
    kaynak = st.radio("Girdi kaynağı", ["📸 Görüntü yükle", "🌐 URL'den yakala", "📁 Örnek galeri"])

    if kaynak == "📸 Görüntü yükle":
        dosya = st.file_uploader("Web sitesi ekran görüntüsü", type=["png", "jpg", "jpeg"])
        if dosya is not None:
            durum["goruntu"] = dosya.getvalue()
            durum["mime"] = dosya.type or "image/png"
            durum["html"] = None
            durum["axe"] = None
            durum.pop("hazir", None)

    elif kaynak == "🌐 URL'den yakala":
        url = st.text_input("Site adresi", placeholder="ornek.gov.tr")
        tam_sayfa = st.checkbox("Tam sayfa (uzun görüntü)", value=False)
        if st.button("📥 Sayfayı Yakala", use_container_width=True) and url:
            try:
                from web_capture import sayfa_yakala

                with st.spinner("Sayfa ziyaret ediliyor, görüntü ve HTML alınıyor..."):
                    yakalanan = sayfa_yakala(url, tam_sayfa=tam_sayfa)
                durum["goruntu"] = yakalanan["png"]
                durum["mime"] = "image/png"
                durum["html"] = yakalanan["html"]
                durum["axe"] = yakalanan["axe"]
                durum.pop("hazir", None)
                st.success("Yakalandı ✓ (HTML kod analizi otomatik dahil edilecek)")
            except Exception as hata:
                st.error(f"Yakalama başarısız: {hata}")

    else:  # Örnek galeri — API'siz demo modu
        ornekler = gallery.listele()
        if not ornekler:
            st.info("Galeri boş. Bir analiz yapıp '💾 Galeriye kaydet' ile örnek ekleyin.")
        else:
            secilen_ornek = st.selectbox("Kayıtlı örnek", ornekler)
            if st.button("📂 Örneği Aç", use_container_width=True):
                g_bytes, g_sonuclar, g_rapor = gallery.yukle(secilen_ornek)
                durum["goruntu"] = g_bytes
                durum["mime"] = "image/png"
                durum["html"] = None
                durum["axe"] = None
                durum["hazir"] = (g_sonuclar, g_rapor)

    secilen_personalar = st.multiselect(
        "Personalar",
        options=list(PERSONAS.keys()),
        default=list(PERSONAS.keys()),
        format_func=lambda k: f"{PERSONAS[k]['emoji']} {PERSONAS[k]['ad']}",
    )
    simulasyon_tipi = st.selectbox(
        "Renk körlüğü simülasyonu", ["(kapalı)"] + list(DONUSUM_MATRISLERI)
    )
    elle_html = st.text_area("HTML/CSS kodu (opsiyonel)", height=100)
    baslat = st.button("🔍 Analiz Et", type="primary", use_container_width=True)


# ---------- Ana alan ----------
if "goruntu" not in durum:
    st.info("👈 Görüntü yükleyin, URL yakalayın veya galeriden örnek açın.")
    with st.expander("📖 Disleksi Metin Simülasyonu — okumak nasıl hissettiriyor?"):
        metin = st.text_area("Bir paragraf yapıştırın", height=100, key="dys_bos")
        if metin:
            st.write(disleksi_metni(metin))
            st.caption(
                "Basitleştirilmiş bir empati aracıdır; disleksi deneyimi kişiden kişiye değişir."
            )
    st.stop()

goruntu = Image.open(io.BytesIO(durum["goruntu"]))
sol, sag = st.columns(2)
sol.subheader("Orijinal")
sol.image(goruntu, use_container_width=True)
if simulasyon_tipi != "(kapalı)":
    sag.subheader(f"Simülasyon: {simulasyon_tipi}")
    sag.image(simule_et(goruntu, simulasyon_tipi), use_container_width=True)

if durum.get("axe"):
    axe_bolumu(durum["axe"])

with st.expander("📖 Disleksi Metin Simülasyonu — okumak nasıl hissettiriyor?"):
    metin = st.text_area("Sayfadaki bir paragrafı buraya yapıştırın", height=100, key="dys")
    if metin:
        st.write(disleksi_metni(metin))
        st.caption(
            "Basitleştirilmiş bir empati aracıdır; disleksi deneyimi kişiden kişiye değişir."
        )

# ---------- Galeriden açılan hazır sonuç (API'siz gösterim) ----------
if "hazir" in durum and not baslat:
    st.info("📁 Galeriden kayıtlı analiz gösteriliyor (API çağrısı yapılmadı).")
    hazir_sonuclar, hazir_rapor = durum["hazir"]
    for anahtar, sonuc in hazir_sonuclar.items():
        if anahtar in PERSONAS:
            persona_bolumu(anahtar, sonuc)
    if hazir_sonuclar:
        karsilastirma_bolumu(hazir_sonuclar)
    if hazir_rapor:
        st.divider()
        koordinator_bolumu(hazir_rapor)

# ---------- Canlı analiz ----------
if baslat:
    if not secilen_personalar:
        st.warning("En az bir persona seçin.")
        st.stop()

    # URL'den yakalanan HTML otomatik; elle yapıştırılan varsa o öncelikli.
    html_kodu = elle_html.strip() or durum.get("html")
    sonuclar: dict[str, dict] = {}

    for anahtar in secilen_personalar:
        p = PERSONAS[anahtar]
        with st.spinner(f"{p['ad']} personası analiz ediyor..."):
            try:
                sonuclar[anahtar] = analiz_et(
                    durum["goruntu"], durum["mime"], anahtar, html_kodu
                )
            except Exception as hata:
                st.error(f"{p['ad']} analizi başarısız: {hata}")
                continue
        persona_bolumu(anahtar, sonuclar[anahtar])

    if sonuclar:
        karsilastirma_bolumu(sonuclar)

        with st.spinner("Koordinatör ajan persona bulgularını sentezliyor..."):
            rapor = koordine_et(sonuclar)
        koordinator_bolumu(rapor)

        # ---------- Görsel işaretleme (4.2) ----------
        st.subheader("📍 Sorunlu Bölgeler Görüntü Üzerinde")
        tarifler = [
            f"{alan.get('bolge', '')}: {alan.get('sorun', '')}"
            for sonuc in sonuclar.values()
            for alan in sonuc.get("sorunlu_alanlar", [])
            if alan.get("onem") in ("yuksek", "orta")
        ][:6]
        with st.spinner("Bölgeler görüntü üzerinde işaretleniyor..."):
            isaretli = bolgeleri_isaretle(durum["goruntu"], durum["mime"], tarifler)
        if isaretli is not None:
            st.image(isaretli, use_container_width=True)
            st.caption("Numaralar, yukarıdaki öncelikli sorun listesindeki sırayla eşleşir.")
        else:
            st.info("Bu görüntü için bölge işaretlemesi yapılamadı.")

        durum["son_analiz"] = (sonuclar, rapor)

# ---------- Galeriye kaydet ----------
if "son_analiz" in durum:
    st.divider()
    g1, g2 = st.columns([3, 1])
    galeri_adi = g1.text_input(
        "Örnek adı (galeriye kaydetmek için)", placeholder="ornek-haber-sitesi"
    )
    if g2.button("💾 Galeriye kaydet", use_container_width=True) and galeri_adi:
        kayit_sonuclar, kayit_rapor = durum["son_analiz"]
        ad = gallery.kaydet(galeri_adi, durum["goruntu"], kayit_sonuclar, kayit_rapor)
        st.success(f"Kaydedildi: galeri/{ad} — artık API'siz de açılabilir.")
