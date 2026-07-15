"""CogniTrace — Bilişsel Yük ve Erişilebilirlik Analiz Ajanı (Sprint 2).

Çalıştırma:  streamlit run app.py   (app klasörünün içinden)
Gereksinim:  .env dosyasında GEMINI_API_KEY (bkz. .env.example)
"""

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from analyzer import analiz_et
from coordinator import koordine_et
from dyslexia_sim import disleksi_metni
from personas import PERSONAS
from simulation import DONUSUM_MATRISLERI, simule_et

load_dotenv()

st.set_page_config(page_title="CogniTrace", page_icon="🧠", layout="wide")
st.title("🧠 CogniTrace")
st.caption("Bilişsel Yük ve Erişilebilirlik Analiz Ajanı — Takım 307 | YZTA Bootcamp")

# ---------- Kenar çubuğu: girdiler ----------
with st.sidebar:
    st.header("Analiz Ayarları")
    dosya = st.file_uploader("Web sitesi ekran görüntüsü", type=["png", "jpg", "jpeg"])
    secilen_personalar = st.multiselect(
        "Personalar",
        options=list(PERSONAS.keys()),
        default=list(PERSONAS.keys()),
        format_func=lambda k: f"{PERSONAS[k]['emoji']} {PERSONAS[k]['ad']}",
    )
    simulasyon_tipi = st.selectbox(
        "Renk körlüğü simülasyonu", ["(kapalı)"] + list(DONUSUM_MATRISLERI)
    )
    html_kodu = st.text_area("HTML/CSS kodu (opsiyonel)", height=120)
    baslat = st.button("🔍 Analiz Et", type="primary", use_container_width=True)

if dosya is None:
    st.info("👈 Başlamak için soldan bir ekran görüntüsü yükleyin.")
    # Görüntü olmasa da disleksi metin simülasyonu denenebilsin.
    with st.expander("📖 Disleksi Metin Simülasyonu — okumak nasıl hissettiriyor?"):
        metin = st.text_area("Bir paragraf yapıştırın", height=100, key="dys_bos")
        if metin:
            st.write(disleksi_metni(metin))
            st.caption(
                "Basitleştirilmiş bir empati aracıdır; disleksi deneyimi kişiden kişiye değişir."
            )
    st.stop()

goruntu = Image.open(dosya)

# ---------- Görüntü + simülasyon yan yana ----------
sol, sag = st.columns(2)
sol.subheader("Orijinal")
sol.image(goruntu, use_container_width=True)
if simulasyon_tipi != "(kapalı)":
    sag.subheader(f"Simülasyon: {simulasyon_tipi}")
    sag.image(simule_et(goruntu, simulasyon_tipi), use_container_width=True)

with st.expander("📖 Disleksi Metin Simülasyonu — okumak nasıl hissettiriyor?"):
    metin = st.text_area("Sayfadaki bir paragrafı buraya yapıştırın", height=100, key="dys")
    if metin:
        st.write(disleksi_metni(metin))
        st.caption(
            "Basitleştirilmiş bir empati aracıdır; disleksi deneyimi kişiden kişiye değişir."
        )

# ---------- Persona analizleri ----------
if baslat:
    if not secilen_personalar:
        st.warning("En az bir persona seçin.")
        st.stop()

    goruntu_bytes = dosya.getvalue()
    mime = dosya.type or "image/png"
    sonuclar: dict[str, dict] = {}

    for anahtar in secilen_personalar:
        p = PERSONAS[anahtar]
        with st.spinner(f"{p['ad']} personası analiz ediyor..."):
            try:
                sonuclar[anahtar] = analiz_et(goruntu_bytes, mime, anahtar, html_kodu or None)
            except Exception as hata:
                st.error(f"{p['ad']} analizi başarısız: {hata}")
                continue

        sonuc = sonuclar[anahtar]
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

    # ---------- Persona karşılaştırması (3.3) ----------
    if sonuclar:
        st.divider()
        st.subheader("📊 Persona Karşılaştırması")
        kolonlar = st.columns(len(sonuclar))
        for kolon, (anahtar, sonuc) in zip(kolonlar, sonuclar.items(), strict=True):
            kolon.metric(
                f"{PERSONAS[anahtar]['emoji']} {PERSONAS[anahtar]['ad']}",
                f"{int(sonuc.get('bilissel_yuk_skoru', 0))}/100",
            )

        # ---------- Koordinatör Ajan (3.5) ----------
        st.subheader("🧭 Koordinatör Ajan Raporu")
        with st.spinner("Koordinatör ajan persona bulgularını sentezliyor..."):
            rapor = koordine_et(sonuclar)

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
                etkilenen = ", ".join(eylem.get("etkilenen_personalar", []))
                satir = f"{i}. {rozet} {eylem.get('sorun', '')}"
                if eylem.get("oneri"):
                    satir += f" → **{eylem['oneri']}**"
                if etkilenen:
                    satir += f" *({etkilenen})*"
                st.markdown(satir)

        if rapor.get("celiskiler"):
            with st.expander("⚖️ Personalar arası çelişkiler"):
                for celiski in rapor["celiskiler"]:
                    st.markdown(f"- {celiski}")
