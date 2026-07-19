# **Takım İsmi**

Takım 307

# Ürün İle İlgili Bilgiler

## Takım Elemanları

- Gökhan Dumlupınar: Product Owner
- Tuana Hergüner: Scrum Master 
- M.Buğrahan Bayrakçı: Developer
- Mustafa Yazbahar: Developer
- Şükran Akşimşek: Developer

## Ürün İsmi

CogniTrace

## Ürün Açıklaması

- Geliştireceğimiz multimodal web analiz uygulaması ile disleksi, renk körlüğü ve DEHB gibi nöroçeşitlilik senaryolarına sahip bireylerin web sitelerinde karşılaştığı bilişsel yükü (Cognitive Load) ölçümleyeceğiz. Web sitelerinin ekran görüntülerini ve kaynak kodlarını işleyen çoklu ajan (Multi-Agent) mimarimiz, arayüzdeki erişilebilirlik bariyerlerini tespit ederek tasarımcılara ve yazılımcılara yapay zeka tabanlı iyileştirme raporları ve pratik kod yamaları sunacaktır.

## Ürün Özellikleri

- **Disleksi ve Tipografi Analizi:** Sayfadaki yazı tiplerini, satır aralıklarını ve metin yoğunluklarını okuma güçlüğü perspektifinden inceleme.
- **Renk Körlüğü Kontrast Denetimi:** Farklı renk körlüğü tiplerine (Protanopia, Deuteranopia vb.) göre WCAG 2.2 standartlarında görsel analiz yapma.
- **Bilişsel Yük Haritalandırma:** Pop-up'lar, dikkat dağıtıcı ögeler ve karmaşık menü yapıları üzerinden arayüzün zihinsel yorgunluk skorunu çıkarma.
- **Yapay Zeka Ajan Orkestrasyonu:** Özelleşmiş alt ajanların (Specialist Agents) ortak bir hafıza (Memory) kullanarak entegre ve dinamik bir UX erişilebilirlik raporu oluşturması.

## Hedef Kitle

- Web Tasarımcıları ve UI/UX Profesyonelleri
- Ön Yüz (Frontend) ve Web Geliştiricileri
- Dijital platformlarında kapsayıcılık ve tam erişilebilirlik sağlamak isteyen teknoloji şirketleri
- Nöroçeşitli bireyler için içerik üreten platformlar

## Product Backlog URL

[Miro Backlog Board](https://miro.com/app/board/uXjVH_KUIII=/)

---

# Sprint 1

- **Sprint içinde tamamlanması tahmin edilen puan:** 90 Puan

- **Puan tamamlama mantığı:** Proje boyunca tamamlanması gereken toplam backlog puanı 300'dür. İlk sprint araştırma, kurulum ve temel prototip odaklı olduğundan 90 puan; Sprint 2'de çekirdek özellik geliştirme (110 puan); Sprint 3'te tamamlama, test ve sunum (100 puan) hedeflenmiştir. Detaylı story listesi: [backlog/product-backlog.md](backlog/product-backlog.md)

- **Backlog düzeni ve Story seçimleri**: Backlog'umuz ilk sprintte odaklanılması gereken temel altyapı ve fizibilite story'lerine göre düzenlenmiştir. Sprint başına tahmin edilen puan sayısını geçmeyecek şekilde sıradan seçimler yapılmaktadır.  

Story'ler yapılacak işlere (task'lere) bölünmüştür. Miro Board'da gözüken kırmızı item'lar yapılacak işleri (task) gösterirken, mavi item'lar story'leri temsil etmektedir.

