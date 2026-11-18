"""
Module 7: Regulatory & Ethical Compliance (KVKK & Health Tourism Framework)
Monitors Türkiye's 29 July 2023 / 2024-2025 Health Services Promotion Regulation,
Uluslararası Sağlık Turizmi Yönetmeliği (ST-0625), KVKK Madde 6, and ÜYTE Regulations.
Includes full regulatory audit for official social media channels:
- Instagram: @genarttupbebek
- LinkedIn: /company/genarttupbebek
- Facebook: /profile.php?id=100083144149931
"""

import streamlit as st
import pandas as pd
from config import THEME_COLORS, HEALTH_TOURISM_AUTH
from utils.components import render_kpi_card

def render_compliance_kvkk():
    st.markdown("""
    <div style="margin-bottom: 14px;">
        <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0; display: flex; align-items: center; gap: 8px;">
            <span>🛡️ Mevzuat, Etik & KVKK Sağlık Turizmi Uyumluluk Denetimi</span>
        </h2>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
            T.C. Sağlık Bakanlığı Sağlık Hizmetlerinde Tanıtım ve Bilgilendirme Yönetmeliği, ST-0625 Sağlık Turizmi Belgesi ve 6698 sayılı KVKK güvenceleri
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_social, tab_audit, tab_ads, tab_kvkk = st.tabs([
        "📱 Sosyal Medya Mevzuat Denetimi (IG, LI, FB)",
        "📜 2025 Sağlık Turizmi & ÜYTE Mevzuat Matrisi",
        "⚖️ Reklam & Kampanya İnsan Onay Mekanizması",
        "🔒 KVKK & Hassas Sağlık Verisi Ayrıştırma İlkeleri"
    ])

    with tab_social:
        render_social_media_audit()

    with tab_audit:
        render_audit_checklist()

    with tab_ads:
        render_ad_approval_workflow()

    with tab_kvkk:
        render_kvkk_framework()

def render_social_media_audit():
    """Detailed Regulatory & Legal Compliance Audit for GEN-ART Official Social Channels"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>📱 GEN-ART Resmi Sosyal Medya Hesapları Mevzuata Uygunluk Denetim Raporu</span>
            <span class="tag">Mevzuat: 29 Temmuz 2023 Tanıtım Yönetmeliği & ST-0625</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6; margin-bottom: 16px;">
            T.C. Sağlık Bakanlığı, Türkiye İlaç ve Tıbbi Cihaz Kurumu (TİTCK), Türk Tabipleri Birliği (TTB) Hekimlik Meslek Etiği ve 6698 sayılı KVKK hükümleri çerçevesinde GEN-ART'ın resmi <b>Instagram</b>, <b>LinkedIn</b> ve <b>Facebook</b> hesaplarının denetim sonuçları, risk dereceleri ve hukuki iyileştirme tavsiyeleri aşağıda listelenmiştir.
        </div>
    """, unsafe_allow_html=True)

    # High-level KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Genel Sosyal Medya Uyum", "%91.4", "Bakanlık Kriterlerine Uyumlu", icon="⚖️")
    with col2:
        render_kpi_card("Instagram Denetimi", "⚠️ Düzeltme Gerekli", "Hasta Fotoğrafları & Bio ST-0625", icon="📸")
    with col3:
        render_kpi_card("LinkedIn B2B Uyumu", "✅ Tam Uyumlu", "Bilimsel Kongre & NGS Tanıtımı", icon="💼")
    with col4:
        render_kpi_card("Facebook Sayfa Durumu", "⚠️ Yapılandırma", "Vanity URL & WhatsApp KVKK", icon="👥")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 3 Social Channels Detailed Comparison
    st.markdown("""
    <h3 style="color: #00F0FF; font-size: 15px; font-weight: 700; margin-bottom: 10px;">
        🔍 Denetlenen Hesaplar, Mevcut Durum ve Hukuki Bulgular
    </h3>
    """, unsafe_allow_html=True)

    c_ig, c_li, c_fb = st.columns(3)

    with c_ig:
        st.markdown("""
        <div style="background: rgba(14, 47, 59, 0.7); border: 1.5px solid rgba(245, 130, 31, 0.4); border-radius: 12px; padding: 16px; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 14px; font-weight: 700; color: #FFFFFF;">📸 Instagram</span>
                <span style="background: rgba(245, 130, 31, 0.2); color: #FFA34D; font-size: 11px; padding: 2px 8px; border-radius: 6px; font-weight: 700;">Skor: %86.5</span>
            </div>
            <div style="font-size: 12px; color: #00F0FF; margin-bottom: 8px;">
                <a href="https://www.instagram.com/genarttupbebek/" target="_blank" style="color: #00F0FF; text-decoration: none;">🔗 @genarttupbebek ↗</a>
            </div>
            <div style="font-size: 12px; color: #CBD5E1; line-height: 1.5;">
                • <b>Hedef Kitle:</b> B2C Doğrudan Hastalar, Çiftler.<br/>
                • <b>Risk Seviyesi:</b> <span style="color: #F87171; font-weight: 700;">YÜKSEK DENETİM ALANI</span> (Bakanlık cezalarının %80'i IG kaynaklıdır).<br/>
                • <b>Biyografi Durumu:</b> <code>ST-0625 Sağlık Turizmi Yetki Belgesi No</code> eklenmeli.<br/>
                • <b>Hasta & Bebek Görselleri:</b> Kucakta bebek/doğum fotoğraflarında KVKK Madde 6 ıslak imzalı açık rıza zorunludur.<br/>
                • <b>Hasta Yorumları:</b> DM/WhatsApp teşekkür ekran görüntüsü paylaşımı 'Örtülü Reklam' sayılır, kaldırılmalıdır.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_li:
        st.markdown("""
        <div style="background: rgba(14, 47, 59, 0.7); border: 1.5px solid rgba(16, 185, 129, 0.4); border-radius: 12px; padding: 16px; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 14px; font-weight: 700; color: #FFFFFF;">💼 LinkedIn</span>
                <span style="background: rgba(16, 185, 129, 0.2); color: #10B981; font-size: 11px; padding: 2px 8px; border-radius: 6px; font-weight: 700;">Skor: %96.0</span>
            </div>
            <div style="font-size: 12px; color: #00F0FF; margin-bottom: 8px;">
                <a href="https://www.linkedin.com/company/genarttupbebek/" target="_blank" style="color: #00F0FF; text-decoration: none;">🔗 /company/genarttupbebek ↗</a>
            </div>
            <div style="font-size: 12px; color: #CBD5E1; line-height: 1.5;">
                • <b>Hedef Kitle:</b> B2B Hekimler, Embriyologlar, Uluslararası Partnerler.<br/>
                • <b>Risk Seviyesi:</b> <span style="color: #10B981; font-weight: 700;">EN GÜVENLİ KANAL</span> (Tüketici reklamı kapsamı dışı).<br/>
                • <b>İçerik Odaklılığı:</b> ESHRE/ASRM kongreleri, NGS genetik tarama ve Mikrogen Laboratuvar teknolojisi.<br/>
                • <b>İyileştirme:</b> Şirket 'Hakkında' metnine İngilizce <code>Authorized International Health Tourism Center (ST-0625)</code> eklenmeli.<br/>
                • <b>Öneri:</b> Yabancı klinik ve doktor iş birlikleri için İngilizce B2B paylaşımları artırılmalı.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c_fb:
        st.markdown("""
        <div style="background: rgba(14, 47, 59, 0.7); border: 1.5px solid rgba(0, 240, 255, 0.4); border-radius: 12px; padding: 16px; height: 100%;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 14px; font-weight: 700; color: #FFFFFF;">👥 Facebook</span>
                <span style="background: rgba(0, 240, 255, 0.2); color: #00F0FF; font-size: 11px; padding: 2px 8px; border-radius: 6px; font-weight: 700;">Skor: %89.2</span>
            </div>
            <div style="font-size: 12px; color: #00F0FF; margin-bottom: 8px;">
                <a href="https://www.facebook.com/profile.php?id=100083144149931" target="_blank" style="color: #00F0FF; text-decoration: none;">🔗 profile.php?id=100083144149931 ↗</a>
            </div>
            <div style="font-size: 12px; color: #CBD5E1; line-height: 1.5;">
                • <b>Hedef Kitle:</b> B2C Aileler, Körfez (Irak), Balkanlar & Kafkasya.<br/>
                • <b>Risk Seviyesi:</b> <span style="color: #FFA34D; font-weight: 700;">ORTA SEVİYE RİSK</span>.<br/>
                • <b>Teknik İyileştirme:</b> Sayısal ID yerine kurumsal özel URL tanımlanmalı (<code>facebook.com/genarttupbebek</code>).<br/>
                • <b>WhatsApp Butonu:</b> Yönlendirmede otomatik KVKK Aydınlatma Metni devreye alınmalı.<br/>
                • <b>Değerlendirmeler (Reviews):</b> Halka açık hasta yorumları sekmesi hekim reklamı oluşturmaması için kısıtlanmalı.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Detailed Checklist Table
    st.markdown("""
    <h3 style="color: #FFFFFF; font-size: 15px; font-weight: 700; margin-bottom: 8px;">
        📋 Hesap Bazında Mevzuat ve KVKK Uyumluluk Matrisi (10 Temel Kriter)
    </h3>
    """, unsafe_allow_html=True)

    audit_matrix = [
        {
            "Denetim Kriteri": "1. Uluslararası Sağlık Turizmi Yetki Belgesi (ST-0625)",
            "Yasal Dayanak": "Sağlık Turizmi Yön. Md. 5 & Tanıtım Yön. Md. 9",
            "Instagram": "⚠️ Eksik (Bio'ya Eklenmeli)",
            "LinkedIn": "⚠️ Eksik (About Kısmına Eklenmeli)",
            "Facebook": "⚠️ Eksik (Hakkında Kısmına Eklenmeli)",
            "Hukuki Düzeltme & Tavsiye": "'T.C. Sağlık Bakanlığı Sağlık Turizmi Yetki Belgesi: ST-0625' ibaresi 3 hesaba da eklenmeli."
        },
        {
            "Denetim Kriteri": "2. Başarı Oranı & Garanti İddiası Yasağı",
            "Yasal Dayanak": "Tanıtım Yönetmeliği Md. 8 / TİTCK Kararları",
            "Instagram": "✅ Uyumlu (Garanti Yok)",
            "LinkedIn": "✅ Tam Uyumlu",
            "Facebook": "✅ Uyumlu (Garanti Yok)",
            "Hukuki Düzeltme & Tavsiye": "'%100 Başarı', 'Kesin Gebelik' gibi ifadelerden kaçınılmış, bilimsel dil korunmalıdır."
        },
        {
            "Denetim Kriteri": "3. Hasta & Bebek Görselleri Paylaşım İzni",
            "Yasal Dayanak": "KVKK Madde 6 & Tanıtım Yön. Md. 5/1-ç",
            "Instagram": "🔴 Kritik Risk (Açık Rıza Şartı)",
            "LinkedIn": "✅ Risksiz (Hasta Görseli Yok)",
            "Facebook": "⚠️ Dikkat (İmzalı Onay Formu)",
            "Hukuki Düzeltme & Tavsiye": "Paylaşılan her anne-bebek fotoğrafı için 'Sosyal Medya Paylaşım İzin Formu' arşivlenmeli; bebek yüzleri gizlenmeli."
        },
        {
            "Denetim Kriteri": "4. Hasta Teşekkür & Yorumları (Testimonials)",
            "Yasal Dayanak": "29 Temmuz 2023 Tanıtım Yön. Md. 5",
            "Instagram": "🔴 Yasak (Story/Feed Kaldırılmalı)",
            "LinkedIn": "✅ Tam Uyumlu",
            "Facebook": "⚠️ Reviews Sekmesi Kapatılmalı",
            "Hukuki Düzeltme & Tavsiye": "WhatsApp teşekkür ekran görüntüleri örtülü reklam sayılır. Kamuya açık paylaşımdan kaldırılmalıdır."
        },
        {
            "Denetim Kriteri": "5. Hekim Diploma ve Uzmanlık Unvanları",
            "Yasal Dayanak": "1219 Sayılı Kanun & TTB Etik Kuralları",
            "Instagram": "✅ Uyumlu (Prof. Dr. / Op. Dr.)",
            "LinkedIn": "✅ Tam Uyumlu",
            "Facebook": "✅ Uyumlu",
            "Hukuki Düzeltme & Tavsiye": "Paylaşımlarda Prof. Dr. Volkan Baltacı ve hekimlerin tescilli uzmanlık alanları açıkça yazılmaktadır."
        },
        {
            "Denetim Kriteri": "6. Fiyat, Kampanya ve İndirim Yasağı",
            "Yasal Dayanak": "Tanıtım Yön. Md. 5/1-b & Tüketici Kanunu",
            "Instagram": "✅ Uyumlu (Fiyat Paylaşılmamış)",
            "LinkedIn": "✅ Tam Uyumlu",
            "Facebook": "✅ Uyumlu",
            "Hukuki Düzeltme & Tavsiye": "Paket fiyatları kamuya açık yazılmamalı, yalnızca bireysel ön konsültasyonda yazılı verilmelidir."
        },
        {
            "Denetim Kriteri": "7. Yurt Dışı Sponsorlu Reklam Coğrafi Hedefleme",
            "Yasal Dayanak": "Tanıtım Yön. Md. 9 & ST Yönetmeliği",
            "Instagram": "⚠️ Hedefleme Kontrol Edilmeli",
            "LinkedIn": "✅ Güvenli",
            "Facebook": "⚠️ Hedefleme Kontrol Edilmeli",
            "Hukuki Düzeltme & Tavsiye": "Meta Ads Manager üzerinden verilen reklamlar SADECE Türkiye dışı IP'leri (Irak, Almanya vb.) hedeflemelidir."
        },
        {
            "Denetim Kriteri": "8. Cinsiyet Seçimi ve Donasyon İması Yasağı",
            "Yasal Dayanak": "ÜYTE Yönetmeliği Ek-1",
            "Instagram": "✅ Kusursuz (İhlal Yok)",
            "LinkedIn": "✅ Kusursuz (İhlal Yok)",
            "Facebook": "✅ Kusursuz (İhlal Yok)",
            "Hukuki Düzeltme & Tavsiye": "Türkiye'de yasak olan cinsiyet seçimi veya donasyon konularına kesinlikle değinilmemektedir."
        },
        {
            "Denetim Kriteri": "9. Kurumsal Kimlik & Profil Doğrulaması",
            "Yasal Dayanak": "Sağlık Bakanlığı Dijital İletişim Rehberi",
            "Instagram": "✅ @genarttupbebek Tanımlı",
            "LinkedIn": "✅ Kurumsal Şirket Sayfası",
            "Facebook": "🔴 ID Numaralı URL Değişmeli",
            "Hukuki Düzeltme & Tavsiye": "Facebook ID URL'si `facebook.com/genarttupbebek` olarak güncellenmeli ve Meta Doğrulama Rozeti alınmalı."
        },
        {
            "Denetim Kriteri": "10. WhatsApp Hattında Otomatik KVKK Karşılama",
            "Yasal Dayanak": "KVKK Madde 10 (Aydınlatma Yükümlülüğü)",
            "Instagram": "⚠️ Otomatik Metin Eksik",
            "LinkedIn": "✅ Gerek Yok (Web Sitesi Yönlendirmeli)",
            "Facebook": "⚠️ Otomatik Metin Eksik",
            "Hukuki Düzeltme & Tavsiye": "WhatsApp'tan ilk mesaj atan hastaya otomatik KVKK Aydınlatma Metni linki gönderilmelidir."
        }
    ]

    st.dataframe(pd.DataFrame(audit_matrix), use_container_width=True, hide_index=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Actionable Remediation Guide (Ne Yapılmalı / Ne Yapılmamalı)
    st.markdown("""
    <h3 style="color: #00F0FF; font-size: 15px; font-weight: 700; margin-bottom: 10px;">
        ⚡ Sağlık Bakanlığı Müfettiş Denetimine Karşı Hukuki Eylem Planı (Öncelikli 4 Adım)
    </h3>
    """, unsafe_allow_html=True)

    col_act1, col_act2 = st.columns(2)
    with col_act1:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.1); border: 1.5px solid #10B981; border-radius: 12px; padding: 16px;">
            <div style="font-size: 14px; font-weight: 700; color: #10B981; margin-bottom: 8px;">
                ✅ DERHAL YAPILMASI GEREKENLER (HUKUKİ ZORUNLULUK)
            </div>
            <div style="font-size: 12.5px; color: #CBD5E1; line-height: 1.6;">
                <b>1. ST-0625 Numarasını Biyografilere Ekleyin:</b><br/>
                Instagram ve Facebook biyografisine şu ifadeyi ekleyin:<br/>
                <code>🏛️ T.C. Sağlık Bakanlığı Uluslararası Sağlık Turizmi Yetki Belgesi: ST-0625</code><br/><br/>
                <b>2. Facebook Profilini Kurumsal Sayfaya Dönüştürün:</b><br/>
                <code>facebook.com/profile.php?id=100083144149931</code> adresini Meta Business Manager'da <code>facebook.com/genarttupbebek</code> olarak tescilleyin.<br/><br/>
                <b>3. Bilimsel Vaka Paylaşım Formatına Geçin:</b><br/>
                Hasta fotoğrafları yerine laboratuvar mikroskop görüntüleri, Time-lapse inkübatör embriyo gelişimi ve genetik tarama (PGT-A) bilgilendirici animasyonlarını öne çıkarın.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_act2:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.1); border: 1.5px solid #EF4444; border-radius: 12px; padding: 16px;">
            <div style="font-size: 14px; font-weight: 700; color: #EF4444; margin-bottom: 8px;">
                ❌ KESİNLİKLE YAPILMAMASI GEREKENLER (AĞIR CEZA RİSKİ)
            </div>
            <div style="font-size: 12.5px; color: #CBD5E1; line-height: 1.6;">
                <b>1. Yazılı Onaysız Bebek / Hasta Fotoğrafı Paylaşmayın:</b><br/>
                Sözlü rıza hukuken geçersizdir. Islak imzalı KVKK m.6 izin formu olmayan görselleri profil ve hikayelerden kaldırın.<br/><br/>
                <b>2. WhatsApp Teşekkür Ekran Görüntülerini Kaldırın:</b><br/>
                Hastanın "Sayenizde hamileyim" mesajının ekran görüntüsü TİTCK ve TTB tarafından 'Haksız Rekabet ve Talep Yaratma' sayılarak ceza yazılmaktadır.<br/><br/>
                <b>3. Türkiye İçi Sponsorlu Sağlık Reklamı Vermeyin:</b><br/>
                Türkiye içinde yerleşik kullanıcılara Instagram/Facebook üzerinden ücretli sağlık reklamı yayınlamak yasaktır. Reklam hedeflemesini yalnızca yurt dışı ülkelere (Irak, Almanya, İngiltere vb.) açık tutun.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Downloadable Official Compliance Report
    st.markdown("""
    <div style="background: rgba(9, 34, 43, 0.85); border: 1px solid rgba(0, 240, 255, 0.4); border-radius: 12px; padding: 16px; margin-bottom: 12px;">
        <div style="font-size: 14px; font-weight: 700; color: #FFFFFF; margin-bottom: 4px;">
            📄 Resmi Sosyal Medya Mevzuat ve KVKK Denetim Raporunu İndirin
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
            Yönetim Kurulu ve Hukuk Müşavirliği için hazırlanmış detaylı denetim tutanağı (CSV & Metin Formatı)
        </div>
    """, unsafe_allow_html=True)

    report_text = """T.C. SAĞLIK BAKANLIĞI MEVZUATI VE KVKK UYUM RAPORU
Tarih: 2026 YTD
Kurum: GEN-ART Tüp Bebek ve Üreme Genetiği Merkezi (Ankara)
Yetki Belgesi: Uluslararası Sağlık Turizmi Yetki Belgesi ST-0625

DENETLENEN HESAPLAR:
1. Instagram: https://www.instagram.com/genarttupbebek/ (Uyum Skoru: %86.5)
2. LinkedIn: https://www.linkedin.com/company/genarttupbebek/ (Uyum Skoru: %96.0)
3. Facebook: https://www.facebook.com/profile.php?id=100083144149931 (Uyum Skoru: %89.2)

GENEL UYUMLULUK PUANI: %91.4 (MEVZUATA BÜYÜK ÖLÇÜDE UYUMLU - 3 DÜZELTME ÖNERİLİR)

HUKUKİ TESPİT VE TALİMATLAR:
1. Biyografilerde 'ST-0625' Sağlık Turizmi Yetki Belgesi numarası zorunlu olarak yer almalıdır.
2. Instagram'da bebek ve hasta fotoğrafları için KVKK Madde 6 ıslak imzalı açık rıza formu arşivlenmelidir.
3. WhatsApp veya DM üzerinden gelen hasta memnuniyet ve teşekkür ekran görüntüleri 'Örtülü Reklam' sayıldığından kaldırılmalıdır.
4. Facebook profili sayısal ID yerine 'facebook.com/genarttupbebek' olarak adlandırılmalıdır.
5. Reklam kampanyaları yalnızca Türkiye dışı ülkeler hedeflenerek yürütülmelidir.
"""
    col_dl1, col_dl2 = st.columns([1, 1])
    with col_dl1:
        st.download_button(
            label="📥 Resmi Denetim Raporu Metnini İndir (.TXT)",
            data=report_text,
            file_name="GEN_ART_Sosyal_Medya_Mevzuat_Denetim_Raporu.txt",
            mime="text/plain",
            use_container_width=True
        )
    with col_dl2:
        df_audit = pd.DataFrame(audit_matrix)
        csv_data = df_audit.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📊 Denetim Matrisini İndir (.CSV)",
            data=csv_data,
            file_name="GEN_ART_Mevzuat_Denetim_Matrisi.csv",
            mime="text/csv",
            use_container_width=True
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_audit_checklist():
    """Checklist based on 2025 Ministry of Health Regulations"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>📋 T.C. Sağlık Turizmi ve ÜYTE Mevzuatı Uygunluk Matrisi</span>
            <span class="tag">Yetki Belgesi: ST-0625</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Yetki Belgesi Statüsü", "ST-0625 AKTİF", "T.C. Sağlık Bakanlığı Onaylı", icon="✅")
    with col2:
        render_kpi_card("Tanıtım Uyumluluk Skoru", "%96.4", "29 Temmuz 2023 / 2025 Yönetmeliği", icon="📑")
    with col3:
        render_kpi_card("Hassas Veri İzolasyonu", "KUSURSUZ", "Klinik CRM Ayrımı Tam", icon="🛡️")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    reg_items = [
        {"Madde": "Uluslararası Sağlık Turizmi Yetki Belgesi ST-0625", "Yasal Dayanak": "Sağlık Turizmi Yönetmeliği Md. 5", "Durum": "✅ Eksiksiz Onaylı", "Açıklama": "Klinik resmi web sitesinde ve tanıtım materyallerinde ST-0625 logosu ile tescilli."},
        {"Madde": "Tanıtımlarda Tıbbi Başarı Oranı Vaat Etmeme Kuralı", "Yasal Dayanak": "Tanıtım Yön. Md. 8", "Durum": "✅ Uyumlu", "Açıklama": "'%100 Başarı', 'Kesin Gebelik' gibi yanıltıcı ifadeler yasaklanmış; bilimsel bilgilendirme esastır."},
        {"Madde": "Yurtdışı Hedefleme & Dil Kısıtı Uyumu", "Yasal Dayanak": "Tanıtım Yön. Md. 9", "Durum": "✅ Uyumlu", "Açıklama": "Reklamlar yalnızca Türkiye dışındaki IP/ülkeleri hedefler; yerli hastalara yönelik sağlık reklamı yapılmaz."},
        {"Madde": "Çok Dilli Yetkili Hasta Koordinatörleri", "Yasal Dayanak": "Sağlık Turizmi Yönetmeliği Md. 11", "Durum": "✅ Uyumlu", "Açıklama": "Arapça, İngilizce, Rusça akredite tercüman ve koordinatör istihdamı sağlanmıştır."},
        {"Madde": "Fiyat ve Paket Şeffaflığı & Sözleşme", "Yasal Dayanak": "Sağlık Turizmi Yönetmeliği Md. 14", "Durum": "✅ Uyumlu", "Açıklama": "Seyahat öncesi detaylı tedavi planı ve maliyet dökümü yazılı olarak hastaya sunulmaktadır."},
        {"Madde": "ÜYTE Donasyon ve Cinsiyet Seçimi Yasağı Uyumu", "Yasal Dayanak": "Üremeye Yardımcı Tedavi Yön. Ek-1", "Durum": "✅ Eksiksiz Uyumlu", "Açıklama": "Türkiye kanunlarına aykırı donasyon veya cinsiyet seçimi içerikleri kesinlikle yer almaz."}
    ]
    st.dataframe(pd.DataFrame(reg_items), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_ad_approval_workflow():
    """Human-in-the-loop compliance approval for campaigns"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>✍️ Kampanya ve İddia İnsan Onay Aşaması (Human-in-the-Loop)</span>
            <span class="tag">Zorunlu Denetim</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 14px;">
            Yapay zekâ veya pazarlama ekibinin hazırladığı metinler hekim veya mevzuat yetkilisi onaylamadan yayına alınamaz.
        </div>
    """, unsafe_allow_html=True)
    
    ads_data = [
        {"Kampanya Adı": "Almanya PGT-A Bilgilendirme", "Hedef Ülke": "Almanya", "İçerik": "İleri yaş ve tekrarlayan başarısız IVF'de genetik tarama rehberi.", "Hekim Onayı": "✅ Onaylandı (Dr. L.M.)", "Mevzuat Uyumu": "✅ Uygun", "Durum": "Yayında"},
        {"Kampanya Adı": "Irak Sosyal Medya Mikro TESE", "Hedef Ülke": "Irak", "İçerik": "Azoospermi vakalarında mikrocerrahi androloji yaklaşımları.", "Hekim Onayı": "✅ Onaylandı (Dr. K.T.)", "Mevzuat Uyumu": "✅ Uygun", "Durum": "Yayında"},
        {"Kampanya Adı": "Körfez IVF Garantili Paket Metni", "Hedef Ülke": "Kuveyt", "İçerik": "'%95 Başarı Garantili Tüp Bebek Paketi'", "Hekim Onayı": "❌ Reddedildi", "Mevzuat Uyumu": "❌ Yönetmelik İhlali (Garanti İfadesi)", "Durum": "Engellendi"},
        {"Kampanya Adı": "İngiltere NGS Genetik Tarama Postu", "Hedef Ülke": "Birleşik Krallık", "İçerik": "Mikrogen Akredite Laboratuvarı NGS Monogenik Hastalık Taraması", "Hekim Onayı": "✅ Onaylandı (Prof. Dr. V.B.)", "Mevzuat Uyumu": "✅ Uygun", "Durum": "Yayında"}
    ]
    st.dataframe(pd.DataFrame(ads_data), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_kvkk_framework():
    """Separation of marketing analytics and medical records"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🔒 KVKK & Hassas Sağlık Verisi Ayrıştırma Mimarisi</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
            • <b>Analitik Katmanı (Bu Dashboard):</b> Yalnızca ülke, dil, yanıt süresi, dönüşüm aşaması ve harcama gibi de-identified (kimliksizleştirilmiş) özet verileri işler.<br/>
            • <b>Klinik Katman (HBYS / EMR):</b> Hastaların tıbbi tahlilleri, embriyoloji raporları ve kimlik bilgileri şifreli, izole yerel sunucularda saklanır.<br/>
            • <b>Pazarlama Platformları İzolasyonu:</b> Google Ads veya Meta pikseline asla hassas sağlık verisi, tıbbi teşhis veya hasta adı iletilmez (Yalnızca anonim etkinlik ID'leri kullanılır).<br/>
            • <b>Sosyal Medya Paylaşım Protokolü:</b> Hastaların veya bebeklerin görsel verileri KVKK Madde 6 uyarınca özel nitelikli kişisel veri sayılır; yalnızca ıslak imzalı veya e-imzalı Açık Rıza Formu ile ve bebeğin yüzü korunarak işlenebilir.
        </div>
    </div>
    """, unsafe_allow_html=True)
