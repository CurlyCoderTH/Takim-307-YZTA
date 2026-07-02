# Product Backlog — EmpatiLens (Toplam: 300 Puan)

> Bu dosyadaki kartları Miro board'a taşıyın. Önerilen Miro düzeni aşağıda.

## Miro Board Düzeni Önerisi

**Sütunlar:** `Product Backlog` → `Sprint Backlog` → `In Progress` → `Review` → `Done`

**Kart formatı:** Başlık + story point (kartın sağ üst köşesine) + üye rengi
**Renk kodu:** Her takım üyesine bir renk (örn. [İSİM 1]=sarı, [İSİM 2]=mavi, [İSİM 3]=yeşil, [İSİM 4]=pembe, [İSİM 5]=turuncu)
**Epic'ler:** 4 epic'i ayrı şerit (swimlane) olarak yerleştirin.

---

## EPIC 1: Araştırma & Planlama

| # | User Story | Puan | Sprint |
|---|---|---|---|
| 1.1 | Bir takım üyesi olarak, projenin özgünlüğünü kanıtlamak için benzer akademik çalışmaları ve rakip ürünleri içeren bir literatür taraması istiyorum | 13 | 1 |
| 1.2 | Bir takım olarak, fikri netleştirip kapsam dokümanı (ürün adı, açıklama, hedef kitle) oluşturmak istiyoruz | 8 | 1 |
| 1.3 | Bir takım olarak, GitHub reposunu Scrum template'e uygun kurmak istiyoruz | 5 | 1 |
| 1.4 | Bir takım olarak, Miro'da product backlog board'u kurmak istiyoruz | 5 | 1 |
| 1.5 | Bir takım olarak, rol dağılımı ve daily scrum iletişim planı yapmak istiyoruz | 3 | 1 |

**Epic 1 toplamı: 34**

## EPIC 2: Veri & Ön İşleme

| # | User Story | Puan | Sprint |
|---|---|---|---|
| 2.1 | Bir geliştirici olarak, test için iyi/kötü tasarlanmış 15-20 web sayfası ekran görüntüsünden oluşan bir set toplamak istiyorum | 5 | 1 |
| 2.2 | Bir kullanıcı olarak, yüklediğim ekran görüntüsünün renk körü bir bireye nasıl göründüğünü görmek istiyorum (deuteranopia/protanopia/tritanopia simülasyonu) | 8 | 1 |
| 2.3 | Bir kullanıcı olarak, ekran görüntüsü yerine URL girdiğimde sistemin otomatik screenshot almasını istiyorum (Playwright) | 13 | 2 |
| 2.4 | Bir geliştirici olarak, axe-core ile kural tabanlı WCAG taramasını LLM analizine ek katman olarak entegre etmek istiyorum | 13 | 2 |

**Epic 2 toplamı: 39**

## EPIC 3: AI Ajan Geliştirme

| # | User Story | Puan | Sprint |
|---|---|---|---|
| 3.1 | Bir geliştirici olarak, W3C COGA ve BDA rehberlerine dayalı 4 persona promptu (disleksi, renk körlüğü, DEHB, düşük görme) tasarlamak istiyorum | 13 | 1 |
| 3.2 | Bir kullanıcı olarak, ekran görüntüsünü tek personayla analiz edip JSON formatında skor + sorun + öneri almak istiyorum (Gemini entegrasyonu, PoC) | 13 | 1 |
| 3.3 | Bir kullanıcı olarak, birden fazla personayı aynı anda seçip karşılaştırmalı analiz almak istiyorum | 8 | 2 |
| 3.4 | Bir kullanıcı olarak, HTML/CSS kodumu da vererek yapısal analiz (font, satır uzunluğu, kontrast tanımları) almak istiyorum | 13 | 2 |
| 3.5 | Bir geliştirici olarak, persona ajanlarını orkestre eden ve çıktılarını birleştirip genel Bilişsel Yük Skoru üreten koordinatör ajan (AI agent orkestrasyonu — puanlama kriteri) geliştirmek istiyorum | 13 | 2 |
| 3.6 | Bir geliştirici olarak, LLM çıktılarının tutarlılığını örnek set üzerinde test etmek istiyorum (aynı görüntüye 3 çalıştırma, skor sapması ölçümü) | 8 | 3 |

