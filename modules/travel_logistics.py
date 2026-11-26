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
from data.travel_data_loader import get_full_travel_dataframe, get_daily_esb_flight_scan

def render_html(html_str):
    """Renders HTML safely by stripping all leading whitespace from each line and removing blank lines to prevent markdown code block formatting"""
    lines = [line.strip() for line in html_str.strip().split("\n") if line.strip()]
    cleaned = "\n".join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def render_travel_logistics(mcda_df, leads_df, protocols=None):
    if protocols is None:
        protocols = IVF_TREATMENT_PROTOCOLS

    full_travel_df = get_full_travel_dataframe(leads_df)

    st.markdown("""
<div style="margin-bottom: 12px;">
    <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
        ✈️ Uluslararası Hasta Seyahat, Vize & Tedavi Lojistiği Koordinasyonu
    </h2>
    <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
        GEN-ART klinik protokolleri (IVF SÜREÇLERİ.xlsx), tüm 59 kaynak ülke güncel vize kuralları (mfa.gov.tr) ve günlük canlı Ankara Esenboğa (ESB) uçuş taraması
    </div>
</div>
""", unsafe_allow_html=True)

    tab_protocols, tab_tests, tab_calc, tab_visas, tab_flights = st.tabs([
        "🧬 Resmi Tedavi Protokolleri (Excel Entegre)",
        "🩺 Gelmeden Önce İstenen Ön Testler (Excel Entegre)",
        "🗓️ İnteraktif Hasta Seyahat & Kalış Hesaplayıcı",
        "🛂 Tüm Ülkeler Vize & Giriş (59 Ülke)",
        "🛫 Ankara Ulaşım Hatları & Günlük ESB Tarama"
    ])

    with tab_protocols:
        render_protocol_cards(protocols)

    with tab_tests:
        render_prearrival_tests()

    with tab_calc:
        render_itinerary_calculator(protocols)

    with tab_visas:
        render_visa_matrix(full_travel_df)

    with tab_flights:
        render_flight_corridors(full_travel_df)

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
            
            card_html = (
                f'<div style="background: rgba(14, 47, 59, 0.75); border: 1px solid rgba(0, 240, 255, 0.25); border-radius: 12px; padding: 18px; margin-bottom: 16px; min-height: 280px; display: flex; flex-direction: column; justify-content: space-between;">'
                f'<div>'
                f'<div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 10px;">'
                f'<div style="font-size: 15px; font-weight: 700; color: #FFFFFF; line-height: 1.3;">{proto["name"]}</div>'
                f'<span style="font-size: 10px; font-weight: 700; background: rgba(0, 240, 255, 0.15); color: {badge_color}; border: 1px solid {badge_color}; padding: 3px 8px; border-radius: 6px; white-space: nowrap; margin-left: 6px;">{visits_badge}</span>'
                f'</div>'
                f'<div style="font-size: 12px; color: #E2E8F0; line-height: 1.6; margin-bottom: 12px;">'
                f'• <b>Tedavi Başlangıcı:</b> {proto["start_day"]}<br/>'
                f'• <b>Ankara\'da Kalış Süresi:</b> <span style="color: #00F0FF; font-weight: 700;">{proto["stay_days"]} Gün</span><br/>'
                f'• <b>Hedef Hasta Profili:</b> {proto["target_group"]}<br/>'
                f'• <b>Vize Tavsiyesi:</b> {proto["visa_req"]}'
                f'</div>'
                f'</div>'
                f'<div>'
                f'<div style="font-size: 11px; background: rgba(0, 240, 255, 0.08); border-left: 3px solid #00F0FF; padding: 6px 10px; border-radius: 4px; color: #94A3B8; margin-bottom: 8px;">'
                f'💡 <b>Koordinatör Notu:</b> {proto["description"]}'
                f'</div>'
                f'<div style="font-size: 10px; background: rgba(245, 130, 31, 0.12); color: #F5821F; padding: 4px 8px; border-radius: 4px; font-weight: 600;">'
                f'📋 Zorunlu Ön Tetkik: Kadın Hormon/Seroloji + Erkek Spermiogram (yurtdışı gelmeden test.xlsx)'
                f'</div>'
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

def render_visa_matrix(travel_df):
    """Comprehensive visa matrix for ALL 59 countries verified against 2025-2026 mfa.gov.tr rules"""
    render_html("""
<div class="section-card">
    <div class="section-header">
        <span>🛂 Tüm Kaynak Ülkeler Vize Rejimi &amp; Medikal Vize Kolaylığı (59 Ülke)</span>
        <span class="tag">mfa.gov.tr &amp; USHAŞ 2025-2026 Güncel</span>
    </div>
    <div style="font-size: 13px; color: #CBD5E1; margin-bottom: 14px;">
        T.C. Dışişleri Bakanlığı (<b>mfa.gov.tr</b>) 2025-2026 güncel mevzuatına göre <code>yabancilar4.xlsx</code> dosyasındaki <b>tüm 59 kaynak ülkenin</b> vize muafiyeti (Kanada/Avustralya/Umman güncel muafiyetleri, ABD e-Vize/Sınır Vizesi, Irak/Libya/Cezayir yaş şartları dahil) ve USHAŞ ST-0625 kolaylıkları:
    </div>
</div>
""")

    kimlik_cnt = len(travel_df[travel_df["visa_cat"] == "Vizesiz & Kimlikle"])
    pasaport_cnt = len(travel_df[travel_df["visa_cat"] == "Vizesiz (Pasaportla)"])
    total_vizesiz = kimlik_cnt + pasaport_cnt
    evize_cnt = len(travel_df[travel_df["visa_cat"] == "e-Vize / Kapı Vizesi"])
    ushas_cnt = len(travel_df[travel_df["visa_cat"].str.contains("USHAŞ|Konsolosluk", case=False, na=False)])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Vizesiz & Kimlikle", f"{total_vizesiz} Ülke", f"{kimlik_cnt} Kimlikle · {pasaport_cnt} Pasaportla (Kanada/Avustralya/Umman dahil)", icon="🟢", is_highlight=True)
    with col2:
        render_kpi_card("e-Vize / Kapı Vizesi", f"{evize_cnt} Ülke", "ABD, Mısır, Güney Afrika (evisa.gov.tr)", icon="🔵")
    with col3:
        render_kpi_card("USHAŞ & Konsolosluk", f"{ushas_cnt} Ülke", "Irak, Libya, Cezayir, Suriye, Somali, Pakistan, Nijerya...", icon="🟠")
    with col4:
        render_kpi_card("Pasaport Geçerlilik Şartı", "Min. +60 Gün", "Vize/Muafiyet bitiminden min. 60 gün (Öneri: 6 Ay)", icon="📘")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    vf_c1, vf_c2 = st.columns([1.2, 1.8])
    with vf_c1:
        visa_cats = ["Tüm Kategoriler (59 Ülke)"] + sorted(travel_df["visa_cat"].unique().tolist())
        sel_vcat = st.selectbox("Vize Kategorisine Göre Filtrele:", visa_cats)
    with vf_c2:
        v_search = st.text_input("🔍 Ülke veya Vize Kuralı Ara:", "", placeholder="Örn: Canada, Oman, USA, Iraq, Kimlikle...")

    v_view = travel_df.copy()
    if sel_vcat != "Tüm Kategoriler (59 Ülke)":
        v_view = v_view[v_view["visa_cat"] == sel_vcat]
    if v_search.strip():
        vs = v_search.strip().lower()
        v_view = v_view[
            v_view["country"].str.lower().str.contains(vs, na=False) |
            v_view["visa_type"].str.lower().str.contains(vs, na=False) |
            v_view["entry_doc"].str.lower().str.contains(vs, na=False)
        ]

    visa_table = v_view[["country", "excel_patients", "region", "visa_cat", "visa_type", "entry_doc", "medical_visa_support"]].rename(columns={
        "country": "Ülke",
        "excel_patients": "Vaka (Excel)",
        "region": "Bölge",
        "visa_cat": "Kategori",
        "visa_type": "Resmi Vize Rejimi (mfa.gov.tr)",
        "entry_doc": "Giriş Belgesi / Şartlar",
        "medical_visa_support": "Medikal Vize Desteği (ST-0625 / USHAŞ)"
    })

    st.dataframe(visa_table, use_container_width=True, height=430, hide_index=True)

def render_flight_corridors(travel_df):
    """Flight connections to Ankara Esenboğa Airport (ESB) with Daily Auto-Scan & 2026-2027 Expansion Updates"""
    # Auto-run daily scan if new calendar day, or refresh on button click
    if "force_esb_scan" not in st.session_state:
        st.session_state["force_esb_scan"] = False

    scan_data = get_daily_esb_flight_scan(force_refresh=st.session_state["force_esb_scan"])
    st.session_state["force_esb_scan"] = False

    render_html(f"""
<div class="section-card">
    <div class="section-header">
        <span>🛫 Ankara Esenboğa (ESB) Günlük Canlı Uçuş Taraması &amp; 59 Ülke Bağlantıları</span>
        <span class="tag">🔄 Günlük Otomatik Tarama Aktif · Son Kontrol: {scan_data.get('last_scan_timestamp', '')}</span>
    </div>
    <div style="font-size: 13px; color: #CBD5E1; line-height: 1.55; margin-bottom: 8px;">
        Ankara Esenboğa (ESB) merkezli AJet, Pegasus, SunExpress, THY ve yabancı taşıyıcıların <b>59 kaynak ülke</b> uçuş ağları her gün otomatik taranarak güncel tutulur ({scan_data.get('scan_status', '')}).
    </div>
</div>
""")

    btn_c1, btn_c2 = st.columns([1.4, 2.6])
    with btn_c1:
        if st.button("🔄 Ankara ESB Uçuş & Haber Taramasını Şimdi Yenile", use_container_width=True):
            st.session_state["force_esb_scan"] = True
            st.rerun()
    with btn_c2:
        st.info(f"📡 **Son Tarama Zamanı:** `{scan_data.get('last_scan_timestamp')}` — Yeni güne geçildiğinde sistem Esenboğa yeni hat haberlerini otomatik tekrar tarar.")

    # Confirmed 2026-2027 Ankara Esenboga Expansion News Box
    with st.expander("📰 TEYİT EDİLDİ: 2026 - 2027 Yeni Yıl Ankara (ESB) Direkt Uçuş Artışları & Canlı Havacılık Akışı", expanded=True):
        for upd in scan_data.get("verified_2026_2027_updates", []):
            render_html(f"""
            <div style="background: rgba(9, 34, 43, 0.75); border-left: 3px solid #00F0FF; padding: 10px 14px; border-radius: 6px; margin-bottom: 8px; font-size: 12.5px; color: #E2E8F0; line-height: 1.55;">
                <b style="color: #00F0FF;">✓ {upd['carrier']}:</b> {upd['summary']}
            </div>
            """)

        headlines = scan_data.get("live_headlines", [])
        if headlines:
            st.markdown("<div style='font-size: 12.5px; font-weight: 700; color: #F5821F; margin-top: 10px; margin-bottom: 6px;'>📡 Canlı Tarama ile Yakalanan Güncel Esenboğa / AJet Duyuru Başlıkları:</div>", unsafe_allow_html=True)
            for hl in headlines:
                st.markdown(f"- [{hl['title']}]({hl['link']}) *({hl['pub_date'][:16]})*")

    direct_cnt = len(travel_df[travel_df["direct_flight"] == True])
    connecting_cnt = len(travel_df[travel_df["direct_flight"] == False])
    avg_direct_hrs = travel_df[travel_df["direct_flight"] == True]["flight_hrs"].mean()

    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Ankara ESB Direkt Uçuş", f"{direct_cnt} Ülke", "Almanya, Irak, Bakü, Londra, Paris, Viyana, Dubai, Taşkent, Saraybosna...", icon="🛫", is_highlight=True)
    with col2:
        render_kpi_card("İstanbul / Hub Aktarmalı", f"{connecting_cnt} Ülke", "IST / SAW / DOH üzerinden tek aktarma", icon="✈️")
    with col3:
        render_kpi_card("Direkt Hat Ort. Süresi", f"{avg_direct_hrs:.1f} Saat", "70+ AJet / Pegasus / SunExpress ESB Hattı", icon="⏱️")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    fc1, fc2 = st.columns([1.2, 1.8])
    with fc1:
        f_filter = st.selectbox("Sefer Durumu Filtresi:", ["Tüm Ülkeler (59 Ülke)", "Yalnızca ESB Direkt Uçuş Var", "Yalnızca Aktarmalı Hatlar"])
    with fc2:
        f_search = st.text_input("🔍 Ülke, Havalimanı veya Havayolu Ara:", "", placeholder="Örn: AJet, Dubai, London, Taşkent, Baghdad...")

    f_view = travel_df.copy()
    if f_filter == "Yalnızca ESB Direkt Uçuş Var":
        f_view = f_view[f_view["direct_flight"] == True]
    elif f_filter == "Yalnızca Aktarmalı Hatlar":
        f_view = f_view[f_view["direct_flight"] == False]

    if f_search.strip():
        fs = f_search.strip().lower()
        f_view = f_view[
            f_view["country"].str.lower().str.contains(fs, na=False) |
            f_view["flight_route"].str.lower().str.contains(fs, na=False) |
            f_view["esb_update"].str.lower().str.contains(fs, na=False)
        ]

    f_view["sefer_durumu"] = f_view["direct_flight"].apply(lambda x: "✅ Direkt Uçuş Var" if x else "✈️ Aktarmalı (IST/SAW/DOH)")
    f_view["sure_str"] = f_view["flight_hrs"].apply(lambda x: f"{x:.1f} Saat")

    flight_table = f_view[["country", "excel_patients", "sefer_durumu", "sure_str", "flight_route", "esb_update"]].rename(columns={
        "country": "Kaynak Ülke",
        "excel_patients": "Vaka (Excel)",
        "sefer_durumu": "Ankara ESB Durumu",
        "sure_str": "Uçuş Süresi",
        "flight_route": "Havayolu & Rota (ESB)",
        "esb_update": "2026-2027 Güncel ESB Notu"
    })

    st.dataframe(flight_table, use_container_width=True, height=430, hide_index=True)

def render_prearrival_tests():
    """Renders pre-arrival medical tests checklist extracted directly from 'yurtdışı gelmeden test.xlsx'"""
    render_html("""
    <div class="section-card">
        <div class="section-header">
            <span>🩺 Türkiye'ye (Ankara) Gelmeden Önce Yaptırılması Gereken Ön Tetkikler</span>
            <span class="tag">yurtdışı gelmeden test.xlsx</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
            Uluslararası hastaların gereksiz uçuş, konaklama ve zaman kaybı yaşamaması için Ankara'ya seyahat etmeden önce kendi ülkelerinde tamamlayıp medikal koordinatörlerimize iletmesi gereken resmi klinik test listesi:
        </div>
    </div>
    """)

    c_female, c_male = st.columns(2)
    
    with c_female:
        render_html("""
        <div style="background: rgba(14, 47, 59, 0.7); border: 1px solid rgba(0, 240, 255, 0.35); border-radius: 10px; padding: 18px; height: 100%;">
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(0, 240, 255, 0.2); padding-bottom: 8px; margin-bottom: 12px;">
                <div style="font-size: 14px; font-weight: 700; color: #00F0FF;">
                    👩 KADIN EŞ İÇİN GEREKLİ TESTLER
                </div>
                <span style="font-size: 11px; background: rgba(0, 240, 255, 0.15); color: #00F0FF; padding: 2px 8px; border-radius: 4px;">
                    Adetin 2-3. Günü
                </span>
            </div>
            
            <div style="font-size: 13px; font-weight: 600; color: #18AEBB; margin-top: 8px; margin-bottom: 4px;">
                1. Bazal Hormon Profili (Over Rezervi Değerlendirmesi):
            </div>
            <ul style="font-size: 12px; color: #E2E8F0; line-height: 1.7; margin-bottom: 12px;">
                <li><b>FSH (Folikül Uyarıcı Hormon):</b> Yumurtalık rezervi ve uyarılabilirlik kapasitesi.</li>
                <li><b>LH (Luteinleştirici Hormon):</b> Ovülasyon ve hipofiz dengesi.</li>
                <li><b>E2 (Estradiol):</b> Bazal östrojen düzeyi; kist veya erken folikül varlığı kontrolü.</li>
            </ul>

            <div style="font-size: 13px; font-weight: 600; color: #18AEBB; margin-bottom: 4px;">
                2. Tiroid & Metabolik İnceleme:
            </div>
            <ul style="font-size: 12px; color: #E2E8F0; line-height: 1.7; margin-bottom: 12px;">
                <li><b>TSH (Tiroid Stimülan Hormon):</b> Sağlıklı implantasyon için &lt;2.5 mIU/L olması önerilir.</li>
            </ul>

            <div style="font-size: 13px; font-weight: 600; color: #18AEBB; margin-bottom: 4px;">
                3. Bulaşıcı Hastalık Serolojisi (Yasal Zorunluluk):
            </div>
            <ul style="font-size: 12px; color: #E2E8F0; line-height: 1.7; margin-bottom: 12px;">
                <li><b>HBsAg:</b> Hepatit B yüzey antijeni</li>
                <li><b>Anti-HCV:</b> Hepatit C antikoru</li>
                <li><b>HIV (Anti-HIV 1/2):</b> Bulaşıcı enfeksiyon kontrolü</li>
            </ul>

            <div style="font-size: 13px; font-weight: 600; color: #18AEBB; margin-bottom: 4px;">
                4. Genel Hematoloji:
            </div>
            <ul style="font-size: 12px; color: #E2E8F0; line-height: 1.7;">
                <li><b>CBC (Tam Kan Sayımı):</b> Hemoglobin, trombosit ve enfeksiyon belirteçleri.</li>
            </ul>
        </div>
        """)

    with c_male:
        render_html("""
        <div style="background: rgba(14, 47, 59, 0.7); border: 1px solid rgba(245, 130, 31, 0.35); border-radius: 10px; padding: 18px; height: 100%;">
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(245, 130, 31, 0.2); padding-bottom: 8px; margin-bottom: 12px;">
                <div style="font-size: 14px; font-weight: 700; color: #F5821F;">
                    👨 ERKEK EŞ İÇİN GEREKLİ TESTLER
                </div>
                <span style="font-size: 11px; background: rgba(245, 130, 31, 0.15); color: #F5821F; padding: 2px 8px; border-radius: 4px;">
                    3-5 Gün Perhiz
                </span>
            </div>

            <div style="font-size: 13px; font-weight: 600; color: #FF8C1A; margin-top: 8px; margin-bottom: 4px;">
                1. Androloji & Sperm Analizi:
            </div>
            <ul style="font-size: 12px; color: #E2E8F0; line-height: 1.7; margin-bottom: 16px;">
                <li><b>Spermiogram (Semen Analizi):</b> 3-5 günlük cinsel perhiz sonrası yapılmalıdır.
                    <br/>- Sperm Konsantrasyonu (Sayı / ml)
                    <br/>- Total Motilite (% İleri Hareketlilik)
                    <br/>- Morfoloji (Kruger Strict Kriterleri)
                    <br/><i>*Ağır oligoastenoteratozoospermi veya azospermi durumunda Ankara'ya gelmeden Mikro-TESE ön hazırlığı planlanır.</i>
                </li>
            </ul>

            <div style="font-size: 13px; font-weight: 600; color: #FF8C1A; margin-bottom: 4px;">
                2. Bulaşıcı Hastalık Serolojisi (Laboratuvar Güvenliği):
            </div>
            <ul style="font-size: 12px; color: #E2E8F0; line-height: 1.7;">
                <li><b>HBsAg:</b> Hepatit B yüzey antijeni</li>
                <li><b>Anti-HCV:</b> Hepatit C antikoru</li>
                <li><b>HIV (Anti-HIV 1/2):</b> Bulaşıcı enfeksiyon kontrolü</li>
            </ul>

            <div style="background: rgba(245, 130, 31, 0.1); border-left: 3px solid #F5821F; padding: 10px; border-radius: 6px; font-size: 11px; color: #CBD5E1; margin-top: 35px;">
                💡 <b>Klinik Neden:</b> Embriyoloji laboratuvarında döllenme (ICSI) ve kriyoprezervasyon (dondurma) tanklarının güvenliği için seroloji testleri yasal zorunluluktur.
            </div>
        </div>
        """)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    render_html("""
    <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 14px;">
        <div style="font-size: 13px; font-weight: 700; color: #10B981; margin-bottom: 4px;">
            🛡️ Ön Tetkiklerin Sınır Ötesi Hasta Kazanımına Etkisi:
        </div>
        <div style="font-size: 12px; color: #CBD5E1; line-height: 1.6;">
            Bu testler hastalar kendi ülkelerindeyken dijital olarak incelendiğinde; Ankara'ya geldiklerinde ortaya çıkabilecek <b>tıbbi uygunsuzluk iptalleri (Clinical Non-eligibility drop-off) %85 oranında önlenmektedir</b>. Çiftler Ankara Esenboğa'ya indiklerinde tedavi protokolleri, ilaç dozajları ve seyahat takvimleri önceden %100 kesinleşmiş olur.
        </div>
    </div>
    """)
