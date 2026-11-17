"""
Module 3: International Patient CRM & Conversion Drop-off Analyzer
Pinpoints exactly where and why international patients are lost across the acquisition pipeline.
Distinguishes marketing drop-offs from operational, clinical, and logistics roadblocks.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import THEME_COLORS, DROP_OFF_REASONS
from utils.components import render_kpi_card

def render_patient_crm(filtered_leads):
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
            👥 Uluslararası Hasta CRM & Dönüşüm Kayıp (Drop-off) Analizleri
        </h2>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
            Hastaların tedaviye başlamasını engelleyen kök nedenleri tespit ederek pazarlama, operasyon ve klinik engelleri ayrıştırın
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_dropoff, tab_simulator, tab_leads = st.tabs([
        "🔍 Kayıp Nedenleri Kök Neden Analizi",
        "🎛️ Hasta Dönüşüm Simülatörü",
        "📋 De-Identified Hasta Takip Listesi"
    ])

    with tab_dropoff:
        render_dropoff_breakdown(filtered_leads)

    with tab_simulator:
        render_conversion_simulator()

    with tab_leads:
        render_leads_table(filtered_leads)

def render_dropoff_breakdown(leads_df):
    """Visualizes reasons why inquiries dropped out of the funnel"""
    lost_leads = leads_df[leads_df["drop_reason"].notna()]
    total_lost = len(lost_leads)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Toplam Kaybedilen Başvuru", f"{total_lost:,}", f"İncelenen {len(leads_df)} vaka içinden", icon="📉")
    with col2:
        maliyet_kaybi = len(lost_leads[lost_leads["drop_reason"].str.contains("Maliyet|Affordability", na=False)])
        maliyet_pct = (maliyet_kaybi / total_lost * 100) if total_lost > 0 else 0
        render_kpi_card("Bütçe / Fiyat Kaynaklı", f"%{maliyet_pct:.1f}", f"{maliyet_kaybi} hasta bütçeyi yüksek buldu", icon="💶")
    with col3:
        sla_kaybi = len(lost_leads[lost_leads["drop_reason"].str.contains("Gecikmiş|Slow", na=False)])
        sla_pct = (sla_kaybi / total_lost * 100) if total_lost > 0 else 0
        render_kpi_card("İletişim & Yanıt Gecikmesi", f"%{sla_pct:.1f}", f"{sla_kaybi} hasta geç yanıttan dolayı koptu", icon="⏱️")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    c_pie, c_bar = st.columns([1, 1.3])
    
    with c_pie:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>📊 Kayıp Nedenleri Dağılımı</span>
            </div>
        """, unsafe_allow_html=True)
        
        reason_counts = lost_leads["drop_reason"].value_counts().reset_index()
        reason_counts.columns = ["Neden", "Adet"]
        
        fig = px.pie(
            reason_counts,
            names="Neden",
            values="Adet",
            hole=0.45,
            color_discrete_sequence=["#EF4444", "#F59E0B", "#00B4D8", "#8B5CF6", "#64748B", "#EC4899"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            margin=dict(l=10, r=10, t=20, b=10),
            height=300,
            showlegend=True,
            legend=dict(orientation="h", y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_bar:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>🌍 Ülkelere Göre En Belirgin Kayıp Sebebi</span>
            </div>
        """, unsafe_allow_html=True)
        
        country_loss = lost_leads.groupby(["country", "drop_reason"]).size().reset_index(name="Kayıp_Adedi")
        # Top 6 countries
        top_c = leads_df["country"].value_counts().head(6).index
        country_loss_filtered = country_loss[country_loss["country"].isin(top_c)]
        
        fig_bar = px.bar(
            country_loss_filtered,
            x="country",
            y="Kayıp_Adedi",
            color="drop_reason",
            title="Ülke Bazlı Neden Ayrımı",
            barmode="stack",
            color_discrete_sequence=["#EF4444", "#F59E0B", "#00B4D8", "#8B5CF6", "#64748B", "#EC4899"]
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            margin=dict(l=10, r=10, t=30, b=10),
            height=300,
            legend=dict(title="")
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_conversion_simulator():
    """Interactive Patient conversion simulator matching docx spec Section 5"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🧮 İnteraktif Hasta Dönüşüm Simülatörü</span>
            <span class="tag">Varsayım Modeli</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 16px;">
            Örneğin: GEN-ART bir ülkeden 100 başvuru aldığında aşama geçiş oranlarını değiştirerek nihai tedaviye başlayan hasta sayısını ve beklenen ciroyu anlık simüle edebilirsiniz.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        inquiries = st.number_input("Aylık Başvuru Hacmi", min_value=10, max_value=2000, value=100, step=10)
    with col2:
        r1 = st.slider("1. Başvuru → Nitelikli (%)", 10, 100, 50, step=5) / 100.0
    with col3:
        r2 = st.slider("2. Nitelikli → Konsültasyon (%)", 10, 100, 60, step=5) / 100.0
    with col4:
        r3 = st.slider("3. Konsültasyon → Tedavi (%)", 5, 80, 20, step=1) / 100.0

    # Calculations
    qualified = inquiries * r1
    consulted = qualified * r2
    treatment_starts = consulted * r3
    overall_cvr = (treatment_starts / inquiries) * 100.0
    est_revenue = treatment_starts * 5500.0  # Average package €5,500
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    c_res1, c_res2, c_res3, c_res4 = st.columns(4)
    with c_res1:
        render_kpi_card("Nitelikli Başvuru", f"{qualified:.1f}", f"%{r1*100:.0f} Ön Kabul", icon="1️⃣")
    with c_res2:
        render_kpi_card("Gerçekleşen Konsültasyon", f"{consulted:.1f}", f"%{r2*100:.0f} Doktor Randevusu", icon="2️⃣")
    with c_res3:
        render_kpi_card("Beklenen Tedavi Başlangıcı", f"{treatment_starts:.1f}", "Ayda Kesin Başlayan", icon="🧬", is_highlight=True)
    with c_res4:
        render_kpi_card("Toplam Dönüşüm / Ciro", f"%{overall_cvr:.1f}", f"Tahmini Ciro: €{est_revenue:,.0f}", icon="💶", is_highlight=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_leads_table(leads_df):
    """De-identified register table for international patient leads"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🛡️ KVKK Uyumlu Anonim Hasta Takip Listesi (CRM)</span>
            <span class="tag">Kişisel Veri İçermez</span>
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
            Yönetici kokpiti seviyesinde hasta isimleri veya özel klinik notlar gizlenmiştir. Süreç, koordinatör ve dönüşüm durumu takip edilir.
        </div>
    """, unsafe_allow_html=True)
    
    filter_stage = st.multiselect("Aşama Filtresi:", leads_df["stage"].unique(), default=None)
    
    display_leads = leads_df.copy()
    if filter_stage:
        display_leads = display_leads[display_leads["stage"].isin(filter_stage)]
        
    display_leads["inquiry_date"] = display_leads["inquiry_date"].dt.strftime("%Y-%m-%d %H:%M")
    display_leads["response_time_hrs"] = display_leads["response_time_hrs"].apply(lambda x: f"{x:.1f} saat")
    display_leads["revenue"] = display_leads["revenue"].apply(lambda x: f"€{x:,.0f}" if x > 0 else "-")
    
    st.dataframe(
        display_leads[[
            "lead_id", "inquiry_date", "country", "language", "channel",
            "coordinator", "response_time_hrs", "clinical_segment", "stage", "drop_reason", "revenue"
        ]].rename(columns={
            "lead_id": "Kayıt No",
            "inquiry_date": "Başvuru Zamanı",
            "country": "Ülke",
            "language": "Dil",
            "channel": "Kanal",
            "coordinator": "Koordinatör",
            "response_time_hrs": "Yanıt Süresi",
            "clinical_segment": "Klinik İlgi Segmenti",
            "stage": "Aşama",
            "drop_reason": "Kayıp Nedeni",
            "revenue": "Ciro (€)"
        }),
        use_container_width=True,
        height=400,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
