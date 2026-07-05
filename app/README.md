# CogniTrace Prototip — Kurulum ve Çalıştırma

Sprint 1 dikey dilimi: ekran görüntüsü + persona seçimi → bilişsel yük analizi.

## Kurulum (her takım üyesi kendi bilgisayarında)

```bash
# 1. Repoyu klonla ve app klasörüne gir
git clone https://github.com/CurlyCoderTH/Takim-307-YZTA.git
cd Takim-307-YZTA/app

# 2. Sanal ortam oluştur ve etkinleştir
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# 3. Bağımlılıkları kur
pip install -r requirements.txt

# 4. API anahtarını ayarla
# .env.example dosyasını .env olarak kopyala ve anahtarını yapıştır
# Anahtar ücretsiz: https://aistudio.google.com → "Get API key"
```

## Çalıştırma

```bash
streamlit run app.py
```

Tarayıcıda `http://localhost:8501` açılır:
1. Soldan bir web sitesi ekran görüntüsü yükle (PNG/JPG)
2. Persona(lar) seç (disleksi, renk körlüğü, DEHB, düşük görme)
3. İstersen renk körlüğü simülasyonunu aç
4. **Analiz Et** butonuna bas

## Dosya Yapısı

| Dosya | Görev |
|---|---|
| `app.py` | Streamlit arayüzü (giriş noktası) |
| `personas.py` | Persona tanımları ve promptları (W3C COGA / BDA kurallarına dayalı) |
| `analyzer.py` | Gemini multimodal API çağrısı, JSON çıktı |
| `simulation.py` | Renk körlüğü matris simülasyonu (deterministik, LLM'siz) |

## Sık Karşılaşılan Sorunlar

- **"GEMINI_API_KEY bulunamadı"** → `.env` dosyasını `app/` klasörünün içinde oluşturduğunuzdan emin olun.
- **429 / kota hatası** → Ücretsiz katman günlük istek limitine takıldınız; başka bir üyenin anahtarıyla devam edin veya ertesi günü bekleyin.
- **JSON parse hatası** → Nadiren model şema dışına çıkabilir; "Analiz Et"e tekrar basın.
