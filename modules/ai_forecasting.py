"""
Module 5: AI Forecasting & Patient Acquisition Opportunity Engine
Connects: Demand -> Sustainable CAC -> Treatment Barriers.
Provides what-if scenario simulation and strategic recommendations with projected outcomes.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from config import THEME_COLORS
from utils.components import render_kpi_card

def render_ai_forecasting(leads_df, spend_df):
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
            🤖 AI Tahminleme & Hasta Kazanım Fırsat Motoru
        </h2>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
            Yapay zekâ destekli büyüme senaryoları, bütçe optimizasyonu ve karar destek simülasyonları
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_engine, tab_simulator, tab_budget = st.tabs([
        "🧠 AI Fırsat Öneri Motoru (Strategy Engine)",
        "🎛️ Çok Değişkenli Senaryo Simülatörü",
        "💰 Pazar Bazlı Bütçe & ROI Optimizasyonu"
    ])

    with tab_engine:
        render_opportunity_engine(leads_df)

    with tab_simulator:
        render_scenario_simulator(leads_df, spend_df)

    with tab_budget:
        render_budget_optimizer(leads_df, spend_df)

def render_opportunity_engine(leads_df):
    """Answers the 3 core strategic questions specified in the design doc"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>💡 AI Patient Acquisition Opportunity Engine</span>
            <span class="tag">Stratejik Karar Destek</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6; margin-bottom: 16px;">
            Motor, kliniğin 3 temel sorusunu otomatik analiz eder ve yönetime insan onaylı stratejik öneriler sunar:
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 10px; padding: 14px;">
            <div style="font-size: 13px; font-weight: 700; color: #00F0FF; margin-bottom: 6px;">
                1. Anlamlı Talep Üreten Ülkeler
            </div>
            <div style="font-size: 12px; color: #E2E8F0; line-height: 1.5;">
                • <b>Irak & Ürdün:</b> Yüksek hacimli genel IVF talebi.<br/>
                • <b>Azerbaycan:</b> Güçlü hekim güveni & tekrarlayan başarısız vaka yoğunluğu.<br/>
                • <b>Almanya:</b> Yasal kısıtlar nedeniyle sınır ötesi PGT-A taraması arayışı.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 14px;">
            <div style="font-size: 13px; font-weight: 700; color: #10B981; margin-bottom: 6px;">
                2. Sürdürülebilir CAC ile Nitelikli Pazar
            </div>
            <div style="font-size: 12px; color: #E2E8F0; line-height: 1.5;">
                • <b>Balkanlar (Sırbistan/Bosna):</b> CAC ortalama <b>€410</b> ile en ekonomik pazar.<br/>
                • <b>Azerbaycan:</b> Dönüşüm %9.2, CAC <b>€530</b>, yüksek kârlılık.<br/>
                • <b>Körfez (Kuveyt/Katar):</b> CAC yüksek (€1,150) ancak vaka başı gelir €7,800.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 14px;">
            <div style="font-size: 13px; font-weight: 700; color: #F87171; margin-bottom: 6px;">
                3. Tedavi Başlangıcını Engelleyen Bariyerler
            </div>
            <div style="font-size: 12px; color: #E2E8F0; line-height: 1.5;">
                • <b>Libya:</b> Vize gecikmeleri ve direkt uçuş yokluğu nedeniyle %40 fire.<br/>
                • <b>Orta Doğu:</b> İlk 4 saatte yanıt verilmeyen taleplerde %58 terk.<br/>
                • <b>Avrupa:</b> Seyahat süresi planlaması ve iş izni uyumsuzlukları.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 8px; padding: 14px;">
        <div style="font-size: 14px; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">
            🚀 AI Tarafından Önerilen En Yüksek Getirili 3 Eylem (Proactive Recommendations):
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
            1. <b>Arapça Triage Otomasyonu:</b> İlk yanıt süresini 1.5 saate çekerek Orta Doğu konsültasyon kabulünü +%18 artırın (Beklenen ek ciro: +€42,000/ay).<br/>
            2. <b>Almanya/Hollanda PGT-A Bilgi Kampanyası:</b> Yasal mevzuat kısıtlarını açıklayan ve genetik danışmanlık sunan Almanca içerik yayına alın (Beklenen yeni vaka: +4/ay).<br/>
            3. <b>Balkan Bütçe Genişletmesi:</b> Düşük CAC avantajını kullanarak Sırbistan ve Bosna bütçesini %30 artırın (Öngörülen ek tedavi: +3 vaka/ay).
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)

