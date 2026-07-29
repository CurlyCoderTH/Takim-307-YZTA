"""Gemini multimodal analiz katmanı.

Ekran görüntüsünü seçilen persona gözüyle analiz eder ve yapılandırılmış
JSON çıktı döndürür. JSON şeması zorunlu tutularak halüsinasyon riski
azaltılır (model serbest metin yerine şemaya uymak zorunda kalır).
"""

import json
import os

from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from personas import GENEL_TALIMAT, PERSONAS

# Varsayılan model; Streamlit session_state içinden dinamik ezilebilir.
DEFAULTS_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MODEL = DEFAULTS_MODEL


def get_model() -> str:
    """Aktif modeli döner; streamlit session_state önceliklidir."""
    try:
        import streamlit as st
        if "secilen_model" in st.session_state and st.session_state["secilen_model"]:
            return st.session_state["secilen_model"]
    except Exception:
        pass
    return DEFAULTS_MODEL


class SorunluAlan(BaseModel):
    bolge: str = Field(description="Ekrandaki konum tarifi, örn: 'sağ üst köşedeki menü'")
    sorun: str = Field(description="Sorunun açıklaması")
    onem: str = Field(description="Önem derecesi. Olası değerler: yuksek, orta, dusuk")


class PersonaAnalizCiktisi(BaseModel):
    bilissel_yuk_skoru: int = Field(ge=1, le=100, description="1-100 arası tamsayı; 1=çok rahat, 100=aşırı yorucu")
    genel_degerlendirme: str = Field(description="2-3 cümlelik özet")
    sorunlu_alanlar: list[SorunluAlan] = Field(description="En fazla 5 sorunlu alan listesi")
    oneriler: list[str] = Field(description="Somut, uygulanabilir iyileştirme önerileri listesi")
    pozitif_yonler: list[str] = Field(description="Arayüzün bu persona için iyi yaptığı şeyler listesi")


# İstemci bir kez oluşturulup saklanır; her çağrıda yeniden oluşturulursa
# Python geçici nesneyi erken temizleyip bağlantıyı kapatabiliyor
# ("Cannot send a request, as the client has been closed" hatası).
_CLIENT: genai.Client | None = None


def _istemci() -> genai.Client:
    global _CLIENT
    if _CLIENT is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY bulunamadı. .env dosyası oluşturup anahtarınızı ekleyin "
                "(https://aistudio.google.com adresinden ücretsiz alınır)."
            )
        _CLIENT = genai.Client(api_key=api_key)
    return _CLIENT


def analiz_et(
    goruntu_bytes: bytes,
    mime_type: str,
    persona_anahtari: str,
    html_kodu: str | None = None,
) -> dict:
    """Tek persona için görüntü (+ opsiyonel HTML) analizi yapar, dict döner."""
    persona = PERSONAS[persona_anahtari]

    icerik: list = [
        types.Part.from_bytes(data=goruntu_bytes, mime_type=mime_type),
        persona["prompt"] + "\n" + GENEL_TALIMAT,
    ]
    # HTML/CSS verilmişse yapısal analiz için ekle (token limiti için kırpılır).
    if html_kodu:
        icerik.append(
            "Ek olarak sayfanın kaynak kodu (yapısal sorunları da denetle):\n"
            "```html\n" + html_kodu[:20000] + "\n```"
        )

    istemci = _istemci()
    yanit = istemci.models.generate_content(
        model=get_model(),
        contents=icerik,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=PersonaAnalizCiktisi,
        ),
    )
    return json.loads(yanit.text)
