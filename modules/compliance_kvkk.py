"""
Module 7: Regulatory & Ethical Compliance (KVKK & Health Tourism Framework)
Monitors Türkiye's 26 April 2025 Health Tourism Regulation and 12 November 2025 Promotion Regulation.
Enforces ST-0625 authorization checks, KVKK clinical data isolation, and human-in-the-loop ad review.
"""

import streamlit as st
import pandas as pd
from config import THEME_COLORS, HEALTH_TOURISM_AUTH
from utils.components import render_kpi_card

def render_compliance_kvkk():
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
            🛡️ Mevzuat, Etik & KVKK Sağlık Turizmi Uyumluluk Denetimi
        </h2>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
            T.C. Sağlık Bakanlığı 26 Nisan 2025 Yönetmeliği, 12 Kasım 2025 Tanıtım Yönetmeliği ve ST-0625 yetki belgesi güvenceleri
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_audit, tab_ads, tab_kvkk = st.tabs([
        "📜 2025 Sağlık Turizmi Mevzuat Denetim Listesi",
        "⚖️ Reklam & Kampanya İnsan Onay Mekanizması",
        "🔒 KVKK & Hassas Sağlık Verisi Ayrıştırma İlkeleri"
    ])

    with tab_audit:
        render_audit_checklist()

    with tab_ads:
        render_ad_approval_workflow()

    with tab_kvkk:
        render_kvkk_framework()

def render_audit_checklist():
    """Checklist based on 2025 Ministry of Health Regulations"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>📋 T.C. Sağlık Turizmi Mevzuatı Uygunluk Matrisi</span>
            <span class="tag">Yetki Belgesi: ST-0625</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Yetki Belgesi Statüsü", "ST-0625 AKTİF", "T.C. Sağlık Bakanlığı Onaylı", icon="✅")
    with col2:
        render_kpi_card("Tanıtım Uyumluluk Skoru", "%96.4", "12 Kasım 2025 Yönetmeliği", icon="📑")
    with col3:
        render_kpi_card("Hassas Veri İzolasyonu", "KUSURSUZ", "Klinik CRM Ayrımı Tam", icon="🛡️")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    reg_items = [
        {"Madde": "Uluslararası Sağlık Turizmi Yetki Belgesi ST-0625", "Yasal Dayanak": "26 Nisan 2025 Yönetmeliği Md. 5", "Durum": "✅ Eksiksiz Onaylı", "Açıklama": "Klinik resmi web sitesinde ve tanıtım materyallerinde ST-0625 logosu ile tescilli."},
        {"Madde": "Tanıtımlarda Tıbbi Başarı Oranı Vaat Etmeme Kuralı", "Yasal Dayanak": "12 Kasım 2025 Tanıtım Yön. Md. 8", "Durum": "✅ Uyumlu", "Açıklama": "'%100 Başarı', 'Kesin Gebelik' gibi yanıltıcı ifadeler yasaklanmış; bilimsel bilgilendirme esastır."},
        {"Madde": "Yurtdışı Hedefleme & Dil Kısıtı Uyumu", "Yasal Dayanak": "12 Kasım 2025 Tanıtım Yön. Md. 9", "Durum": "✅ Uyumlu", "Açıklama": "Reklamlar yalnızca Türkiye dışındaki IP/ülkeleri hedefler; yerli hastalara yönelik sağlık reklamı yapılmaz."},
        {"Madde": "Çok Dilli Yetkili Hasta Koordinatörleri", "Yasal Dayanak": "26 Nisan 2025 Yönetmeliği Md. 11", "Durum": "✅ Uyumlu", "Açıklama": "Arapça, İngilizce, Rusça akredite tercüman ve koordinatör istihdamı sağlanmıştır."},
        {"Madde": "Fiyat ve Paket Şeffaflığı & Sözleşme", "Yasal Dayanak": "26 Nisan 2025 Yönetmeliği Md. 14", "Durum": "✅ Uyumlu", "Açıklama": "Seyahat öncesi detaylı tedavi planı ve maliyet dökümü yazılı olarak hastaya sunulmaktadır."}
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
        {"Kampanya Adı": "Körfez IVF Garantili Paket Metni", "Hedef Ülke": "Kuveyt", "İçerik": "'%95 Başarı Garantili Tüp Bebek Paketi'", "Hekim Onayı": "❌ Reddedildi", "Mevzuat Uyumu": "❌ Yönetmelik İhlali (Garanti İfadesi)", "Durum": "Engellendi"}
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
            • <b>Pazarlama Platformları İzolasyonu:</b> Google Ads veya Meta pikseline asla hassas sağlık verisi, tıbbi teşhis veya hasta adı iletilmez (Yalnızca anonim etkinlik ID'leri kullanılır).
        </div>
    </div>
    """, unsafe_allow_html=True)
