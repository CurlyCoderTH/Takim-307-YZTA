"""Önbellekli örnek galerisi (backlog: 'Create cached sample gallery').

Tamamlanmış analizleri diske kaydeder; uygulama API'siz de (kota bitti,
internet yok, demo günü aksilikleri) kayıtlı örnekleri gösterebilir.
Her örnek bir klasördür: galeri/<ad>/goruntu.png + sonuc.json
"""

import json
import re
from pathlib import Path

GALERI_YOL = Path(__file__).parent / "galeri"


def _guvenli_ad(ad: str) -> str:
    """Klasör adı için sadeleştirme: boşluk → tire, tehlikeli karakterler dışarı."""
    ad = ad.strip().lower().replace(" ", "-")
    return re.sub(r"[^a-z0-9çğıöşü\-]", "", ad)[:50] or "ornek"


def kaydet(ad: str, goruntu_bytes: bytes, sonuclar: dict, rapor: dict | None) -> str:
    """Analizi galeriye yazar; kullanılan klasör adını döner."""
    klasor = GALERI_YOL / _guvenli_ad(ad)
    klasor.mkdir(parents=True, exist_ok=True)
    (klasor / "goruntu.png").write_bytes(goruntu_bytes)
    (klasor / "sonuc.json").write_text(
        json.dumps({"sonuclar": sonuclar, "rapor": rapor}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return klasor.name


def listele() -> list[str]:
    """Kayıtlı örnek adlarını döner (galeri boşsa boş liste)."""
    if not GALERI_YOL.exists():
        return []
    return sorted(k.name for k in GALERI_YOL.iterdir() if (k / "sonuc.json").exists())


def yukle(ad: str) -> tuple[bytes, dict, dict | None]:
    """Kayıtlı örneği okur: (görüntü bayları, persona sonuçları, koordinatör raporu)."""
    klasor = GALERI_YOL / ad
    veri = json.loads((klasor / "sonuc.json").read_text(encoding="utf-8"))
    return (klasor / "goruntu.png").read_bytes(), veri["sonuclar"], veri.get("rapor")
