# CogniTrace Uygulaması — Kurulum ve Çalıştırma

Bilişsel yük ve erişilebilirlik analiz ajanı (Sprint 2 sürümü).

## Kurulum (her takım üyesi kendi bilgisayarında)

```bash
# 1. Repoyu klonla
git clone https://github.com/CurlyCoderTH/Takim-307-YZTA.git
cd Takim-307-YZTA

# 2. Sanal ortam (repo kökünde)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 3. Bağımlılıklar
pip install -r app/requirements.txt

# 4. URL yakalama için tarayıcı (bir kez)
playwright install chromium

# 5. API anahtarı: app/.env.example → app/.env kopyala, anahtarını yapıştır
#    Ücretsiz: https://aistudio.google.com → "Get API key"
```

## Çalıştırma

```bash
cd app
streamlit run app.py
```

## Özellikler (Sprint 2)

| Özellik | Modül |
|---|---|
| 3 girdi kaynağı: görüntü yükle / **URL'den otomatik yakala** / örnek galeri | `app.py`, `web_capture.py` |
| 4 persona ajanı (disleksi, renk körlüğü, DEHB, düşük görme) — COGA/BDA kurallı | `personas.py`, `analyzer.py` |
| **Koordinatör ajan**: bulguları sentezler, gerekçeli genel skor + eylem planı | `coordinator.py` |
| Persona skor karşılaştırması | `app.py` |
| **axe-core WCAG taraması** (kural tabanlı çapraz doğrulama) | `web_capture.py` |
| **Sorunlu bölgelerin görüntü üzerinde işaretlenmesi** | `annotate.py` |
| Renk körlüğü simülasyonu (deuteranopia, protanopia, tritanopia, akromatopsi) | `simulation.py` |
| Disleksi metin simülasyonu (empati aracı) | `dyslexia_sim.py` |
| Örnek galerisi — analizleri kaydet, **API'siz göster** (demo sigortası) | `gallery.py` |

## Test ve Kod Kalitesi

```bash
cd app
python -m pytest tests/ -v    # 19 birim + E2E testi
ruff check .                  # lint
ruff format .                 # otomatik biçimlendirme
```

## Sık Karşılaşılan Sorunlar

- **"GEMINI_API_KEY bulunamadı"** → `.env` dosyası `app/` içinde olmalı (uzantısız, `.env.txt` değil).
- **"No module named pytest/playwright"** → `pip install -r app/requirements.txt` komutunu sanal ortam aktifken çalıştırın.
- **URL yakalama "Executable doesn't exist"** → `playwright install chromium` çalıştırılmamış.
- **429 / kota** → Ücretsiz katman limiti; başka üyenin anahtarıyla devam edin veya galeri modunu kullanın.
- **Koordinatör "yedek mod" uyarısı** → LLM'e ulaşılamadı; persona raporları yine de tam, genel skor kural tabanlı birleştirildi.
