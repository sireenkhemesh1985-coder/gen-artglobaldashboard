# GEN-ART Global Patient Intelligence Platform
> **AI-Powered International Patient Acquisition, Market Intelligence & Conversion Management**
> T.C. Sağlık Bakanlığı Uluslararası Sağlık Turizmi Yetki Belgesi: **ST-0625** | Ankara, Türkiye

---

## 📌 Proje Genel Bakış ve Amaç
Bu platform, **GEN-ART Tüp Bebek ve Üreme Genetiği Merkezi** için özel olarak tasarlanmış kurumsal bir B2C uluslararası hasta kazanım ve karar destek kokpitidir.

`genart-dashboard.docx` ve `IVF SÜREÇLERİ.xlsx` dosyalarında yer alan tüm stratejik hedefler, operasyonel klinik protokoller ve veri modelleri eksiksiz uygulanmıştır:
* **B2C Hasta Kazanım Odaklılığı:** Uluslararası hastayı anlama, doğru medikal mesajla çekme, konsültasyona yönlendirme ve Ankara'da tedaviye dönüştürme odağı.
* **Klinik Farklılaşma:** Sıradan bir IVF kliniği pazarlaması yerine; **Üreme Genetiği, PGT-A / PGT-M / PGT-SR, Şiddetli Erkek Kısırlığı (Mikro TESE) ve Tekrarlayan IVF Başarısızlıkları** odaklı medikal segmentasyon.
* **Görsel Kimlik:** Koyu Lacivert & Neon Turkuaz (**Dark Navy #070D1E & Turquoise #00F0FF**) modern medikal yönetici kokpiti teması.
* **3 Katmanlı Mimari:** Data Layer, Intelligence Layer ve Executive Dashboard.

---

## 🚀 8 Temel Modül Mimarisi

### 1. 🌐 Yönetici Özeti (Global Cockpit & Executive Overview)
* **6 Temel KPI Kartı:**
  1. *Yeni Başvuru Sayısı* (Inquiries / Leads)
  2. *Konsültasyon Gerçekleşme Oranı* (% Qualified / Consultation rate)
  3. *Tedaviye Başlayan Hasta Sayısı* (Treatment starts in Ankara)
  4. *Başvurudan Tedaviye Dönüşüm Oranı* (Overall CVR %)
  5. *Hasta Başına Pazarlama Maliyeti* (CAC - Cost per Patient)
  6. *Uluslararası Hasta Geliri* (Revenue in EUR)
* **Hasta Edinme Hunisi (Funnel):** Yeni Başvuru → Nitelikli Ön Eleme → Doktor Konsültasyonu → Tedavi Planı Onayı → Tedavi Başlangıcı (Ankara).
* **Tekil Ülke Performans Tablosu:** Her ülke bağımsız tek satırda gösterilir (Irak ve Ürdün ayrı tutulur; grup birleştirmesi yapılmaz).
* **Takibi Geciken Başvurular (SLA Alerts):** İlk yanıt süresi hedefi (4 saat) aşılmış kayıtların anlık takibi.
* **Onaylanan Stratejik Eylem Planları:** *Sorun/Fırsat → Dayanak Veri → Karar → Sorumlu → Son Tarih → Durum → Gerçekleşen Sonuç* yapısında açılır detay pencereleri.

### 2. 🌍 3D Hasta Akış Küresi & Küresel Pazar Zekası (Market Intelligence & MCDA)
* **3D Patient Flow Globe (Pydeck / ArcLayer):** Hedef ülkelerden Ankara Esenboğa Havalimanı'na (ESB) uzanan hasta akış koridorları ve hasta yoğunlukları.
* **AI Ülke Cazibe Skorlama Modeli (MCDA):** $S_c = \sum_{i=1}^{6} w_i \cdot x_{c,i}$ formülüyle dinamik ağırlıklandırma:
  - *Hasta Talebi (%25)*
  - *Tedavi Karşılanabilirliği / Alım Gücü (%20)*
  - *Seyahat & Lojistik Erişilebilirlik (%15)*
  - *Rekabet & Genetik Farklılaşma (%15)*
  - *Dijital Fırsat (%15)*
  - *Yasal & Operasyonel Uygunluk (%10)*
* **Ülke 360° Derinlik Profili:** Vize şartları, direkt/aktarmalı uçuş süreleri, ortalama kalış süresi (15-20 gün) ve stratejik pazar hipotezleri.

### 3. 👥 Uluslararası Hasta CRM & Dönüşüm Kayıp (Drop-off) Analizleri
* **Neden Kaybettik? (Root-Cause Breakdown):** 100 başvurudan neden sadece 6'sının tedaviye başladığını ortaya koyan yapılandırılmış kayıp nedenleri:
  - *Maliyet / Bütçe Yetersizliği*
  - *Seyahat & Vize Zorlukları*
  - *Plan Değişikliği / Erteleme*
  - *Tıbbi Uygunsuzluk*
  - *İletişim & Yanıt Gecikmesi*
  - *Başka Klinik Tercihi*
* **İnteraktif Dönüşüm Simülatörü:** Başvuru hacmi ve aşama geçiş oranları girilerek beklenen hasta ve ciro simülasyonu.
* **De-Identified Hasta Takip Listesi:** KVKK ilkelerine uygun, kişisel veri (PII) arındırılmış operasyonel liste.

### 4. 🎯 Dijital Pazarlama, Arama & Hasta Keşfi (Marketing Discovery)
* **Kanal Başarı & Attribution Matrisi:** Google Ads, Meta, Organik SEO, WhatsApp Healthline ve Tıbbi Referansların gerçek tedaviye dönüşüm katsayıları.
* **Klinik Tedavi Protokolleri Dağılımı:** Standart IVF (17 gün), IVF+PGT Dondurmalı (12+15 gün), Express PGT-A NGS (17 gün) ve FET (14-15 gün) süreçlerinin hasta tercihleri ve gelir analizi.
* **Medikal Segment Matrisi:** Tekrarlayan başarısız IVF, şiddetli erkek kısırlığı ve genetik hastalık odaklı arama performansı.
* **Dil Analizi:** Arapça, Rusça, İngilizce, Türkçe ve Balkan dilleri performans dağılımları.

### 5. 🤖 AI Tahminleme & Hasta Kazanım Fırsat Motoru (AI Forecasting & Opportunity Engine)
* **3 Temel Karar Sorusu:**
  1. *Hangi ülkeler anlamlı talep üretiyor?*
  2. *Hangi ülkeler sürdürülebilir CAC ile hasta sağlıyor?*
  3. *Tedavi başlangıcını hangi bariyerler önlüyor?*
* **What-If Senaryo Simülatörü:** Pazarlama bütçesi değişimi (+%25), yanıt süresi iyileştirmesi ve yeni dil açılışlarının (örn. Rusça pazar) çoklu değişken analizi.
* **Bütçe Optimizasyonu:** Düşük getirili kanallardan yüksek marjlı genetik/türki cumhuriyetler pazarlarına bütçe kaydırma önerileri.

### 6. ✈️ Uluslararası Hasta Seyahat, Vize & Tedavi Lojistiği (Travel Coordination)
* **Resmi GEN-ART Tedavi Protokolleri:** Excel tablosundaki 4 resmi süreç ve kalış süreleri.
* **İnteraktif Hasta Seyahat Takvimi Hesaplayıcı:** Hastanın adet başlangıç tarihine göre Ankara varış, kalış süresi ve ayrılış tarihlerini otomatik hesaplama aracı.
* **Vize Matrisi:** Vizesiz/Kimlikle giriş, Kolay e-vize ve Etiket/Medikal vize kolaylaştırma takibi.
* **Ankara Esenboğa Ulaşım Hatları:** Uçuş süreleri ve direkt sefer analizleri.

### 7. 🛡️ Mevzuat, Etik & KVKK Uyumluluk Denetimi
* **2025 Mevzuatı Kontrol Listesi:** T.C. Sağlık Bakanlığı 26 Nisan 2025 Sağlık Turizmi Yönetmeliği ve 12 Kasım 2025 Tanıtım Yönetmeliği uyum maddeleri.
* **Human-in-the-Loop Reklam Onay Mekanizması:** Başarı garantisi ifadelerinin engellenmesi ve zorunlu hekim incelemesi.
* **KVKK Ayrıştırma İlkeleri:** Hassas klinik sağlık kayıtları ile pazarlama karar destek verilerinin tam izolasyonu.

### 8. 📊 Yönetici Raporları & Veri Dışa Aktarma Merkezi
* **1. Yönetici Raporu (.xlsx):** Seçilen dönem, KPI kartları, ülke tablosu ve eylem planlarını içeren çok sekmeli Excel raporu.
* **2. Performans Verisi (.csv):** Analitik ekipler için hasta kimlik bilgisi içermeyen pazar ve kanal bazlı veri seti.
* **3. Operasyon Takip Listesi (.csv):** Yalnızca yetkili koordinatörlerin eriştiği başvuru ve takip kayıtları.

---

## 🛠️ Kurulum ve Çalıştırma

Platform standart Python kütüphaneleriyle çalışmaktadır:
```bash
# Projeyi başlatın
python -m streamlit run app.py
```
Veya klasördeki **`GENART_Dashboard_Baslat.bat`** dosyasına çift tıklayabilirsiniz.
Uygulama **`http://localhost:8501`** adresinde açılır.
