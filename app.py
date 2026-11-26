"""
GEN-ART Global Patient Intelligence Platform
Main Entry Point - Streamlit Application
Visual Identity: Dark Navy & Neon Turquoise Executive Cockpit
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta

# Page Configuration
st.set_page_config(
    page_title="GEN-ART | Global Patient Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Internal Imports
from config import APP_TITLE, APP_SUBTITLE, HEALTH_TOURISM_AUTH, THEME_COLORS, MARKET_GROUPS, COUNTRY_COORDINATES
from utils.components import inject_custom_css, render_top_navbar
from data.database import load_all_data, apply_filters
from modules.executive_cockpit import render_executive_cockpit
from modules.market_intelligence import render_market_intelligence
from modules.patient_crm import render_patient_crm
from modules.marketing_discovery import render_marketing_discovery
from modules.ai_forecasting import render_ai_forecasting
from modules.travel_logistics import render_travel_logistics
from modules.compliance_kvkk import render_compliance_kvkk
from modules.executive_reports import render_executive_reports
from modules.genetics_oncology import render_genetics_oncology

def main():
    # Inject high-end styling
    inject_custom_css()

    # Load baseline datasets including real clinical HBYS data
    leads_df, mcda_df, spend_df, actions_df, protocols, real_clinical_df = load_all_data()

    # Sidebar Header & Branding
    st.sidebar.image("assets/logo.png", use_container_width=True)
    st.sidebar.markdown(f"""
    <div style="padding: 4px 0 12px 0; border-bottom: 1px solid rgba(0, 240, 255, 0.2); margin-bottom: 14px;">
        <div style="font-size: 11px; font-weight: 700; color: #00F0FF; text-transform: uppercase; letter-spacing: 0.5px;">
            Global Patient Intelligence
        </div>
        <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">
            Ankara Tüp Bebek & Genetik Merkezi
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Navigation Menu
    nav_options = [
        "🌐 1. Yönetici Özeti (Cockpit)",
        "🌍 2. 3D Hasta Küresi & Pazar Zekası",
        "👥 3. Uluslararası Hasta CRM & Kayıp",
        "🎯 4. Dijital Pazarlama & Keşif",
        "🤖 5. AI Tahmin & Fırsat Motoru",
        "✈️ 6. Seyahat & Tedavi Lojistiği",
        "🛡️ 7. Mevzuat, Etik & KVKK Uyumu",
        "📊 8. Yönetici Raporları & Dışa Aktar",
        "🧬 9. Genetik & Kanser Pazar Zekası"
    ]
    
    st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding: 0 2px;">
        <span style="font-size: 11px; font-weight: 800; color: #00F0FF; text-transform: uppercase; letter-spacing: 0.8px; display: flex; align-items: center; gap: 6px;">
            <span>🧭</span> SİSTEM MODÜLLERİ
        </span>
        <span style="font-size: 10px; background: rgba(0, 240, 255, 0.12); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.35); padding: 2px 8px; border-radius: 12px; font-weight: 700; letter-spacing: 0.5px;">
            9 MODÜL
        </span>
    </div>
    """, unsafe_allow_html=True)

    if "current_module" not in st.session_state:
        st.session_state["current_module"] = "🌐 1. Yönetici Özeti (Cockpit)"

    for mod_title in nav_options:
        is_active = (st.session_state["current_module"] == mod_title)
        btn_type = "primary" if is_active else "secondary"
        if st.sidebar.button(mod_title, key=f"nav_btn_{mod_title[:6]}", use_container_width=True, type=btn_type):
            st.session_state["current_module"] = mod_title
            st.rerun()

    selected_nav = st.session_state["current_module"]

    st.sidebar.markdown("<div style='height: 10px; border-bottom: 1px solid rgba(24, 174, 187, 0.25); margin-bottom: 14px;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; padding: 0 2px;">
        <span style="font-size: 11px; font-weight: 800; color: #CBD5E1; text-transform: uppercase; letter-spacing: 0.8px; display: flex; align-items: center; gap: 6px;">
            <span>🔍</span> KÜRESEL FİLTRELEME
        </span>
        <span style="font-size: 10px; background: rgba(245, 130, 31, 0.15); color: #F5821F; border: 1px solid rgba(245, 130, 31, 0.35); padding: 2px 8px; border-radius: 12px; font-weight: 700;">
            CANLI
        </span>
    </div>
    """, unsafe_allow_html=True)

    # 1. Period Selector (Strict single-period adherence as required in docx)
    period_choice = st.sidebar.selectbox(
        "Raporlama Dönemi:",
        ["Tüm Yıllar / HBYS Veritabanı (2016 - 2026)", "2026 YTD", "Son 12 Ay (L12M)", "2025 Tam Yıl", "Özel Tarih Aralığı"],
        index=0
    )

    if period_choice == "Tüm Yıllar / HBYS Veritabanı (2016 - 2026)":
        start_date = date(2016, 1, 1)
        end_date = date(2026, 12, 31)
        date_label = "Tüm Yıllar / HBYS Verisi (2016 - 2026)"
    elif period_choice == "2026 YTD":
        start_date = date(2026, 1, 1)
        end_date = date(2026, 11, 15)
        date_label = "2026 YTD (1 Oca - 15 Kas 2026)"
    elif period_choice == "Son 12 Ay (L12M)":
        start_date = date(2025, 11, 15)
        end_date = date(2026, 11, 15)
        date_label = "Son 12 Ay (Kas 2025 - Kas 2026)"
    elif period_choice == "2025 Tam Yıl":
        start_date = date(2025, 1, 1)
        end_date = date(2025, 12, 31)
        date_label = "2025 Tam Yıl"
    else:
        c_d1, c_d2 = st.sidebar.columns(2)
        start_date = c_d1.date_input("Başlangıç", date(2016, 1, 1))
        end_date = c_d2.date_input("Bitiş", date(2026, 12, 31))
        date_label = f"{start_date.strftime('%d.%m.%Y')} - {end_date.strftime('%d.%m.%Y')}"

    # 2. Country Selector (Sorted by real clinical volume descending, then remaining)
    vol_order = [c for c in leads_df["country"].value_counts().index.tolist() if "Boş" not in str(c)]
    extra_countries = sorted([c for c in COUNTRY_COORDINATES.keys() if c not in vol_order])
    all_countries = vol_order + extra_countries
    if "Ülke Kaydı Boş (HBYS)" in leads_df["country"].values:
        all_countries.append("Ülke Kaydı Boş (HBYS)")
    selected_countries = st.sidebar.multiselect("Hedef Ülke(ler):", all_countries, default=None, placeholder="Tüm Ülkeler")

    # 3. Language Selector
    all_languages = sorted(list(leads_df["language"].unique()))
    selected_languages = st.sidebar.multiselect("Hasta İletişim Dili:", all_languages, default=None, placeholder="Tüm Diller")

    # 4. Acquisition Channel Selector
    all_channels = sorted(list(leads_df["channel"].unique()))
    selected_channels = st.sidebar.multiselect("Kazanım Kanalı:", all_channels, default=None, placeholder="Tüm Kanallar")

    # 5. Coordinator Selector
    all_coordinators = ["Tümü (All)"] + sorted(list(leads_df["coordinator"].unique()))
    selected_coordinator = st.sidebar.selectbox("Sorumlu Koordinatör:", all_coordinators, index=0)

    # Apply unified filter pipeline
    filtered_leads, filtered_spend = apply_filters(
        leads_df=leads_df,
        spend_df=spend_df,
        start_date=start_date,
        end_date=end_date,
        selected_countries=selected_countries,
        selected_languages=selected_languages,
        selected_channels=selected_channels,
        selected_coordinator=selected_coordinator
    )

    # Sidebar footer badge
    st.sidebar.markdown(f"""
    <div style="margin-top: 30px; padding: 12px; background: rgba(14, 26, 56, 0.8); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 8px; font-size: 11px;">
        <div style="color: #00F0FF; font-weight: 700;">🛡️ ST-0625 Yetkili Sağlık Turizmi</div>
        <div style="color: #94A3B8; margin-top: 4px;">T.C. Sağlık Bakanlığı Onaylı Akreditasyon</div>
        <div style="color: #64748B; margin-top: 4px; font-size: 10px;">KVKK Madde 6 Uyumlu De-Identified Data</div>
    </div>
    """, unsafe_allow_html=True)

    # Render Top Navigation Bar in main view
    render_top_navbar(date_label=date_label)

    # Render Selected Module
    if "1." in selected_nav:
        render_executive_cockpit(filtered_leads, filtered_spend, actions_df, date_label, real_clinical_df)
    elif "2." in selected_nav:
        render_market_intelligence(filtered_leads, mcda_df)
    elif "3." in selected_nav:
        render_patient_crm(filtered_leads, real_clinical_df)
    elif "4." in selected_nav:
        render_marketing_discovery(filtered_leads, filtered_spend)
    elif "5." in selected_nav:
        render_ai_forecasting(filtered_leads, filtered_spend)
    elif "6." in selected_nav:
        render_travel_logistics(mcda_df, filtered_leads, protocols)
    elif "7." in selected_nav:
        render_compliance_kvkk()
    elif "8." in selected_nav:
        render_executive_reports(filtered_leads, filtered_spend, actions_df, date_label)
    elif "9." in selected_nav:
        render_genetics_oncology()

if __name__ == "__main__":
    main()
