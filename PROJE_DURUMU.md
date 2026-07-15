# Proje Durumu ve Devam Planı — CogniTrace (Takım 307)

> Bu dosya, depoya ilk kez bakan/dönen bir katkıcının mevcut durumu hızlıca kavraması ve Sprint 2'ye nereden devam edeceğini görmesi için hazırlanmıştır. Güncel tarih: 2026-07-09.

## 1. Proje Nedir?

**CogniTrace**, disleksi, renk körlüğü ve DEHB gibi nöroçeşitlilik senaryolarına sahip bireyler için web sitelerindeki bilişsel yükü (cognitive load) ölçen, çoklu ajan (multi-agent) mimarili bir erişilebilirlik analiz uygulamasıdır. Ekran görüntüsü + kaynak kodu girdisiyle, persona bazlı AI analizleri üretir ve iyileştirme önerileri sunar.

Detaylar: [README.md](README.md)

## 2. Depo Yapısı

```
app/                    → Streamlit prototipi (asıl kod burada)
  app.py                → Giriş noktası / arayüz
  personas.py            → 4 persona tanımı + promptlar (disleksi, renk körlüğü, DEHB, düşük görme)
  analyzer.py             → Gemini multimodal API çağrısı, JSON çıktı üretimi
  simulation.py            → Renk körlüğü matris simülasyonu (LLM'siz, deterministik)
  requirements.txt         → streamlit, google-genai, pillow, numpy, python-dotenv
  .env.example              → GEMINI_API_KEY şablonu
  README.md                  → Kurulum ve çalıştırma talimatı

backlog/product-backlog.md → 300 puanlık tüm backlog, 3 sprint'e bölünmüş (EPIC 1-4)
docs/literatur-taramasi.md  → Özgünlük kanıtı için literatür taraması
ProjectManagement/Sprint1Documents/ → Sprint 1 kanıt görselleri + daily scrum notları
README.md                    → Takım bilgisi, ürün tanımı, Sprint 1 kapanış raporu
```

## 3. Şu Ana Kadar Yapılanlar (Sprint 1 — tamamlandı)

- Ürün adı, açıklaması, hedef kitlesi netleşti (README).
- Literatür taraması tamamlandı, benzer akademik çalışmalar (UXAgent, AXNav) incelendi.
- 4 persona promptu (W3C COGA / BDA rehberlerine dayalı) yazıldı → `app/personas.py`.
- Gemini multimodal entegrasyonu ile tekli persona analizi çalışır durumda → `app/analyzer.py`.
- Renk körlüğü simülasyonu (deterministik matris) çalışıyor → `app/simulation.py`.
- Streamlit arayüzü (v0): görüntü yükleme, persona seçimi, simülasyon açma, analiz sonucu gösterme → `app/app.py`.
- Sprint 1 kanıtları (backlog board, ürün ekran görüntüleri, daily scrum notları) README'de bağlantılı.

Genel skor şu an sadece persona skorlarının **ortalaması** alınarak hesaplanıyor (`app/app.py:97-102`) — bu geçici bir yaklaşım, gerçek koordinatör ajan Sprint 2'de gelecek.

## 4. Sprint 2 Kapsamı (6–19 Temmuz, hedef ~115 puan)

`backlog/product-backlog.md` dosyasındaki Sprint 2 story'leri:

| # | Story | Puan |
|---|---|---|
| 2.3 | URL girince Playwright ile otomatik screenshot alma | 13 |
| 2.4 | axe-core ile kural tabanlı WCAG taraması (LLM'e ek katman) | 13 |
| 3.3 | Birden fazla personayı aynı anda seçip karşılaştırmalı analiz | 8 |
| 3.4 | HTML/CSS koduyla yapısal analiz (font, satır uzunluğu, kontrast) | 13 |
| 3.5 | **Koordinatör ajan**: persona çıktılarını birleştirip genel Bilişsel Yük Skoru üretme (ajan orkestrasyonu — puanlama kriteri) | 13 |
| 4.2 | Sorunlu bölgelerin görüntü üzerinde işaretlenmesi (bounding box) | 21 |
| 4.7 | Uygulamayı ücretsiz bir platforma deploy etme (Streamlit Cloud / HF Spaces) — puanlama kriteri | 13 |

**En kritik olan**: 3.5 (koordinatör ajan orkestrasyonu) ve 4.7 (canlıya alma), çünkü bunlar bootcamp değerlendirme kriterlerinde doğrudan puanlanıyor (bkz. backlog dosyasındaki "Değerlendirme Kriterleri ↔ Backlog Eşleşmesi" tablosu).

## 5. Önerilen Devam Sırası

1. **Koordinatör ajan (3.5)** — `app/app.py` içindeki basit ortalama mantığını gerçek bir orkestrasyon katmanına taşı (persona ajanlarının çıktısını birleştiren ayrı bir modül, örn. `app/coordinator.py`).
2. **Çoklu persona karşılaştırması (3.3)** — koordinatör ile birlikte doğal olarak ilerler, arayüzde yan yana karşılaştırma görünümü eklenmeli.
3. **HTML/CSS yapısal analiz (3.4)** — `analyzer.py` zaten `html_kodu` parametresini alıyor, prompt'un buna göre genişletilmesi gerekebilir.
4. **Erken deploy (4.7)** — Sprint 2'nin ortasında bir kere deploy edip çalışır bir link elde etmek, kalan sürede iterasyon yapmayı kolaylaştırır.
5. **Playwright entegrasyonu (2.3)** ve **axe-core (2.4)** — veri/ön işleme katmanını güçlendirir, koordinatör ajandan bağımsız paralel yürütülebilir.
6. **Bounding box çizimi (4.2)** — en yüksek puanlı (21) ama en çok UI işi isteyen story; zaman kalırsa veya birden fazla kişi paralel çalışabiliyorsa öncelik verilebilir.

## 6. Ortamı Ayağa Kaldırma (hızlı hatırlatma)

```bash
cd app
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env   # GEMINI_API_KEY'i doldur (https://aistudio.google.com)
streamlit run app.py
```

Detaylı sorun giderme: [app/README.md](app/README.md#sık-karşılaşılan-sorunlar)

## 7. Açık Notlar / Riskler

- Gemini ücretsiz katman günlük kota limiti var → her üye kendi API anahtarını kullanmalı (Sprint 1 retrospektifinde alınan karar).
- Genel skor hesaplama mantığı geçici (ortalama) — koordinatör ajan bunu değiştirecek, ilgili UI metriklerinin de gözden geçirilmesi gerekir.
- `backlog/product-backlog.md` başlığında hâlâ eski ürün adı "EmpatiLens" geçiyor; README'de isim "CogniTrace" olarak güncellenmiş ama backlog dosyasının başlığı güncellenmemiş görünüyor — küçük bir tutarlılık düzeltmesi gerekebilir.
