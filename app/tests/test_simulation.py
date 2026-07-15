"""Renk körlüğü simülasyonu birim testleri."""

import numpy as np
from PIL import Image

from simulation import DONUSUM_MATRISLERI, simule_et


def test_tum_tipler_gecerli_goruntu_uretir():
    img = Image.new("RGB", (20, 10), (200, 30, 90))
    for tip in DONUSUM_MATRISLERI:
        cikti = simule_et(img, tip)
        assert cikti.size == img.size
        assert cikti.mode == "RGB"


def test_akromatopsi_gri_uretir():
    # Tam renk körlüğünde R=G=B olmalı (renksiz görüntü).
    img = Image.new("RGB", (8, 8), (255, 0, 0))
    cikti = np.asarray(simule_et(img, "akromatopsi"))
    assert (cikti[..., 0] == cikti[..., 1]).all()
    assert (cikti[..., 1] == cikti[..., 2]).all()


def test_deuteranopia_kirmiziyi_donusturur():
    # Kırmızı-yeşil körlüğünde saf kırmızı, kırmızı kalamaz.
    img = Image.new("RGB", (4, 4), (255, 0, 0))
    r, g, b = np.asarray(simule_et(img, "deuteranopia"))[0, 0]
    assert g > 0  # yeşil kanala karışma olmalı


def test_bilinmeyen_tip_hata_verir():
    import pytest

    with pytest.raises(ValueError):
        simule_et(Image.new("RGB", (2, 2)), "yok-boyle-tip")