- **Daily Scrum**: Daily Scrum toplantılarının zamansal senkronizasyonu kolaylaştırmak ve hızlı aksiyon alabilmek adına WhatsApp üzerinden yapılmasına karar verilmiştir. Daily Scrum notları: [Sprint 1 Daily Scrum Notları](https://raw.githubusercontent.com/CurlyCoderTH/Takim-307-YZTA/main/ProjectManagement/Sprint1Documents/DailyScrumMeetingNotesSprint1.docx)

- **Sprint board update**: Sprint board screenshotları: 
  ![Backlog 1](ProjectManagement/Sprint1Documents/backlog1.png)
  ![Backlog 2](ProjectManagement/Sprint1Documents/backlog2.png)
  ![Backlog 3](ProjectManagement/Sprint1Documents/backlog3.png)

- **Ürün Durumu**: Ekran görüntüleri:
  ![Ürün 1](ProjectManagement/Sprint1Documents/productss1.png)
  ![Ürün 2](ProjectManagement/Sprint1Documents/productss2.png)
  ![Ürün 3](ProjectManagement/Sprint1Documents/productss3.png)
  ![Ürün 4](ProjectManagement/Sprint1Documents/productss4.png)
  ![Ürün 5](ProjectManagement/Sprint1Documents/productss5.png)
  ![Ürün 6](ProjectManagement/Sprint1Documents/productss6.png)

- **Sprint Review**: 
Alınan kararlar: Ürün ismi "CogniTrace" olarak kesinleştirilmiş, persona seti (disleksi, renk körlüğü, DEHB, düşük görme) belirlenmiştir. Literatür taraması tamamlanmış ([docs/literatur-taramasi.md](docs/literatur-taramasi.md)); benzer akademik çalışmalar (UXAgent, AXNav) incelenmiş, birebir rakip ürün olmadığı doğrulanarak özgünlük iddiası güçlendirilmiştir. Prototip çalışır durumdadır: ekran görüntüsü yükleme, Gemini ile persona bazlı bilişsel yük analizi ve renk körlüğü simülasyonu test edilmiştir. Geliştirme sırasında karşılaşılan Gemini istemci bağlantı hatası tespit edilip giderilmiştir. URL'den otomatik ekran görüntüsü alma, koordinatör ajan orkestrasyonu ve uygulamanın canlıya alınması Sprint 2'ye aktarılmıştır. Sprint Review katılımcıları: Gökhan Dumlupınar, Tuana Hergüner, M.Buğrahan Bayrakçı, Mustafa Yazbahar, Şükran Akşimşek

- **Sprint Retrospective:**
  - WhatsApp üzerindeki günlük iletişim sıklığının artırılması ve kod commit'lerinin daha düzenli yapılması kararlaştırılmıştır.
  - Daily scrum için sabit bir akşam saati belirlenmiştir.
  - Kota riskine karşı her üyenin kendi Gemini API anahtarını alması kararlaştırılmıştır.
  - Sprint 2 görev dağılımının planlama toplantısında epic bazında yapılmasına karar verilmiştir.

---

# Sprint 2
- **Sprint içinde tamamlanması tahmin edilen puan:** 134 Puan

- **Puan tamamlama mantığı:** Sprint 1'de 90 puanlık temel tamamlandığı için çekirdek özellik geliştirme sprintine 134 puan hedeflenmiştir. Sprint içinde eklenen yeni kartlarla toplam backlog 300'ün üzerine çıkmıştır; backlog yaşayan bir liste olarak yönetilmektedir. Deploy (4.7) bilinçli olarak Sprint 3'ün ilk gününe alınmış, buna karşılık 4.3 PDF raporu plandan önce bu sprintte tamamlanmıştır.

- **Backlog düzeni ve Story seçimleri**: Çekirdek story'ler (URL yakalama, axe-core, koordinatör ajan orkestrasyonu, görsel işaretleme) ile sprint içinde ihtiyaçtan doğan küçük kartlar birlikte yönetilmiştir. Kırmızı item'lar task'ları, mavi item'lar story'leri temsil etmektedir; tüm kartlarda puan ve sorumlu ataması vardır.

- **Daily Scrum**: WhatsApp üzerinden yazılı yürütülmüştür: [Sprint 2 Daily Scrum Notları](https://raw.githubusercontent.com/CurlyCoderTH/Takim-307-YZTA/main/ProjectManagement/Sprint2Documents/DailyScrumMeetingNotesSprint2.docx)

- **Sprint board update**: Sprint board screenshotları:
  ![Backlog 1](ProjectManagement/Sprint2Documents/backlog1.png)
  ![Backlog 2](ProjectManagement/Sprint2Documents/backlog2.png)

- **Ürün Durumu**: Ekran görüntüleri:
  ![Ürün 1](ProjectManagement/Sprint2Documents/productss1.png)
  ![Ürün 2](ProjectManagement/Sprint2Documents/productss2.png)
  ![Ürün 3](ProjectManagement/Sprint2Documents/productss3.png)
  ![Ürün 4](ProjectManagement/Sprint2Documents/productss4.png)
  ![Ürün 5](ProjectManagement/Sprint2Documents/productss5.png)
  ![Ürün 6](ProjectManagement/Sprint2Documents/productss.png)

- **Sprint Review**:
Alınan kararlar: [18 Temmuz toplantısından sonra doldurun — iskelet: koordinatör ajan, URL yakalama, axe-core, işaretleme, galeri, PDF, premium arayüz tamamlandı / dogfooding ve 10 site ligi Sprint 3'e aktarıldı / Sprint 3 hedefi: ilk gün deploy + video + önce/sonra + hafıza]. Katılımcılar: [isimler]

- **Sprint Retrospective:**
  - [18 Temmuz toplantısından sonra doldurun]

---

# Sprint 3

---
