"""Disleksi metin simülasyonu birim testleri."""

from dyslexia_sim import disleksi_metni


def test_ilk_ve_son_harf_korunur():
    cikti = disleksi_metni("merhaba dunyali arkadaslar", oran=1.0, tohum=42)
    kelimeler = "merhaba dunyali arkadaslar".split()
    for orijinal, bozuk in zip(kelimeler, cikti.split(), strict=True):
        assert bozuk[0] == orijinal[0]
        assert bozuk[-1] == orijinal[-1]
        assert sorted(bozuk) == sorted(orijinal)  # harfler kaybolmaz


def test_kisa_kelimeler_dokunulmaz():
    assert disleksi_metni("ev su o kedi", oran=1.0, tohum=1).split()[:3] == ["ev", "su", "o"]


def test_ayni_tohum_ayni_sonuc():
    a = disleksi_metni("tekrarlanabilir sonuclar onemlidir", tohum=7)
    b = disleksi_metni("tekrarlanabilir sonuclar onemlidir", tohum=7)
    assert a == b


def test_sifir_oran_metni_degistirmez():
    metin = "hicbir kelime degismemeli burada"
    assert disleksi_metni(metin, oran=0.0) == metin
