"""Geri bildirim formu veri katmanı (backlog: 'Geri bildirim formu').

Kullanıcı geri bildirimlerini yerel JSON dosyasında biriktirir; harici
servis/veritabanı bağımlılığı yoktur.
"""

import json
from datetime import datetime
from pathlib import Path

BILDIRIM_YOLU = Path(__file__).parent / "geri_bildirimler.json"


def kaydet(ad: str, puan: int, mesaj: str) -> None:
    """Geri bildirimi zaman damgasıyla dosyaya ekler."""
    kayitlar = listele()
    kayitlar.append({
        "tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ad": ad.strip() or "Anonim",
        "puan": int(puan),
        "mesaj": mesaj.strip(),
    })
    BILDIRIM_YOLU.write_text(
        json.dumps(kayitlar, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def listele() -> list[dict]:
    """Kayıtlı geri bildirimleri döner (dosya yoksa boş liste)."""
    if not BILDIRIM_YOLU.exists():
        return []
    try:
        return json.loads(BILDIRIM_YOLU.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
