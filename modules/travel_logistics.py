"""
Module 6: International Patient Travel & Treatment Coordination
Incorporates official clinical protocols directly from 'IVF SÜREÇLERİ.xlsx':
1. Standart IVF Protokolü (PGT'siz & Taze Transfer - 17 Gün)
2. IVF + PGT (Embriyo Dondurmalı - 12 Gün + 1-2 Ay Sonra 14-15 Gün)
3. Express PGT-A NGS (Taze Transfer - 17 Gün Kesintisiz Kalış)
4. Frozen Embryo Transfer (FET - 14-15 Gün)
Includes an interactive Travel & Treatment Itinerary Calculator for coordinators.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from config import THEME_COLORS, COUNTRY_COORDINATES, IVF_TREATMENT_PROTOCOLS
from utils.components import render_kpi_card

def render_travel_logistics(mcda_df, leads_df, protocols=None):
    if protocols is None:
        protocols = IVF_TREATMENT_PROTOCOLS

    st.markdown("""
<div style="margin-bottom: 12px;">
    <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
        ✈️ Uluslararası Hasta Seyahat, Vize & Tedavi Lojistiği Koordinasyonu
    </h2>
    <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
        GEN-ART klinik protokolleri (IVF SÜREÇLERİ.xlsx), Ankara Esenboğa (ESB) bağlantıları ve interaktif seyahat takvimi
    </div>
</div>
""", unsafe_allow_html=True)

    tab_protocols, tab_calc, tab_visas, tab_flights = st.tabs([
        "🧬 Resmi Tedavi Protokolleri (Excel Entegre)",
        "🗓️ İnteraktif Hasta Seyahat & Kalış Hesaplayıcı",
        "🛂 Ülke Vize & Giriş Prosedürleri",
        "🛫 Ankara Ulaşım Hatları & ESB"
    ])

    with tab_protocols:
        render_protocol_cards(protocols)

    with tab_calc:
        render_itinerary_calculator(protocols)

    with tab_visas:
        render_visa_matrix(mcda_df)

    with tab_flights:
        render_flight_corridors(mcda_df)

def render_protocol_cards(protocols):
    """Renders the 4 official clinical IVF treatment protocols from IVF SÜREÇLERİ.xlsx"""
    st.markdown("""
<div class="section-card">
    <div class="section-header">
        <span>🧬 GEN-ART Klinik Tedavi Protokolleri ve Kalış Süreleri</span>
        <span class="tag">IVF SÜREÇLERİ.xlsx Entegrasyonu</span>
    </div>
    <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 16px;">
        Kliniğin yurtdışı hastalarına uyguladığı 4 ana tedavi süreci, kalış süreleri ve operasyonel gereksinimler:
    </div>
