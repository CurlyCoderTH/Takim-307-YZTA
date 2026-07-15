"""Gemini multimodal analiz katmanı.

Ekran görüntüsünü seçilen persona gözüyle analiz eder ve yapılandırılmış
JSON çıktı döndürür. JSON şeması zorunlu tutularak halüsinasyon riski
azaltılır (model serbest metin yerine şemaya uymak zorunda kalır).
"""

import json
import os

from google import genai
from google.genai import types

from personas import GENEL_TALIMAT, PERSONAS

# Ücretsiz katmanda çalışan multimodal model; .env ile değiştirilebilir.
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Modelden istenen çıktı biçimi — her persona için aynı şema kullanılır ki
# koordinatör katman (Sprint 2) çıktıları kolayca birleştirebilsin.
CIKTI_SEMASI = """
Analizini YALNIZCA şu JSON şemasında döndür:
{
  "bilissel_yuk_skoru": <1-100 arası tamsayı; 1=çok rahat, 100=aşırı yorucu>,
  "genel_degerlendirme": "<2-3 cümlelik özet>",
  "sorunlu_alanlar": [
    {
      "bolge": "<ekrandaki konum tarifi, örn: 'sağ üst köşedeki menü'>",
      "sorun": "<sorunun açıklaması>",
      "onem": "<yuksek|orta|dusuk>"
    }
  ],
  "oneriler": ["<somut, uygulanabilir iyileştirme önerisi>", "..."],
  "pozitif_yonler": ["<arayüzün bu persona için iyi yaptığı şeyler>", "..."]
}
Sorunları YALNIZCA görüntüde gerçekten gördüğün kanıtlara dayandır;
görüntüde olmayan şeyler hakkında varsayım yapma. Türkçe yanıt ver.
"""


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
        persona["prompt"] + "\n" + GENEL_TALIMAT + "\n" + CIKTI_SEMASI,
    ]
    # HTML/CSS verilmişse yapısal analiz için ekle (token limiti için kırpılır).
    if html_kodu:
        icerik.append(
            "Ek olarak sayfanın kaynak kodu (yapısal sorunları da denetle):\n"
            "```html\n" + html_kodu[:20000] + "\n```"
        )

    istemci = _istemci()
    yanit = istemci.models.generate_content(
        model=MODEL,
        contents=icerik,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )
    return json.loads(yanit.text)
