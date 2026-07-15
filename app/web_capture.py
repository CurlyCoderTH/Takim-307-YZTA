"""URL'den otomatik sayfa yakalama (backlog 2.3) + axe-core kural taraması (2.4).

Tek tarayıcı oturumunda üç iş: tam sayfa ekran görüntüsü, HTML kaynağı
(3.4 kod analizine otomatik girdi olur) ve axe-core WCAG ihlal taraması.
axe-core, LLM bulgularının kural tabanlı çapraz doğrulamasıdır —
"halüsinasyon mu?" sorusunun cevabı bu katman.
"""

import os
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

# axe-core tek dosyalık motor; ilk kullanımda indirilip vendor/ altına önbelleklenir.
AXE_URL = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.2/axe.min.js"
AXE_YOL = Path(__file__).parent / "vendor" / "axe.min.js"


def _axe_kaynagi() -> str:
    if not AXE_YOL.exists():
        AXE_YOL.parent.mkdir(exist_ok=True)
        urllib.request.urlretrieve(AXE_URL, AXE_YOL)
    return AXE_YOL.read_text(encoding="utf-8")


def _ihlalleri_ozetle(ham: dict) -> list[dict]:
    """axe'ın ayrıntılı çıktısını arayüzde gösterilecek sade listeye indirger."""
    ozet = []
    for ihlal in ham.get("violations", []):
        ozet.append({
            "kural": ihlal.get("id", "?"),
            "etki": ihlal.get("impact") or "bilinmiyor",
            "aciklama": ihlal.get("help", ""),
            "eleman_sayisi": len(ihlal.get("nodes", [])),
            "ornek_hedef": (ihlal["nodes"][0]["target"][0]
                            if ihlal.get("nodes") else ""),
        })
    # Kritik olanlar üste: critical > serious > moderate > minor
    sira = {"critical": 0, "serious": 1, "moderate": 2, "minor": 3}
    ozet.sort(key=lambda i: sira.get(i["etki"], 9))
    return ozet


def sayfa_yakala(
    url: str,
    tam_sayfa: bool = True,
    axe_calistir: bool = True,
    zaman_asimi: int = 30000,
) -> dict:
    """URL'yi ziyaret eder; ekran görüntüsü + HTML + (ops.) axe ihlalleri döner.

    Dönen sözlük: {"png": bytes, "html": str, "axe": list | None}
    axe taraması başarısız olursa uygulama durmaz; "axe" None döner.
    """
    if not url.startswith(("http://", "https://", "file://")):
        url = "https://" + url

    with sync_playwright() as p:
        # Normalde playwright'ın kendi kurduğu Chromium kullanılır
        # (playwright install chromium). CI/sandbox ortamlarında hazır bir
        # binary varsa CHROMIUM_PATH ile gösterilebilir.
        tarayici = p.chromium.launch(executable_path=os.getenv("CHROMIUM_PATH") or None)
        sayfa = tarayici.new_page(viewport={"width": 1366, "height": 768})
        sayfa.goto(url, wait_until="domcontentloaded", timeout=zaman_asimi)
        # Geç yüklenen görseller/fontlar için kısa tampon bekleme.
        sayfa.wait_for_timeout(2500)

        png = sayfa.screenshot(full_page=tam_sayfa)
        html = sayfa.content()

        ihlaller = None
        if axe_calistir:
            try:
                sayfa.add_script_tag(content=_axe_kaynagi())
                ham = sayfa.evaluate(
                    "async () => await axe.run(document, {resultTypes: ['violations']})"
                )
                ihlaller = _ihlalleri_ozetle(ham)
            except Exception:
                ihlaller = None  # tarama düşerse görüntü+HTML yine de kullanılır

        tarayici.close()

    return {"png": png, "html": html, "axe": ihlaller}