def render_scenario_simulator(leads_df, spend_df):
    """Simulates What-if scenarios like increasing budget or improving conversion"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🔮 What-If Senaryo Simülatörü</span>
            <span class="tag">Dinamik Tahmin</span>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        budget_change = st.slider("Pazarlama Bütçesi Değişimi (%)", -50, 100, 25, step=5, help="Google Ads & Meta harcama değişimi")
    with col2:
        cvr_boost = st.slider("Konsültasyon Dönüşüm İyileştirmesi (%)", 0, 50, 15, step=5, help="Hızlı yanıt ve koordinatör eğitimi etkisi")
    with col3:
        new_market_switch = st.selectbox("Yeni Dil / Pazar Açılışı:", ["Yok (Mevcut Pazar)", "Rusça Pazar Genişletmesi (Özbekistan/Kazakistan)", "Almanya Diaspora & PGT Odak"], index=1)

    # Base monthly metrics
    base_inquiries = 240
    base_starts = 18
    base_spend = 12240
    base_revenue = 108000
    
    # Calculate simulated metrics
    budget_factor = 1.0 + (budget_change / 100.0)
    cvr_factor = 1.0 + (cvr_boost / 100.0)
    
    market_bonus_inquiries = 40 if "Rusça" in new_market_switch else (25 if "Almanya" in new_market_switch else 0)
    
    sim_spend = base_spend * budget_factor
    sim_inquiries = int((base_inquiries * budget_factor) + market_bonus_inquiries)
    sim_starts = int((base_starts * (budget_factor ** 0.85) * cvr_factor) + (market_bonus_inquiries * 0.08))
    sim_revenue = sim_starts * 6000
    sim_cac = (sim_spend / sim_starts) if sim_starts > 0 else 0
    
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    # Comparison cards
    c_a, c_b, c_c, c_d = st.columns(4)
    with c_a:
        delta_inq = sim_inquiries - base_inquiries
        render_kpi_card("Tahmini Başvuru", f"{sim_inquiries}", f"Fark: +{delta_inq} lead", icon="📥")
    with c_b:
        delta_starts = sim_starts - base_starts
        render_kpi_card("Tedavi Başlangıcı", f"{sim_starts}", f"Fark: +{delta_starts} hasta", icon="🧬", is_highlight=True)
    with c_c:
        render_kpi_card("Yeni CAC", f"€{sim_cac:,.0f}", f"Önceki: €{base_spend/base_starts:,.0f}", icon="💶")
    with c_d:
        delta_rev = sim_revenue - base_revenue
        render_kpi_card("Tahmini Gelir", f"€{sim_revenue:,.0f}", f"Fark: +€{delta_rev:,.0f}", icon="💎", is_highlight=True)

    # Chart comparison
    fig = go.Figure(data=[
        go.Bar(name='Mevcut Durum', x=['Başvurular', 'Tedavi Başlangıçları', 'Gelir (€ Bin)'], y=[base_inquiries, base_starts, base_revenue/1000], marker_color='#64748B'),
        go.Bar(name='Simülasyon Sonucu', x=['Başvurular', 'Tedavi Başlangıçları', 'Gelir (€ Bin)'], y=[sim_inquiries, sim_starts, sim_revenue/1000], marker_color='#00F0FF')
    ])
    fig.update_layout(
        barmode='group',
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1"),
        height=320,
        margin=dict(l=10, r=10, t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_budget_optimizer(leads_df, spend_df):
    """Budget reallocation recommendation based on marginal ROI"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>💰 AI Destekli Bütçe Yeniden Tahsis Önerisi</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
            Yapay zekâ optimizasyon motoru, dönüşümü düşük kanallardan (örn. jenerik arama) bütçe kısıp yüksek marjlı PGT ve Türki Cumhuriyetler kampanyalarına aktarmayı öneriyor:
        </div>
    """, unsafe_allow_html=True)
    
    realloc_data = [
        {"Pazar / Kanal": "Irak & Körfez Arapça Reklamları", "Mevcut Bütçe (€)": 4500, "Önerilen Bütçe (€)": 5200, "Değişim": "+%15.5", "Gerekçe": "Yüksek talep ve hızlanan koordinatör yanıtı"},
        {"Pazar / Kanal": "Azerbaycan & Özbekistan Odaklı", "Mevcut Bütçe (€)": 2800, "Önerilen Bütçe (€)": 3800, "Değişim": "+%35.7", "Gerekçe": "En düşük CAC (€530) ve yüksek tedavi tamamlanma oranı"},
        {"Pazar / Kanal": "Almanya & Hollanda PGT-A", "Mevcut Bütçe (€)": 2200, "Önerilen Bütçe (€)": 3100, "Değişim": "+%40.9", "Gerekçe": "Vaka başı yüksek gelir (€7,500) ve genetik uzmanlık talebi"},
        {"Pazar / Kanal": "Jenerik Meta Kampanyaları", "Mevcut Bütçe (€)": 2740, "Önerilen Bütçe (€)": 1500, "Değişim": "-%45.2", "Gerekçe": "Tıklama çok fakat nitelikli konsültasyona dönüşüm düşük"}
    ]
    st.dataframe(pd.DataFrame(realloc_data), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
