"""
Module 2: Global Market Opportunity Intelligence & 3D Patient Flow Globe
Visualizes GEN-ART International Patient Flow corridors directly into Ankara using a true 3D Interactive Orthographic Globe.
Includes multi-criteria decision analysis (MCDA) country attractiveness scoring with live weight adjustment.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from config import THEME_COLORS, CLINIC_COORDINATES, COUNTRY_COORDINATES

def calculate_mcda_scores(mcda_df, w_demand, w_afford, w_travel, w_diff, w_digital, w_reg):
    """Calculates normalized MCDA score S_c = sum(w_i * x_c_i)"""
    total_w = w_demand + w_afford + w_travel + w_diff + w_digital + w_reg
    if total_w == 0:
        total_w = 1.0
        
    nw_demand = w_demand / total_w
    nw_afford = w_afford / total_w
    nw_travel = w_travel / total_w
    nw_diff = w_diff / total_w
    nw_digital = w_digital / total_w
    nw_reg = w_reg / total_w
    
    df = mcda_df.copy()
    df["mcda_score"] = (
        df["demand_score"] * nw_demand +
        df["affordability_score"] * nw_afford +
        df["travel_score"] * nw_travel +
        df["differentiation_score"] * nw_diff +
        df["digital_score"] * nw_digital +
        df["regulatory_score"] * nw_reg
    ).round(1)
    
    return df.sort_values(by="mcda_score", ascending=False)

def render_market_intelligence(leads_df, mcda_df):
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
            🌍 Küresel Pazar Fırsat Zekası & 3D Hasta Akış Küresi
        </h2>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
            GEN-ART Ankara merkezli uluslararası hasta hareketliliği, pazar cazibe analizi (MCDA) ve ülke 360° değerlendirmeleri
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_map, tab_mcda, tab_profile = st.tabs([
        "🌐 3D Uluslararası Hasta Akış Küresi",
        "🧮 AI Ülke Cazibe Skorlama Modeli (MCDA)",
        "🔍 Ülke 360° Derinlik Analizi"
    ])

    with tab_map:
        render_globe_view(leads_df, mcda_df)

    with tab_mcda:
        render_mcda_tool(mcda_df)

    with tab_profile:
        render_country_profile_view(mcda_df, leads_df)

def render_globe_view(leads_df, mcda_df):
    """Renders a true 3D Orthographic Earth Globe with flight corridors to Ankara and patient volumes"""
    col_map, col_stats = st.columns([2.2, 1])
    
    with col_map:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>✈️ Ankara Uluslararası Hasta Koridorları (3D Hasta Akış Küresi)</span>
                <span class="tag">Ankara Esenboğa (ESB)</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 8px;">
                Dünya küresini fareyle döndürebilir, ülkelerin üzerine gelerek hasta ve tedavi sayılarını inceleyebilirsiniz.
            </div>
        """, unsafe_allow_html=True)
        
        ankara_lon, ankara_lat = CLINIC_COORDINATES
        
        # Build 3D Globe Figure using Plotly Orthographic projection
        fig = go.Figure()
        
        # 1. Flight Arcs from each country to Ankara
        for _, row in mcda_df.iterrows():
            c_name = row["country"]
            if c_name in COUNTRY_COORDINATES:
                coord = COUNTRY_COORDINATES[c_name]
                c_leads = len(leads_df[leads_df["country"] == c_name])
                c_starts = len(leads_df[(leads_df["country"] == c_name) & (leads_df["stage"] == "5. Treatment Started - Ankara")])
                
                # Arc line
                line_color = "#10B981" if c_starts > 10 else "#00F0FF"
                line_width = max(1.5, min(4.5, c_starts * 0.25))
                
                fig.add_trace(go.Scattergeo(
                    lon=[coord["lon"], ankara_lon],
                    lat=[coord["lat"], ankara_lat],
                    mode='lines',
                    line=dict(width=line_width, color=line_color),
                    opacity=0.75,
                    hoverinfo='none',
                    showlegend=False
                ))
                
                # Country Marker
                fig.add_trace(go.Scattergeo(
                    lon=[coord["lon"]],
                    lat=[coord["lat"]],
                    mode='markers+text',
                    text=[coord["code"]],
                    textposition="top center",
                    textfont=dict(color="#00F0FF", size=10, family="Plus Jakarta Sans"),
                    marker=dict(
                        size=max(8, min(24, 6 + (c_leads * 0.12))),
                        color=line_color,
                        opacity=0.85,
                        line=dict(width=1, color="#FFFFFF")
                    ),
                    name=c_name,
                    hovertemplate=f"<b>{c_name} ({coord['code']})</b><br>" +
                                  f"Bölge: {coord['region']}<br>" +
                                  f"Toplam Başvuru: <b>{c_leads}</b><br>" +
                                  f"Tedaviye Başlayan: <b>{c_starts}</b><extra></extra>",
                    showlegend=False
                ))

        # 2. Ankara Clinic Center Marker (Pulsing Center)
        fig.add_trace(go.Scattergeo(
            lon=[ankara_lon],
            lat=[ankara_lat],
            mode='markers+text',
            text=["GEN-ART (Ankara)"],
            textposition="bottom center",
            textfont=dict(color="#FFFFFF", size=12, family="Plus Jakarta Sans"),
            marker=dict(
                size=18,
                color="#00F0FF",
                symbol="star",
                line=dict(width=2, color="#FFFFFF")
            ),
            name="GEN-ART Clinic",
            hovertemplate="<b>GEN-ART IVF & Genetics Center</b><br>ST-0625 Yetkili Merkez<br>Ankara, Türkiye<extra></extra>",
            showlegend=False
        ))

        # 3D Orthographic Globe Styling
        fig.update_geos(
            projection_type="orthographic",
            projection_rotation=dict(lon=38, lat=35, roll=0),
            showocean=True,
            oceancolor="#070D1E",
            showland=True,
            landcolor="#132347",
            showlakes=True,
            lakecolor="#070D1E",
            showcountries=True,
            countrycolor="rgba(0, 240, 255, 0.35)",
            countrywidth=1,
            showcoastlines=True,
            coastlinecolor="rgba(0, 240, 255, 0.4)",
            coastlinewidth=1,
            bgcolor="rgba(0,0,0,0)",
            resolution=110
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            height=460,
            font=dict(family="Plus Jakarta Sans", color="#CBD5E1")
        )

        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_stats:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>🏆 En Aktif Hasta Pazarları</span>
            </div>
        """, unsafe_allow_html=True)
        
        top_countries = leads_df.groupby("country").agg(
            basvuru=("lead_id", "count"),
            tedavi=("stage", lambda x: (x == "5. Treatment Started - Ankara").sum()),
            gelir=("revenue", "sum")
        ).reset_index().sort_values(by="tedavi", ascending=False).head(5)
        
        for idx, r in top_countries.iterrows():
            st.markdown(f"""
            <div style="background: rgba(19, 35, 71, 0.6); padding: 10px 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #00F0FF;">
                <div style="display: flex; justify-content: space-between; font-weight: 700; color: #FFFFFF;">
                    <span>{r['country']}</span>
                    <span style="color: #10B981;">€{r['gelir']:,.0f}</span>
                </div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 3px; display: flex; justify-content: space-between;">
                    <span>📥 {r['basvuru']} Başvuru</span>
                    <span>🧬 <b>{r['tedavi']} Tedavi Başlangıcı</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("""
        <div style="font-size: 11px; color: #64748B; margin-top: 10px; line-height: 1.4;">
            ℹ️ Ankara Esenboğa Havalimanı (ESB) doğrudan uçuş erişimi ve vizesiz/e-vize imkanı sunan Orta Doğu ve Türki Cumhuriyetler en yüksek dönüşüm katsayısına sahiptir.
        </div>
        </div>
        """, unsafe_allow_html=True)

