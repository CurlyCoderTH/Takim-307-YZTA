"""Sorunlu bölgeleri görüntü üzerinde işaretleme (backlog 4.2).

Persona ajanlarının bulduğu sorunlu bölge tariflerini Gemini'ye geri verip
sınırlayıcı kutu (bounding box) koordinatlarını ister, PIL ile görüntüye
numaralı kırmızı çerçeveler çizer. Kutu bulunamazsa uygulama durmaz.
"""

import json

from google.genai import types
from PIL import Image, ImageDraw

from analyzer import MODEL, _istemci

KUTU_TALIMATI = """
Bu arayüz görüntüsünde aşağıda tarif edilen sorunlu bölgeleri bul.
YALNIZCA şu JSON listesiyle yanıt ver:
[{"etiket": "<bölgenin sıra numarası>", "box_2d": [ymin, xmin, ymax, xmax]}]
box_2d değerleri 0-1000 ölçeğinde normalize koordinatlardır.
Emin olamadığın bölgeyi listeye hiç ekleme; uydurma kutu üretme.
Sorunlu bölgeler:
"""


def _kutulari_ciz(goruntu: Image.Image, kutular: list[dict]) -> Image.Image:
    """0-1000 ölçekli kutuları piksele çevirip numaralı çerçeveler çizer."""
    isaretli = goruntu.convert("RGB").copy()
    cizim = ImageDraw.Draw(isaretli)
    g, y = isaretli.size
    for kutu in kutular:
        try:
            ymin, xmin, ymax, xmax = kutu["box_2d"]
        except (KeyError, ValueError, TypeError):
            continue
        # Normalize (0-1000) → piksel; taşmalara karşı kırpılır.
        x1, y1 = max(0, xmin / 1000 * g), max(0, ymin / 1000 * y)
        x2, y2 = min(g, xmax / 1000 * g), min(y, ymax / 1000 * y)
        if x2 <= x1 or y2 <= y1:
            continue
        cizim.rectangle([x1, y1, x2, y2], outline=(220, 30, 30), width=4)
        etiket = str(kutu.get("etiket", "?"))
        cizim.rectangle([x1, y1, x1 + 14 + 9 * len(etiket), y1 + 22], fill=(220, 30, 30))
        cizim.text((x1 + 6, y1 + 4), etiket, fill=(255, 255, 255))
    return isaretli


def bolgeleri_isaretle(
    goruntu_bytes: bytes, mime_type: str, bolge_tarifleri: list[str]
) -> Image.Image | None:
    """Bölge tariflerinin kutularını Gemini'den ister, işaretli görüntü döner.

    Başarısız olursa (kota, parse hatası) None döner; çağıran taraf bunu
    "işaretleme yapılamadı" bilgisiyle karşılar.
    """
    if not bolge_tarifleri:
        return None
    liste = "\n".join(f"{i}. {t}" for i, t in enumerate(bolge_tarifleri, 1))
    try:
        istemci = _istemci()
        yanit = istemci.models.generate_content(
            model=MODEL,
            contents=[
                types.Part.from_bytes(data=goruntu_bytes, mime_type=mime_type),
                KUTU_TALIMATI + liste,
            ],
            config=types.GenerateContentConfig(response_mime_type="application/json"),
        )
        kutular = json.loads(yanit.text)
        if not isinstance(kutular, list) or not kutular:
            return None
        import io

        return _kutulari_ciz(Image.open(io.BytesIO(goruntu_bytes)), kutular)
    except Exception:
        return None
