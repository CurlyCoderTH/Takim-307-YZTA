# Literatür Taraması ve Yapılabilirlik Analizi

**Proje:** Bilişsel Yük ve Erişilebilirlik (Accessibility) Analiz Ajanı
**Takım:** Takım 307 — YZTA Bootcamp
**Tarih:** Temmuz 2026

---

## 1. Problem Tanımı ve Motivasyon

Web arayüzleri çoğunlukla "ortalama" kullanıcı için tasarlanır; oysa nüfusun önemli bir bölümü nöroçeşitlilik (neurodiversity) kapsamındadır:

| Durum | Yaygınlık | Kaynak |
|---|---|---|
| Disleksi | Nüfusun ~%10'u | British Dyslexia Association |
| Renk körlüğü | Erkeklerin ~%8'i (1/12), kadınların ~%0,5'i (1/200) | Colour Blind Awareness |
| DEHB (Dikkat eksikliği) | Nüfusun ~%5'i | WHO / literatür ortalaması |
| Düşük görme / yaşa bağlı görme kaybı | Yaş ile artan geniş kitle | WHO |

WebAIM'in her yıl yaptığı "WebAIM Million" taramasına göre en çok ziyaret edilen 1 milyon ana sayfanın **%95'inden fazlasında** tespit edilebilir WCAG hatası bulunuyor. Yani sorun gerçek ve yaygın; ancak mevcut araçların odağı teknik kural ihlalleri (alt text eksik, kontrast düşük vb.) ile sınırlı. **Bilişsel yük** — bir arayüzün kullanıcının zihinsel kapasitesine bindirdiği işlem maliyeti — bu araçların ölçmediği bir boyut.

**Projemizin iddiası:** Multimodal LLM'lere "disleksili bir kullanıcı", "deuteranopili (yeşil körü) bir kullanıcı" gibi personalar giydirerek, ekran görüntüsü üzerinden kural tabanlı araçların yakalayamadığı bilişsel/algısal sorunları yorumlatmak ve rapor üretmek.

---

## 2. Akademik Literatür

### 2.1 LLM Ajanlarıyla Kullanılabilirlik ve Erişilebilirlik Testi (fikrimize en yakın alan)

Bu alan 2024–2026 arasında hızla büyüdü; fikrimiz literatürde karşılığı olan ama **henüz ürünleşmemiş** bir noktada duruyor:

