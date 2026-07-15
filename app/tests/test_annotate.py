"""Görsel işaretleme birim testleri (çizim katmanı, API'siz)."""

import numpy as np
from PIL import Image

from annotate import _kutulari_ciz


def test_kutu_cizimi_goruntuyu_bozmaz():
    img = Image.new("RGB", (200, 100), (255, 255, 255))
    kutular = [{"etiket": "1", "box_2d": [100, 100, 500, 500]}]
    cikti = _kutulari_ciz(img, kutular)
    assert cikti.size == img.size
    # Çerçeve çizildi mi: görüntüde kırmızı pikseller olmalı.
    dizi = np.asarray(cikti)
    kirmizi = (dizi[..., 0] > 200) & (dizi[..., 1] < 80) & (dizi[..., 2] < 80)
    assert kirmizi.any()


def test_gecersiz_kutular_atlanir():
    img = Image.new("RGB", (100, 100), (0, 0, 0))
    kutular = [
        {"etiket": "1"},                                # box_2d yok
        {"etiket": "2", "box_2d": [500, 500, 100, 100]},  # ters koordinat
        {"etiket": "3", "box_2d": "bozuk"},             # yanlış tip
    ]
    cikti = _kutulari_ciz(img, kutular)  # hata fırlatmamalı
    assert cikti.size == img.size


def test_bos_liste_kopya_dondurur():
    img = Image.new("RGB", (50, 50), (10, 20, 30))
    cikti = _kutulari_ciz(img, [])
    assert np.asarray(cikti).tolist() == np.asarray(img.convert("RGB")).tolist()
