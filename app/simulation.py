"""Renk körlüğü simülasyonu.

Ekran görüntüsünü, renk körü bir bireyin gördüğü haliyle yeniden üretir.
Literatürde yaygın kullanılan doğrusal RGB dönüşüm matrisleri kullanılır
(deterministik katman — LLM'e girmeden önce çalışır, ücretsizdir).
"""

import numpy as np
from PIL import Image

# Her renk körlüğü tipi için yaklaşık RGB dönüşüm matrisi.
DONUSUM_MATRISLERI: dict[str, list[list[float]]] = {
    # Yeşil körlüğü — erkeklerde en yaygın tip
    "deuteranopia": [
        [0.625, 0.375, 0.0],
        [0.700, 0.300, 0.0],
        [0.000, 0.300, 0.7],
    ],
    # Kırmızı körlüğü
    "protanopia": [
        [0.567, 0.433, 0.000],
        [0.558, 0.442, 0.000],
        [0.000, 0.242, 0.758],
    ],
    # Mavi körlüğü — nadir
    "tritanopia": [
        [0.950, 0.050, 0.000],
        [0.000, 0.433, 0.567],
        [0.000, 0.475, 0.525],
    ],
    # Tam renk körlüğü (monokromasi) — parlaklık algısı korunur, renk tamamen gider
    "akromatopsi": [
        [0.299, 0.587, 0.114],
        [0.299, 0.587, 0.114],
        [0.299, 0.587, 0.114],
    ],
}


def simule_et(goruntu: Image.Image, tip: str = "deuteranopia") -> Image.Image:
    """Görüntüyü verilen renk körlüğü tipine göre dönüştürür."""
    if tip not in DONUSUM_MATRISLERI:
        raise ValueError(f"Bilinmeyen tip: {tip}. Seçenekler: {list(DONUSUM_MATRISLERI)}")
    # RGB'ye çevir, 0-1 aralığına normalle, matrisle çarp, geri ölçekle.
    dizi = np.asarray(goruntu.convert("RGB"), dtype=np.float64) / 255.0
    matris = np.array(DONUSUM_MATRISLERI[tip])
    donusmus = dizi @ matris.T
    return Image.fromarray((np.clip(donusmus, 0.0, 1.0) * 255).astype(np.uint8))
