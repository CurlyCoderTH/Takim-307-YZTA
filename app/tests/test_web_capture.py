"""URL yakalama uçtan uca testi (yerel dosya üzerinde, ağsız).

Chromium kurulu değilse test atlanır (takım arkadaşları önce
`playwright install chromium` çalıştırmalı).
"""

import pytest

from web_capture import sayfa_yakala


def test_yerel_sayfa_yakalama(tmp_path):
    sayfa = tmp_path / "test.html"
    sayfa.write_text(
        "<html><head><title>CogniTraceTest</title></head>"
        "<body><h1>Merhaba CogniTrace</h1></body></html>",
        encoding="utf-8",
    )
    try:
        sonuc = sayfa_yakala(
            sayfa.as_uri(), tam_sayfa=False, axe_calistir=False, zaman_asimi=15000
        )
    except Exception as hata:  # tarayıcı binary'si yoksa test ortamını suçlama
        pytest.skip(f"Chromium başlatılamadı: {hata}")

    assert sonuc["png"][:8] == b"\x89PNG\r\n\x1a\n"  # geçerli PNG imzası
    assert "Merhaba CogniTrace" in sonuc["html"]
    assert sonuc["axe"] is None  # axe kapalıyken None dönmeli