- **UXAgent** (2025) — Web tasarımlarının kullanılabilirlik testini LLM ajanlarıyla simüle eden çerçeve. Binlerce farklı personaya sahip LLM ajanı, web sitesinde gezinip kullanılabilirlik geri bildirimi üretiyor. Fikrimizin "persona simülasyonu" ayağının en güçlü akademik dayanağı. ([arXiv:2502.12561](https://arxiv.org/pdf/2502.12561), [arXiv:2504.09407](https://arxiv.org/pdf/2504.09407))
- **AXNav** (Apple, CHI 2024) — Doğal dildeki erişilebilirlik test talimatlarını LLM + UI otomasyonu ile çalıştırılabilir testlere çeviriyor. Büyük şirketlerin bu alana yatırım yaptığının kanıtı. ([arXiv:2310.02424](https://arxiv.org/abs/2310.02424))
- **UXBench** (2026) — LLM'lerin ürettiği UX eleştirilerinin "eyleme dönüştürülebilirliğini" ölçen benchmark. LLM'lerin arayüz eleştirisi üretebildiğini ama kalitesinin ölçülmesi gerektiğini gösteriyor — bizim skorlama rubriğimize ilham kaynağı. ([arXiv:2606.16262](https://arxiv.org/pdf/2606.16262))
- **Accessibility Scout** (2025) — LLM tabanlı, kişiselleştirilmiş erişilebilirlik taraması (fiziksel mekânlar için). "Persona'ya göre erişilebilirlik analizi" yaklaşımını doğruluyor. ([arXiv:2507.23190](https://arxiv.org/pdf/2507.23190))
- **Empatik erişilebilirlik hata raporları** (2026) — LLM'lerle hem empatik hem yasal-farkındalıklı erişilebilirlik bug raporu üretimi. Bizim "rapor üretme" özelliğimizin akademik karşılığı. ([arXiv:2603.23828](https://arxiv.org/pdf/2603.23828))
- **ADHD profilleriyle LLM persona kararlılığı** (2026) — LLM'lerin DEHB gibi nörogelişimsel profilleri ne kadar tutarlı simüle edebildiğini inceliyor. Hem destek hem de sınırlılık (persona tutarlılığı riski) açısından önemli. ([arXiv:2605.06307](https://arxiv.org/html/2605.06307))

### 2.2 Bilişsel Yükün Hesaplamalı Ölçümü

- **Aalto Interface Metrics (AIM)** — Aalto Üniversitesi'nin açık kaynak servisi; bir arayüz görüntüsünden görsel karmaşıklık (visual clutter), renk çeşitliliği, simetri, görsel dikkat haritası (saliency) gibi onlarca metriği hesaplar. Kural/model tabanlı bu metrikleri LLM yorumuyla birleştirmek, jüriye "sadece LLM'e sormadık, nicel metriklerle destekledik" dememizi sağlar. ([AIM makalesi](https://www.researchgate.net/publication/328322553_Aalto_Interface_Metrics_AIM_A_Service_and_Codebase_for_Computational_GUI_Evaluation), kod: interfacemetrics.aalto.fi)
- **Görsel karmaşıklık ↔ bilişsel yük ilişkisi** — Literatürde web sayfası görsel karmaşıklığının, kullanıcı üzerinde oluşan bilişsel yükün örtük (implicit) bir ölçüsü olarak kullanılabileceği gösterilmiştir ([arXiv:1005.1340](https://arxiv.org/pdf/1005.1340)).
- **Bilişsel yük ölçüm yöntemleri eleştirel analizi** (Human Factors, 2026) — Sweller'ın Bilişsel Yük Teorisi'ni arayüz değerlendirmesine bağlayan güncel çerçeve; rapor yazarken teorik zemin olarak kullanılabilir. ([SAGE](https://journals.sagepub.com/doi/10.1177/00187208261427867))
- **UIQLab** (2025) — Otomatik web arayüzü kalite değerlendirmesi ([Springer](https://link.springer.com/chapter/10.1007/978-3-031-97207-2_21)).

### 2.3 Multimodal LLM'lerin Arayüz Anlama Yeteneği (teknik fizibilite kanıtı)

- **VisualWebArena** (2024) — Multimodal ajanların gerçekçi web görevlerindeki başarımını ölçen benchmark; GPT-4V sınıfı modellerin ekran görüntülerinden arayüzü anlamlandırabildiğini gösteriyor. ([arXiv:2401.13649](https://arxiv.org/pdf/2401.13649))
- **WebVoyager** (2024) — Ekran görüntüsüyle beslenen uçtan uca web ajanı. ([arXiv:2401.13919](https://arxiv.org/html/2401.13919v3))
- **(M)LLM Tabanlı GUI Ajanları Anketi** (2025) — Alanın kapsamlı özeti; mimari seçimlerimizde referans. ([arXiv:2504.13865](https://arxiv.org/pdf/2504.13865))
- **CHI 2025: Multimodal LLM ile UI arama** — GPT-4o'ya persona + görev talimatı + özellik tanımları verilen yapılandırılmış prompt stratejisi; bizim prompt tasarımımıza doğrudan şablon. ([ACM DL](https://dl.acm.org/doi/10.1145/3706598.3714213))

### 2.4 Standartlar ve Rehberler (analiz kriterlerimizin kaynağı)

- **WCAG 2.2 (W3C)** — Erişilebilirlik standardı; ancak bilişsel erişilebilirlik kriterleri sınırlıdır.
- **W3C COGA: "Making Content Usable for People with Cognitive and Learning Disabilities"** — Bilişsel erişilebilirlik için en kapsamlı W3C rehberi ([w3.org/TR/coga-usable](https://www.w3.org/TR/coga-usable/)). Persona promptlarımızın kural setini buradan türeteceğiz.
- **British Dyslexia Association Style Guide** — Disleksi dostu tasarım kuralları: sans-serif font, 12-14pt+, satır aralığı 1.5, iki yana yaslamama (justify yok), krem/pastel arka plan, kısa paragraflar. Disleksi personamızın kontrol listesi.

---

## 3. Mevcut Araçlar ve Pazardaki Boşluk (Gap Analizi)

| Kategori | Örnekler | Ne yapar | Ne YAPAMAZ (bizim boşluğumuz) |
|---|---|---|---|
| Kural tabanlı denetçiler | [axe-core](https://www.deque.com/axe/axe-core/) (Deque), WAVE, Google Lighthouse, Pa11y | DOM üzerinde WCAG kural ihlallerini tarar | WCAG sorunlarının yalnızca **~%30-57'sini** yakalar; bilişsel yükü ve "anlaşılırlığı" hiç ölçmez |
| AI destekli yeni nesil denetçiler | EvinceAI, TestParty vb. (2025-2026 dalgası) | Kural motoru + LLM ile alt-text uygunluğu, link amacı gibi yargı gerektiren kontroller | Persona bazlı nöroçeşitlilik simülasyonu ve bilişsel yük skoru yok |
| Simülatörler | Coblis, Sim Daltonism (renk körlüğü); çeşitli disleksi simülatörleri | Görüntüyü dönüştürüp "nasıl görünüyor" gösterir | Yorum, skor ve öneri üretmez — sadece görsel dönüşüm |
| Overlay çözümleri | accessiBe, EqualWeb | Siteye eklenti olarak widget ekler | Erişilebilirlik camiasında tartışmalı; analiz değil pansuman |

**Sonuç:** Kural tabanlı tarayıcılar + simülatörler + LLM persona yorumu kombinasyonunu tek üründe birleştiren yaygın bir araç yok. Akademide parçalar var (UXAgent, AXNav, AIM) ama Türkçe destekli, jüriye demo edilebilir, persona-bazlı bilişsel yük raporu üreten bir ürün **özgün**. Karşılaştırma kaynakları: [W3C araç listesi](https://www.w3.org/WAI/test-evaluate/tools/list/), [axe vs WAVE vs Lighthouse karşılaştırması](https://accessibility-test.org/blog/compare/eaa-compliance-tool-axe-vs-wave-vs-lighthouse-comparison/), [TestParty araç rehberi](https://testparty.ai/blog/free-accessibility-tools).

---

## 4. Yapılabilirlik Analizi

### 4.1 Teknik Mimari Önerisi (3 katman)

```
[Girdi]  Ekran görüntüsü (PNG/JPG) ve/veya HTML-CSS kodu, opsiyonel URL
   │
   ▼
[Katman 1 — Ön İşleme (deterministik, ücretsiz)]
   • Renk körlüğü simülasyonu (numpy matris dönüşümü: deuteranopia/protanopia/tritanopia)
   • (Sprint 2+) axe-core ile kural tabanlı WCAG taraması
   • (Opsiyonel) AIM benzeri görsel karmaşıklık metrikleri
   │
   ▼
[Katman 2 — Persona Ajanları (multimodal LLM)]
   • Disleksi Ajanı  • Renk Körlüğü Ajanı  • DEHB Ajanı  • Düşük Görme Ajanı
   • Her ajan: görüntü + persona promptu → JSON (skor, sorunlu bölgeler, öneriler)
   │
   ▼
[Katman 3 — Koordinatör Ajan + Rapor]
   • Persona çıktılarını birleştirir, genel Bilişsel Yük Skoru (1-100) üretir
   • Öncelikli iyileştirme listesi + rapor (Streamlit arayüzü, Sprint 3'te PDF)
```

Bu "multi-agent" yapı, bootcamp değerlendirmesindeki **teknik mimari puanı** için güçlü bir hikâye sunar.

### 4.2 Model / API Seçenekleri

| Seçenek | Artı | Eksi | Değerlendirme |
|---|---|---|---|
| **Gemini 2.5 Flash (Google AI Studio)** | Ücretsiz katman (günlük istek kotası var, [güncel limitler](https://ai.google.dev/gemini-api/docs/rate-limits)), güçlü görüntü anlama, JSON çıktı modu | Kota değişken, gün içinde sınır aşılabilir | ✅ **Önerilen başlangıç** — demo ve geliştirme için yeterli |
| Claude / GPT-4o sınıfı API'ler | Çok güçlü görüntü + muhakeme | Ücretli | Bütçe varsa final demo kalitesi için düşünülebilir |
| Açık kaynak VLM (Qwen2.5-VL, LLaVA) — Ollama ile lokal | Tamamen ücretsiz, kota yok, takımın Ollama deneyimi mevcut | GPU ister, kalite API'lerden düşük | 🔄 B planı / "offline mod" özelliği olarak özgünlük katar |

> Not: Ücretsiz kotaya takılmamak için her takım üyesi kendi AI Studio anahtarını alabilir; demo günü için önbellekli örnek analizler saklanmalı.

### 4.3 Veri İhtiyacı

- Dış API bağımlılığı yok; test verisi olarak **iyi/kötü tasarlanmış 15-20 web sayfası ekran görüntüsü** yeterli (devlet siteleri, e-ticaret, haber siteleri — bilinçli kötü örnekler için eski tasarımlar).
- Doğrulama için: aynı sayfayı axe-core'dan geçirip LLM bulgularıyla karşılaştırmak (Sprint 2).

### 4.4 Riskler ve Önlemler

| Risk | Önlem |
|---|---|
| LLM halüsinasyonu (olmayan sorun uydurma) | JSON şemasıyla yapılandırılmış çıktı; ekran görüntüsündeki bölgeye referans zorunluluğu; kural tabanlı metriklerle çapraz kontrol |
| "Persona gerçekten disleksiyi temsil ediyor mu?" eleştirisi | Promptları BDA Style Guide ve W3C COGA kurallarına dayandırmak; raporda "klinik teşhis değil, tasarım rehberi uyum analizi" diye çerçevelemek (etik açıdan da doğru konum) |
| Ücretsiz API kotası | Çoklu anahtar, önbellek, lokal VLM yedeği |
| Sprint takvimine yetişememe | Sprint 1'de tek persona + tek görüntü çalışan dikey dilim (vertical slice); genişletme sonraki sprintlerde |

### 4.5 Sonuç

**Proje yapılabilir (fizibil).** Literatür fikri destekliyor ama birebir aynısını yapan yaygın ürün yok → özgünlük iddiası savunulabilir. Veri ihtiyacı düşük, ücretsiz API ile MVP çıkarılabilir, mimari hikâyesi güçlü. En büyük risk LLM çıktı güvenilirliği; bu da deterministik katman (simülasyon + kural metrikleri) ile dengelenecek.

---

## 5. Kaynakça

1. UXAgent — [arXiv:2502.12561](https://arxiv.org/pdf/2502.12561), [arXiv:2504.09407](https://arxiv.org/pdf/2504.09407)
2. AXNav (Apple) — [arXiv:2310.02424](https://arxiv.org/abs/2310.02424)
3. UXBench — [arXiv:2606.16262](https://arxiv.org/pdf/2606.16262)
4. Accessibility Scout — [arXiv:2507.23190](https://arxiv.org/pdf/2507.23190)
5. Empathetic & Legal-Aware Bug Report Generation — [arXiv:2603.23828](https://arxiv.org/pdf/2603.23828)
6. ADHD Persona Stability — [arXiv:2605.06307](https://arxiv.org/html/2605.06307)
7. Aalto Interface Metrics — [ResearchGate](https://www.researchgate.net/publication/328322553_Aalto_Interface_Metrics_AIM_A_Service_and_Codebase_for_Computational_GUI_Evaluation)
8. Cognitive Load in Web Search — [arXiv:1005.1340](https://arxiv.org/pdf/1005.1340)
9. Cognitive Load Measurement Framework (2026) — [SAGE](https://journals.sagepub.com/doi/10.1177/00187208261427867)
10. UIQLab — [Springer](https://link.springer.com/chapter/10.1007/978-3-031-97207-2_21)
11. VisualWebArena — [arXiv:2401.13649](https://arxiv.org/pdf/2401.13649)
12. WebVoyager — [arXiv:2401.13919](https://arxiv.org/html/2401.13919v3)
13. GUI Agents Survey — [arXiv:2504.13865](https://arxiv.org/pdf/2504.13865)
14. Inspirational UI Search (CHI 2025) — [ACM](https://dl.acm.org/doi/10.1145/3706598.3714213)
15. W3C COGA — [w3.org/TR/coga-usable](https://www.w3.org/TR/coga-usable/)
16. W3C Araç Listesi — [w3.org/WAI](https://www.w3.org/WAI/test-evaluate/tools/list/)
17. axe-core — [deque.com](https://www.deque.com/axe/axe-core/)
18. Araç karşılaştırmaları — [accessibility-test.org](https://accessibility-test.org/blog/compare/eaa-compliance-tool-axe-vs-wave-vs-lighthouse-comparison/), [TestParty](https://testparty.ai/blog/free-accessibility-tools)
19. Gemini API limitleri — [ai.google.dev](https://ai.google.dev/gemini-api/docs/rate-limits)
