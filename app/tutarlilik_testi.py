"""Çıktı tutarlılık testi (backlog 3.6).

Aynı görüntüyü her persona için N kez analiz eder; skorların ortalamasını ve
sapmasını ölçer. LLM tabanlı skorlamanın "her seferinde başka şey söylüyor"
eleştirisine sayısal cevap üretir.

Kullanım (app klasörünün içinden, .env hazır olmalı):
    python tutarlilik_testi.py test-goruntuleri/ornek.png --tekrar 3
"""

import argparse
import json
import statistics
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from analyzer import analiz_et  # noqa: E402  (load_dotenv sonrasında gelmeli)
from personas import PERSONAS  # noqa: E402


def calistir(goruntu_yolu: str, tekrar: int) -> dict:
    veri = Path(goruntu_yolu).read_bytes()
    mime = "image/png" if goruntu_yolu.lower().endswith(".png") else "image/jpeg"
    sonuclar: dict[str, list[int]] = {}

    for anahtar, p in PERSONAS.items():
        skorlar = []
        for deneme in range(1, tekrar + 1):
            try:
                cikti = analiz_et(veri, mime, anahtar)
                skor = int(cikti.get("bilissel_yuk_skoru", 0))
            except Exception as hata:
                print(f"  {p['ad']} deneme {deneme}: HATA — {hata}")
                continue
            skorlar.append(skor)
            print(f"  {p['ad']} deneme {deneme}: {skor}/100")
        sonuclar[anahtar] = skorlar
    return sonuclar


def raporla(sonuclar: dict, dosya: str) -> None:
    print("\n| Persona | Denemeler | Ortalama | Std Sapma |")
    print("|---|---|---|---|")
    for anahtar, skorlar in sonuclar.items():
        if not skorlar:
            continue
        ort = statistics.mean(skorlar)
        sapma = statistics.stdev(skorlar) if len(skorlar) > 1 else 0.0
        print(f"| {PERSONAS[anahtar]['ad']} | {skorlar} | {ort:.1f} | ±{sapma:.1f} |")
    Path("tutarlilik_sonuclari.json").write_text(
        json.dumps({"goruntu": dosya, "sonuclar": sonuclar}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print("\nSonuçlar tutarlilik_sonuclari.json dosyasına yazıldı.")
    print("Bu tabloyu README'ye/rapora yapıştırabilirsiniz.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="CogniTrace skor tutarlılık testi")
    ap.add_argument("goruntu", help="Analiz edilecek ekran görüntüsü yolu")
    ap.add_argument("--tekrar", type=int, default=3, help="Persona başına deneme sayısı")
    args = ap.parse_args()
    print(f"Tutarlılık testi: {args.goruntu} × {args.tekrar} tekrar\n")
    raporla(calistir(args.goruntu, args.tekrar), args.goruntu)
