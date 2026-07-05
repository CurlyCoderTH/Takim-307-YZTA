"""CogniTrace — Bilişsel Yük ve Erişilebilirlik Analiz Ajanı (Sprint 1 prototipi).

Çalıştırma:  streamlit run app.py
Gereksinim:  .env dosyasında GEMINI_API_KEY (bkz. .env.example)
"""

import io

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

from analyzer import analiz_et
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
        default=["disleksi"],
        format_func=lambda k: f"{PERSONAS[k]['emoji']} {PERSONAS[k]['ad']}",
    )
    simulasyon_tipi = st.selectbox(
        "Renk körlüğü simülasyonu", ["(kapalı)"] + list(DONUSUM_MATRISLERI)
    )
    html_kodu = st.text_area("HTML/CSS kodu (opsiyonel)", height=120)
    baslat = st.button("🔍 Analiz Et", type="primary", use_container_width=True)

if dosya is None:
    st.info("👈 Başlamak için soldan bir ekran görüntüsü yükleyin.")
    st.stop()

goruntu = Image.open(dosya)

# ---------- Görüntü + simülasyon yan yana ----------
sol, sag = st.columns(2)
sol.subheader("Orijinal")
sol.image(goruntu, use_container_width=True)
if simulasyon_tipi != "(kapalı)":
    sag.subheader(f"Simülasyon: {simulasyon_tipi}")
    sag.image(simule_et(goruntu, simulasyon_tipi), use_container_width=True)

# ---------- Persona analizleri ----------
if baslat:
    if not secilen_personalar:
        st.warning("En az bir persona seçin.")
        st.stop()

    goruntu_bytes = dosya.getvalue()
    mime = dosya.type or "image/png"
    skorlar: list[int] = []

    for anahtar in secilen_personalar:
        p = PERSONAS[anahtar]
        with st.spinner(f"{p['ad']} personası analiz ediyor..."):
            try:
                sonuc = analiz_et(goruntu_bytes, mime, anahtar, html_kodu or None)
            except Exception as hata:
                st.error(f"{p['ad']} analizi başarısız: {hata}")
                continue

        skor = int(sonuc.get("bilissel_yuk_skoru", 0))
        skorlar.append(skor)

        st.divider()
        st.subheader(f"{p['emoji']} {p['ad']}")
        c1, c2 = st.columns([1, 3])
        c1.metric("Bilişsel Yük", f"{skor}/100")
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

    # Genel skor: persona skorlarının ortalaması (Sprint 2'de koordinatör ajana devredilecek).
    if skorlar:
        st.divider()
        genel = round(sum(skorlar) / len(skorlar))
        st.metric("🎯 Genel Bilişsel Yük Skoru", f"{genel}/100")
        st.progress(genel / 100)
