"""Koordinatör Ajan (backlog 3.5 — AI Agent orkestrasyonu).

Persona ajanlarının JSON çıktılarını alır ve BEŞİNCİ bir Gemini çağrısıyla
sentezler: gerekçeli genel skor, ortak sorunlar, önceliklendirilmiş eylem
planı ve yönetici özeti üretir. Düz ortalama değil, muhakeme katmanıdır —
"dört uzman raporunu okuyup sentez yazan başhekim".

LLM'e ulaşılamazsa (kota/ağ) deterministik birleştirmeye düşer; uygulama
asla boş kalmaz (demo sigortası).
"""

import json

from google.genai import types

from analyzer import MODEL, _istemci
from personas import PERSONAS

SENTEZ_TALIMATI = """
Sen, farklı nöroçeşitlilik uzmanlarının raporlarını birleştiren koordinatör
erişilebilirlik uzmanısın. Aşağıda aynı web arayüzü için persona uzmanlarının
JSON raporları var. Görevin bunları SENTEZLEMEK — özetlemek değil:

- Birden fazla uzmanın işaret ettiği bölgeler en yüksek önceliği alır.
- Genel skoru düz ortalama ALMA; sorunların şiddetine ve kaç personayı
  etkilediğine göre gerekçeli belirle.
- Çelişki varsa (bir persona için iyi, diğeri için kötü olan tasarım) bunu
  açıkça belirt.

YALNIZCA şu JSON şemasında yanıt ver (Türkçe):
{
  "genel_skor": <1-100 tamsayı; 1=çok rahat, 100=aşırı yorucu>,
  "skor_gerekcesi": "<skoru neden böyle belirlediğinin 1-2 cümlelik açıklaması>",
  "yonetici_ozeti": "<arayüzün genel durumunun 2-3 cümlelik özeti>",
  "ortak_sorunlar": ["<birden fazla personayı etkileyen sorun>", "..."],
  "oncelikli_eylemler": [
    {
      "oncelik": "<yuksek|orta|dusuk>",
      "sorun": "<bölge + sorunun kısa tarifi>",
      "etkilenen_personalar": ["<persona adı>", "..."],
      "oneri": "<somut iyileştirme adımı>"
    }
  ],
  "celiskiler": ["<personalar arası çelişen bulgu varsa, yoksa boş liste>"]
}
"""


def _deterministik_birlestir(sonuclar: dict[str, dict]) -> dict:
    """LLM'siz yedek birleştirme: ortalama skor + yüksek önemli sorunların listesi."""
    skorlar = [int(s.get("bilissel_yuk_skoru", 0)) for s in sonuclar.values()]
    eylemler = []
    for anahtar, sonuc in sonuclar.items():
        for alan in sonuc.get("sorunlu_alanlar", []):
            if alan.get("onem") == "yuksek":
                eylemler.append({
                    "oncelik": "yuksek",
                    "sorun": f"{alan.get('bolge', '?')}: {alan.get('sorun', '')}",
                    "etkilenen_personalar": [PERSONAS[anahtar]["ad"]],
                    "oneri": "",
                })
    return {
        "genel_skor": round(sum(skorlar) / len(skorlar)) if skorlar else 0,
        "skor_gerekcesi": "Persona skorlarının aritmetik ortalaması (yedek mod).",
        "yonetici_ozeti": "Koordinatör LLM'e ulaşılamadığı için bulgular kural "
                          "tabanlı birleştirildi; persona raporları yukarıda eksiksizdir.",
        "ortak_sorunlar": [],
        "oncelikli_eylemler": eylemler[:5],
        "celiskiler": [],
        "_yedek_mod": True,
    }


def koordine_et(sonuclar: dict[str, dict]) -> dict:
    """Persona sonuçlarını koordinatör ajanla sentezler; hata halinde yedek moda düşer."""
    if not sonuclar:
        raise ValueError("Sentezlenecek persona sonucu yok.")

    # Tek persona seçiliyse sentezlenecek çokluk yok; skoru doğrudan aktar.
    if len(sonuclar) == 1:
        tek = next(iter(sonuclar.values()))
        return {
            "genel_skor": int(tek.get("bilissel_yuk_skoru", 0)),
            "skor_gerekcesi": "Tek persona analiz edildi; skor doğrudan o personaya aittir.",
            "yonetici_ozeti": tek.get("genel_degerlendirme", ""),
            "ortak_sorunlar": [],
            "oncelikli_eylemler": [
                {
                    "oncelik": a.get("onem", "orta"),
                    "sorun": f"{a.get('bolge', '?')}: {a.get('sorun', '')}",
                    "etkilenen_personalar": [PERSONAS[k]["ad"] for k in sonuclar],
                    "oneri": "",
                }
                for a in tek.get("sorunlu_alanlar", [])
            ],
            "celiskiler": [],
            "_yedek_mod": False,
        }

    # Persona raporlarını okunur adlarla paketleyip sentez çağrısına gönder.
    rapor_paketi = json.dumps(
        {PERSONAS[k]["ad"]: v for k, v in sonuclar.items()}, ensure_ascii=False
    )
    try:
        istemci = _istemci()
        yanit = istemci.models.generate_content(
            model=MODEL,
            contents=[SENTEZ_TALIMATI + "\n\nPersona raporları:\n" + rapor_paketi],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        rapor = json.loads(yanit.text)
        rapor["_yedek_mod"] = False
        return rapor
    except Exception:
        return _deterministik_birlestir(sonuclar)