def render_mcda_tool(mcda_df):
    """Interactive multi-criteria decision analysis weight adjustment tool"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>⚖️ Çok Kriterli Karar Verme (MCDA) Ağırlık Ayarları</span>
            <span class="tag">Formül: S_c = ∑ w_i · x_{c,i}</span>
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 14px;">
            Ağırlıkları kliniğin stratejik önceliklerine göre ayarlayın. Ağırlıklar otomatik normalize edilir (%100).
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        w_demand = st.slider("Hasta Talebi & Tedavi İhtiyacı (%)", 0, 50, 25, help="İnfertilite prevalansı ve yerel tedavi yetersizliği")
        w_afford = st.slider("Tedavi Karşılanabilirliği & Gelir Düzeyi (%)", 0, 50, 20, help="Kişi başı GSYİH ve medikal satın alma gücü")
    with col2:
        w_travel = st.slider("Seyahat & Lojistik Erişilebilirlik (%)", 0, 50, 15, help="Vize rejimi, uçuş süresi ve Ankara direkt hatları")
        w_diff = st.slider("Rekabet & Genetik Farklılaşma (%)", 0, 50, 15, help="PGT ve genetik tanı üstünlüğü / Yerel kanun kısıtlamaları")
    with col3:
        w_digital = st.slider("Dijital Kazanım Potansiyeli (%)", 0, 50, 15, help="Google/Meta reklam erişimi, arama hacmi")
        w_reg = st.slider("Yasal & Operasyonel Uygunluk (%)", 0, 50, 10, help="Sağlık turizmi mevzuat ve sınır ötesi uyumu")

    scored_df = calculate_mcda_scores(mcda_df, w_demand, w_afford, w_travel, w_diff, w_digital, w_reg)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Render Bar chart & Ranked Table
    c_chart, c_table = st.columns([1.3, 1])
    
    with c_chart:
        fig = px.bar(
            scored_df,
            x="country",
            y="mcda_score",
            color="region",
            color_discrete_map={
                "Middle East": "#00F0FF",
                "Central Asia": "#10B981",
                "Europe": "#8B5CF6",
                "Balkans": "#F59E0B",
                "Other": "#EC4899"
            },
            title="Ülke Fırsat Skoru Sıralaması (0 - 100)",
            labels={"country": "Ülke", "mcda_score": "Skor (Puan)", "region": "Pazar Grubu"}
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1"),
            height=360,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_table:
        st.dataframe(
            scored_df[["country", "region", "mcda_score", "demand_score", "affordability_score", "travel_score"]].rename(columns={
                "country": "Ülke", "region": "Bölge", "mcda_score": "Fırsat Skoru",
                "demand_score": "Talep", "affordability_score": "Gelir", "travel_score": "Seyahat"
            }),
            use_container_width=True,
            height=360,
            hide_index=True
        )

def render_country_profile_view(mcda_df, leads_df):
    """Detailed 360-degree country analysis with regulatory, travel, and competitor context"""
    selected_c = st.selectbox("İncelemek İstediğiniz Hedef Ülkeyi Seçin:", sorted(list(mcda_df["country"].unique())))
    
    c_info = mcda_df[mcda_df["country"] == selected_c].iloc[0]
    c_leads = leads_df[leads_df["country"] == selected_c]
    
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        render_kpi_card("Vize Rejimi", c_info["visa_type"], f"Bölge: {c_info['region']}", icon="🛂")
    with col_b:
        render_kpi_card("Uçuş Süresi", f"{c_info['flight_hrs']} Saat", "Ankara Direkt Uçuş" if c_info['direct_flight'] else "Aktarmalı Uçuş", icon="✈️")
    with col_c:
        render_kpi_card("Ort. Kalış Süresi", f"{c_info['avg_stay_days']} Gün", "IVF / PGT Siklus Süresi", icon="🏨")
    with col_d:
        render_kpi_card("Doğurganlık Hızı", f"{c_info['fertility_rate']}", "Kadın Başı Doğum", icon="👶")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    p1, p2 = st.columns(2)
    with p1:
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">
                <span>🎯 {selected_c} Pazar Stratejik Hipotezi</span>
            </div>
            <p style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
                <b>Rekabet Dinamiği:</b> {c_info['competitor_density']}<br/><br/>
                <b>GEN-ART Değer Önerisi:</b> GEN-ART'ın akredite genetik tanı merkezi, PGT-A ve karmaşık infertilite vakalarındaki uzmanlığı, {selected_c} pazarındaki yüksek maliyetli veya kısıtlayıcı yerel alternatiflere karşı güçlü bir medikal güven unsuru oluşturmaktadır.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with p2:
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">
                <span>📊 {selected_c} Mevcut Veri Durumu</span>
            </div>
            <ul style="font-size: 13px; color: #CBD5E1; line-height: 1.8;">
                <li>Toplam Kayıtlı Başvuru: <b>{len(c_leads)}</b></li>
                <li>Tamamlanan Doktor Görüşmesi: <b>{len(c_leads[c_leads['consultation_date'].notna()])}</b></li>
                <li>Ankara'da Tedaviye Başlayan: <b>{len(c_leads[c_leads['stage'] == '5. Treatment Started - Ankara'])}</b></li>
                <li>Üretilen Toplam Tedavi Geliri: <b>€{c_leads['revenue'].sum():,.0f}</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