**Epic 3 toplamı: 68**

## EPIC 4: Arayüz & Rapor

| # | User Story | Puan | Sprint |
|---|---|---|---|
| 4.1 | Bir kullanıcı olarak, görüntü yükleyip analiz başlatabileceğim basit bir web arayüzü istiyorum (Streamlit v0) | 13 | 1 |
| 4.2 | Bir kullanıcı olarak, sorunlu bölgelerin görüntü üzerinde işaretlenmesini istiyorum (bounding box çizimi) | 21 | 2 |
| 4.3 | Bir kullanıcı olarak, analiz sonucunu PDF rapor olarak indirmek istiyorum | 13 | 3 |
| 4.4 | Bir kullanıcı olarak, "önce/sonra" karşılaştırması görmek istiyorum (önerilen iyileştirmeler uygulanmış hali) | 21 | 3 |
| 4.5 | Bir takım olarak, 3 dakikalık YouTube tanıtım videosu ve final sunumu hazırlamak istiyoruz (teslim şartı) | 13 | 3 |
| 4.6 | Bir takım olarak, kullanıcı dokümantasyonu ve README'yi tamamlamak istiyoruz | 8 | 3 |
| 4.7 | Bir geliştirici olarak, uygulamayı ücretsiz bir platforma deploy etmek istiyorum (Streamlit Cloud / HuggingFace Spaces) — canlıya alma puan kriteri olduğu için Sprint 2'ye çekildi | 13 | 2 |
| 4.8 | Bir kullanıcı olarak, geçmiş analizlerimin ajan hafızasında saklanmasını ve yeni analizlerle karşılaştırılmasını istiyorum (agent memory — puanlama kriteri) | 8 | 3 |

**Epic 4 toplamı: 110**

*(Kalan 49 puan Sprint 2-3'te çıkacak yeni ihtiyaçlar için rezerv tutulmuştur — sprint planlamalarında dağıtın veya story'leri detaylandırırken kullanın.)*

---

## Sprint Dağılımı Özeti

| Sprint | Tarih | Story'ler | Hedef Puan |
|---|---|---|---|
| Sprint 1 | 19 Haziran – 5 Temmuz | 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 3.1, 3.2, 4.1 | **90** |
| Sprint 2 | 6 – 19 Temmuz | 2.3, 2.4, 3.3, 3.4, 3.5, 4.2, 4.7 | **~115** |
| Sprint 3 | 20 Temmuz – 2 Ağustos | 3.6, 4.3, 4.4, 4.5, 4.6, 4.8 | **~95** |

---

## Değerlendirme Kriterleri ↔ Backlog Eşleşmesi

Bursiyer Kılavuzu'ndaki YZ puanlama tablosuna göre hangi story hangi puanı hedefliyor:

| Kriter (Max Puan) | İlgili Story'ler |
|---|---|
| AI modeli seçimi, kullanımı, geliştirmesi (20) | 3.1, 3.2, 3.4 — persona promptları W3C COGA/BDA rehberlerine dayalı, JSON şema zorunlu |
| AI Agent kullanımı, hafıza, orkestrasyon (15) | 3.3, 3.5 (çoklu persona ajanı + koordinatör orkestrasyon), 4.8 (hafıza) |
| Mimari yapı, temiz kod (15) | 3 katmanlı mimari (ön işleme → persona ajanları → koordinatör), modüler dosya yapısı |
| Canlıya alma (10) | 4.7 — Sprint 2'de erken deploy |
| Özgünlük (10) | 1.1 literatür taraması ile kanıtlanmış boşluk (gap) |
| Yarışmaya hazır çalışan proje (10) + tamamlanma (10) | Her sprintte çalışan dikey dilim yaklaşımı |
| Pazara uygunluk (10) | Hedef kitle: erişilebilirlik uyumu zorunlu kurumlar (EAA/WCAG yasal baskısı) |

> ⚠️ Kılavuz uyarısı: "Özellik yalnızca eklenmiş olmak için eklendiyse puan verilmez." — Ajan orkestrasyonu ve hafıza bizim üründe doğal ihtiyaç (her persona ayrı uzman ajan, hafıza=analiz geçmişi karşılaştırma), bu gerekçeyi sunumda vurgulayın.
