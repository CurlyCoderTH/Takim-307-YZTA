# Spike: Chrome Eklentisi Fizibilite Değerlendirmesi

**Kart:** "Spike: Evaluate architecture and feasibility for Chrome Extension"
**Sonuç:** ✅ Teknik olarak yapılabilir — bootcamp sonrası yol haritasına alınmıştır.
**Tarih:** Temmuz 2026 · Takım 307

## Önerilen Mimari

```
[Chrome Eklentisi - Manifest V3]
  ├─ Popup UI: "Bu sayfayı analiz et" düğmesi + persona seçimi
  ├─ chrome.tabs.captureVisibleTab → aktif sekmenin ekran görüntüsü
  ├─ content script → sayfanın HTML kaynağı
  └─ HTTPS POST → CogniTrace API
                    │
[CogniTrace Backend (yeni katman)]
  ├─ FastAPI uç noktası: /analiz  (görüntü + HTML alır)
  ├─ Mevcut modüller aynen yeniden kullanılır:
  │    personas.py · analyzer.py · coordinator.py · annotate.py
  └─ JSON yanıt → eklenti popup'ında skor + öneri listesi
```

## Bulgular

1. **Ekran görüntüsü alımı:** `chrome.tabs.captureVisibleTab` görünür alanı verir;
   tam sayfa için scroll-and-stitch veya `chrome.debugger` API'si gerekir (ek izin).
2. **Mevcut kodun yeniden kullanımı:** Analiz katmanı (persona ajanları +
   koordinatör) arayüzden bağımsız yazıldığı için FastAPI arkasına taşımak
   düşük maliyetli; yalnızca Streamlit'e bağlı kısımlar (app.py) hariç.
3. **API anahtarı güvenliği:** Anahtar eklentiye gömülemez — backend zorunlu.
   Bu da barındırma maliyeti ve kullanıcı kimliklendirme ihtiyacı doğurur
   (backlog'daki OAuth kartıyla birleşir).
4. **Mağaza süreci:** Chrome Web Store incelemesi 1-2 hafta; bootcamp
   takvimine sığmaz.

## Karar

Bootcamp kapsamında **yapılmayacak**; mimari hazır olduğundan mezuniyet
sonrası ilk geliştirme hedefi olarak vizyon planına eklendi. Jüri sunumunda
"gelecek planları" bölümünde bu dokümana atıf yapılacaktır.