</div>
""", unsafe_allow_html=True)

    p_cols = st.columns(2)
    
    for idx, proto in enumerate(protocols):
        col = p_cols[idx % 2]
        with col:
            visits_badge = "1 Ziyaret (Tek Seferde)" if proto["visits"] == 1 else "⚠️ 2 Ayrı Ziyaret (1-2 Ay Arayla)"
            badge_color = "#10B981" if proto["visits"] == 1 else "#F59E0B"
            raw_desc = proto.get('excel_raw_description', proto['description'])
            
            card_html = (
                f'<div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 12px; padding: 18px; margin-bottom: 16px;">'
                f'<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">'
                f'<div style="font-size: 15px; font-weight: 700; color: #FFFFFF;">{proto["name"]}</div>'
                f'<span style="font-size: 10px; font-weight: 700; background: rgba(0, 240, 255, 0.15); color: {badge_color}; border: 1px solid {badge_color}; padding: 3px 8px; border-radius: 6px;">{visits_badge}</span>'
                f'</div>'
                f'<div style="font-size: 11px; color: #00F0FF; font-family: monospace; margin-bottom: 8px;">📁 Orijinal Metin: "{raw_desc}"</div>'
                f'<div style="font-size: 12px; color: #E2E8F0; line-height: 1.5; margin-bottom: 10px;">'
                f'• <b>Tedavi Başlangıcı:</b> {proto["start_day"]}<br/>'
                f'• <b>Ankara\'da Kalış Süresi:</b> <span style="color: #00F0FF; font-weight: 700;">{proto["stay_days"]} Gün</span><br/>'
                f'• <b>Hedef Hasta Profili:</b> {proto["target_group"]}<br/>'
                f'• <b>Vize Tavsiyesi:</b> {proto["visa_req"]}'
                f'</div>'
                f'<div style="font-size: 11px; background: rgba(0, 240, 255, 0.06); padding: 8px 10px; border-radius: 6px; color: #94A3B8;">'
                f'💡 <b>Koordinatör Notu:</b> {proto["description"]}'
                f'</div>'
                f'</div>'
            )
            st.markdown(card_html, unsafe_allow_html=True)

def render_itinerary_calculator(protocols):
    """Interactive travel date calculator based on patient's menstrual period and protocol"""
    st.markdown("""
<div class="section-card">
    <div class="section-header">
        <span>🧮 Uluslararası Hasta Seyahat & Tedavi Takvimi Hesaplayıcı</span>
        <span class="tag">Koordinatör Planlama Aracı</span>
    </div>
    <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 16px;">
        Hastanın beklenen adet kanaması tarihini ve uygulanacak protokolü girerek Ankara varış, klinik başlama, kalış ve dönüş tarihlerini otomatik hesaplayın.
    </div>
</div>
""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        patient_country = st.selectbox("Hastanın Geldiği Ülke:", list(COUNTRY_COORDINATES.keys()), index=0)
    with col2:
        proto_names = [p["name"] for p in protocols]
        chosen_proto_name = st.selectbox("Uygulanacak Tedavi Protokolü:", proto_names, index=2) # Default to Express NGS
    with col3:
        period_start = st.date_input("Beklenen Adet Kanaması Başlangıç Tarihi:", date.today() + timedelta(days=14))
        
    selected_proto = next(p for p in protocols if p["name"] == chosen_proto_name)
    country_info = COUNTRY_COORDINATES[patient_country]

    # Calculations:
    clinic_start_date = period_start + timedelta(days=2) # Day 3 of cycle
    arrival_date = clinic_start_date - timedelta(days=1)
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    if selected_proto["visits"] == 1:
        departure_date = clinic_start_date + timedelta(days=selected_proto["stay_days"])
        total_stay = (departure_date - arrival_date).days
        
        c_r1, c_r2, c_r3, c_r4 = st.columns(4)
        with c_r1:
            render_kpi_card("Ankara'ya Varış", arrival_date.strftime("%d.%m.%Y"), "Esenboğa Havalimanı Karşılama", icon="🛬")
        with c_r2:
            render_kpi_card("Klinik Tedavi Başlangıcı", clinic_start_date.strftime("%d.%m.%Y"), "Adetin 2-3. Günü / Stimülasyon", icon="🧬")
        with c_r3:
            render_kpi_card("Planlanan Dönüş", departure_date.strftime("%d.%m.%Y"), "Embriyo Transferi Sonrası", icon="🛫")
        with c_r4:
            render_kpi_card("Toplam Kalış", f"{total_stay} Gün", selected_proto["visa_req"], icon="🏨", is_highlight=True)
            
        alert_html = (
            f'<div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 12px 16px; border-radius: 6px; font-size: 13px; color: #CBD5E1; margin-top: 14px;">'
            f'✅ <b>Tek Seferde Tamamlanan Protokol:</b> Hasta <b>{arrival_date.strftime("%d %B %Y")}</b> tarihinde Ankara\'ya gelip <b>{departure_date.strftime("%d %B %Y")}</b> tarihinde ülkesine dönebilir. '
            f'Tek girişli 30 günlük standart vize ve {total_stay} gecelik otel rezervasyonu gereklidir.'
            f'</div>'
        )
        st.markdown(alert_html, unsafe_allow_html=True)
        
    else: # 2-visit protocol (Freeze & FET later)
        dep1 = clinic_start_date + timedelta(days=12)
        phase2_start = dep1 + timedelta(days=45)
        phase2_clinic = phase2_start + timedelta(days=2)
        dep2 = phase2_clinic + timedelta(days=15)
        
        c_r1, c_r2, c_r3, c_r4 = st.columns(4)
        with c_r1:
            render_kpi_card("1. Ziyaret Varış", arrival_date.strftime("%d.%m.%Y"), "Stimülasyon & OPU & Biyopsi", icon="1️⃣")
        with c_r2:
            render_kpi_card("1. Ziyaret Dönüş", dep1.strftime("%d.%m.%Y"), "Embriyolar Donduruldu (12 Gün)", icon="🛫")
        with c_r3:
            render_kpi_card("2. Ziyaret Dönüşü", phase2_clinic.strftime("%d.%m.%Y"), "1-2 Ay Sonra FET Hazırlığı", icon="2️⃣")
        with c_r4:
            render_kpi_card("Nihai Transfer Dönüş", dep2.strftime("%d.%m.%Y"), "FET Transferi (15 Gün)", icon="👶", is_highlight=True)
            
        alert2_html = (
            f'<div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #F59E0B; padding: 12px 16px; border-radius: 6px; font-size: 13px; color: #CBD5E1; margin-top: 14px;">'
            f'⚠️ <b>2 Aşamalı Seyahat Uyarısı:</b> Bu protokol <b>2 ayrı Ankara seyahati</b> gerektirir. '
            f'İlk ziyaret <b>{arrival_date.strftime("%d.%m.%Y")} - {dep1.strftime("%d.%m.%Y")}</b> (12 gün); ikinci ziyaret yaklaşık <b>{phase2_clinic.strftime("%d.%m.%Y")} - {dep2.strftime("%d.%m.%Y")}</b> (15 gün) olacaktır. '
            f'Hastaya <b>Çoklu Girişli (Multiple Entry) medikal vize</b> düzenlenmeli ve iki ayrı uçuş bileti bütçesi bildirilmelidir.'
            f'</div>'
        )
        st.markdown(alert2_html, unsafe_allow_html=True)

def render_visa_matrix(mcda_df):
    """Visa categories and health tourism facilitation status"""
    st.markdown("""
<div class="section-card">
    <div class="section-header">
        <span>🛂 Hedef Ülke Vize Rejimi & Medikal Vize Kolaylığı</span>
        <span class="tag">USHAŞ & Dışişleri Entegrasyonu</span>
    </div>
    <div style="font-size: 13px; color: #CBD5E1; margin-bottom: 14px;">
        Hastaların tedaviye gelişini hızlandırmak için vize türleri kategorize edilmiştir:
    </div>
</div>
""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Vizesiz / Kimlikle Giriş", "6 Ülke", "Azerbaycan, Gürcistan, Sırbistan, Bosna...", icon="🟢")
    with col2:
        render_kpi_card("Kolay e-Vize / 90 Gün", "8 Ülke", "Kuveyt, Katar, BAE, Ürdün, Almanya, İngiltere...", icon="🔵")
    with col3:
        render_kpi_card("Etiket / Konsolosluk Vizesi", "3 Ülke", "Irak, Libya, Özbekistan (Medikal Destek Şart)", icon="🟠")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    visa_table = mcda_df[["country", "region", "visa_type", "travel_score"]].copy()
    visa_table.rename(columns={
        "country": "Ülke", "region": "Bölge", "visa_type": "Vize Rejimi / Şartlar", "travel_score": "Erişilebilirlik Skoru"
    }, inplace=True)
    
    st.dataframe(visa_table, use_container_width=True, hide_index=True)

def render_flight_corridors(mcda_df):
    """Flight connections to Ankara Esenboğa Airport (ESB)"""
    st.markdown("""
<div class="section-card">
    <div class="section-header">
        <span>🛬 Ankara Esenboğa (ESB) Uçuş Mesafeleri & Direkt Seferler</span>
    </div>
    <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 14px;">
        Tüp bebek ve genetik tedavilerde zamanlama kritik olduğundan, direkt uçuş imkanları hasta tercihinde belirleyici rol oynar.
    </div>
</div>
""", unsafe_allow_html=True)
    
    flight_df = mcda_df[["country", "flight_hrs", "direct_flight", "avg_stay_days"]].copy()
    flight_df["direct_flight"] = flight_df["direct_flight"].apply(lambda x: "✅ Direkt Uçuş Var" if x else "⚠️ Aktarmalı (IST/SAW)")
    flight_df["flight_hrs"] = flight_df["flight_hrs"].apply(lambda x: f"{x:.1f} Saat")
    flight_df["avg_stay_days"] = flight_df["avg_stay_days"].apply(lambda x: f"{x} Gün")
    
    flight_df.rename(columns={
        "country": "Kaynak Ülke", "flight_hrs": "Uçuş Süresi", "direct_flight": "Ankara Sefer Durumu", "avg_stay_days": "Önerilen Kalış Süresi"
    }, inplace=True)
    
    st.dataframe(flight_df, use_container_width=True, hide_index=True)
