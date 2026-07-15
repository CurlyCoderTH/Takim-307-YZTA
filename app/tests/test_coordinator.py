"""Koordinatör ajan birim testleri (LLM'siz kısımlar)."""

import pytest

from coordinator import _deterministik_birlestir, koordine_et

ORNEK_SONUCLAR = {
    "disleksi": {
        "bilissel_yuk_skoru": 80,
        "genel_degerlendirme": "Metin yoğunluğu yüksek.",
        "sorunlu_alanlar": [
            {"bolge": "üst menü", "sorun": "sıkışık yazı", "onem": "yuksek"},
            {"bolge": "alt bilgi", "sorun": "küçük punto", "onem": "dusuk"},
        ],
    },
    "dehb": {
        "bilissel_yuk_skoru": 60,
        "genel_degerlendirme": "Dikkat dağıtıcı öğeler var.",
        "sorunlu_alanlar": [
            {"bolge": "yan banner", "sorun": "hareket izlenimi", "onem": "yuksek"},
        ],
    },
}


def test_yedek_birlestirme_ortalama_alir():
    rapor = _deterministik_birlestir(ORNEK_SONUCLAR)
    assert rapor["genel_skor"] == 70  # (80+60)/2
    assert rapor["_yedek_mod"] is True


def test_yedek_birlestirme_yuksek_onemlileri_toplar():
    rapor = _deterministik_birlestir(ORNEK_SONUCLAR)
    sorunlar = [e["sorun"] for e in rapor["oncelikli_eylemler"]]
    assert any("üst menü" in s for s in sorunlar)
    assert any("yan banner" in s for s in sorunlar)
    assert not any("alt bilgi" in s for s in sorunlar)  # dusuk önem elenir


def test_tek_persona_dogrudan_aktarilir():
    tek = {"disleksi": ORNEK_SONUCLAR["disleksi"]}
    rapor = koordine_et(tek)  # tek persona LLM'e gitmez
    assert rapor["genel_skor"] == 80
    assert len(rapor["oncelikli_eylemler"]) == 2


def test_bos_girdi_hata_verir():
    with pytest.raises(ValueError):
        koordine_et({})
