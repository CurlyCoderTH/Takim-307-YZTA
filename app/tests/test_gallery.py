"""Örnek galerisi birim testleri."""

import gallery


def test_kaydet_yukle_dongusu(tmp_path, monkeypatch):
    monkeypatch.setattr(gallery, "GALERI_YOL", tmp_path)
    sonuclar = {"disleksi": {"bilissel_yuk_skoru": 42, "sorunlu_alanlar": []}}
    rapor = {"genel_skor": 42, "yonetici_ozeti": "test"}

    ad = gallery.kaydet("Örnek Haber Sitesi!", b"PNGBAYTLARI", sonuclar, rapor)
    assert ad in gallery.listele()

    g_bytes, g_sonuclar, g_rapor = gallery.yukle(ad)
    assert g_bytes == b"PNGBAYTLARI"
    assert g_sonuclar["disleksi"]["bilissel_yuk_skoru"] == 42
    assert g_rapor["genel_skor"] == 42


def test_guvenli_ad_tehlikeli_karakterleri_temizler():
    assert "/" not in gallery._guvenli_ad("../kötü/../yol")
    assert "." not in gallery._guvenli_ad("../kötü/../yol")
    assert gallery._guvenli_ad("Örnek Site 1") != ""


def test_bos_galeri_bos_liste(tmp_path, monkeypatch):
    monkeypatch.setattr(gallery, "GALERI_YOL", tmp_path / "yok")
    assert gallery.listele() == []
