"""Disleksi metin simülasyonu (backlog: 'Develop dyslexia text simulation module').

Kelimelerin ilk ve son harfini sabit tutup iç harfleri karıştırır — disleksili
okuyucuların yaşadığı harf kayması deneyimine YAKLAŞIK bir his verir.
Bilimsel bir model değil, empati aracıdır; arayüzde de böyle etiketlenir.
Deterministik test için `tohum` parametresi alır.
"""

import random


def disleksi_metni(metin: str, oran: float = 0.6, tohum: int | None = None) -> str:
    """Metindeki kelimelerin bir kısmının iç harflerini karıştırır.

    oran: bir kelimenin karıştırılma olasılığı (0-1). Hepsini bozmak
    okunmaz bir çorba üretir; gerçek deneyim 'bazen kayan' harflerdir.
    """
    rnd = random.Random(tohum)

    def kelime_karistir(kelime: str) -> str:
        # Kısa kelimeler, sayılar ve noktalama içerenler dokunulmadan geçer.
        if len(kelime) < 4 or not kelime.isalpha() or rnd.random() > oran:
            return kelime
        ic_harfler = list(kelime[1:-1])
        rnd.shuffle(ic_harfler)
        return kelime[0] + "".join(ic_harfler) + kelime[-1]

    return " ".join(kelime_karistir(k) for k in metin.split())
