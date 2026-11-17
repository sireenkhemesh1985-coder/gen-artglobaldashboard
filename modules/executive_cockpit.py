"""
Module 1: Global Patient Acquisition Command Center (Executive Overview)
Fulfills all core instructions from genart-dashboard spec:
- 6 standardized KPI cards
- Left: Patient Acquisition Funnel & Drop-off stages
- Right: Single-country granular performance table (no grouped countries!)
- Overdue inquiries / SLA follow-ups
- Approved Strategic Action Plans table with full detail drawer
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from config import THEME_COLORS
from utils.components import render_kpi_card, build_funnel_figure
from data.database import calculate_executive_kpis, get_country_performance_summary, get_overdue_tasks

def render_executive_cockpit(filtered_leads, filtered_spend, actions_df, date_label):
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
            🌐 Uluslararası Hasta Kazanım Komuta Merkezi <span style="font-size: 14px; font-weight: 400; color: #94A3B8;">(Yönetici Özeti)</span>
        </h2>
        <span style="font-size: 12px; color: #00F0FF; background: rgba(0,240,255,0.1); padding: 4px 10px; border-radius: 6px; border: 1px solid rgba(0,240,255,0.3);">
            Aktif Dönem Filtresi: <b>{date_label}</b>
        </span>
    </div>
    """, unsafe_allow_html=True)

    # 1. Calculate 6 Core KPIs
    kpis = calculate_executive_kpis(filtered_leads, filtered_spend)
    
    # 2. Render 6 KPI Cards in a clean responsive grid
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        render_kpi_card(
            title="Yeni Başvuru",
            value=f"{kpis['total_inquiries']:,}",
            subtext=f"<span class='highlight'>{kpis['qualified_leads']}</span> nitelikli aday",
            icon="📥"
        )
    with col2:
        render_kpi_card(
            title="Konsültasyon Oranı",
            value=f"%{kpis['consultation_rate']:.1f}",
            subtext=f"<span class='positive'>{kpis['consultations']}</span> doktor görüşmesi",
            icon="🩺"
        )
    with col3:
        render_kpi_card(
            title="Tedaviye Başlayan",
            value=f"{kpis['treatment_starts']:,}",
            subtext="Ankara'da kesin tedavi",
            icon="🧬",
            is_highlight=True
        )
    with col4:
        render_kpi_card(
            title="Başvuru → Tedavi CVR",
            value=f"%{kpis['overall_conversion']:.1f}",
            subtext="Uçtan uca dönüşüm",
            icon="📈",
            is_highlight=True
        )
    with col5:
        render_kpi_card(
            title="Hasta Başı CAC",
            value=f"€{kpis['cac']:,.0f}",
            subtext=f"Toplam Harcama: €{kpis['total_spend']:,.0f}",
            icon="💶"
        )
    with col6:
        render_kpi_card(
            title="Uluslararası Gelir",
            value=f"€{kpis['total_revenue']:,.0f}",
            subtext=f"Ort. €{kpis['avg_revenue_per_patient']:,.0f} / vaka",
            icon="💎"
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 3. Main Row: Left Funnel Chart, Right Single-Country Granular Performance Table
    left_col, right_col = st.columns([1, 1.25])
    
    with left_col:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>🔻 Hasta Kazanım Hunisi ve Dönüşüm Aşamaları</span>
                <span class="tag">Gerçek Zamanlı</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">
                Başvuru aşamasından Ankara'da tedavi başlangıcına kadar hasta akışı ve kayıp analizleri
            </div>
        """, unsafe_allow_html=True)
        
        # Prepare Funnel Data
        total = kpis["total_inquiries"]
        qualified = kpis["qualified_leads"]
        consultations = kpis["consultations"]
        accepted = len(filtered_leads[filtered_leads["stage"].isin(["4. Treatment Plan Accepted", "5. Treatment Started - Ankara"])])
        treatment = kpis["treatment_starts"]
        
        funnel_data = [
            {"stage": "1. Yeni Başvuru", "value": total, "rate": 100.0},
            {"stage": "2. Nitelikli Başvuru", "value": qualified, "rate": (qualified/total*100) if total else 0},
            {"stage": "3. Doktor Konsültasyonu", "value": consultations, "rate": (consultations/total*100) if total else 0},
            {"stage": "4. Tedavi Planı Onayı", "value": accepted, "rate": (accepted/total*100) if total else 0},
            {"stage": "5. Tedavi Başlangıcı (Ankara)", "value": treatment, "rate": (treatment/total*100) if total else 0}
        ]
        
        fig_funnel = build_funnel_figure(funnel_data)
        st.plotly_chart(fig_funnel, use_container_width=True, config={'displayModeBar': False})
        
        # Quick drop-off callout
        lost_count = total - treatment
        st.markdown(f"""
        <div style="background: rgba(239, 68, 68, 0.08); border-left: 3px solid #EF4444; padding: 8px 12px; border-radius: 4px; font-size: 12px; color: #CBD5E1; margin-top: 4px;">
            ⚠️ <b>Dönüşüm Kaybı:</b> Toplam <b>{lost_count}</b> başvuru süreç içerisinde kaybedildi. En büyük kayıp <b>Konsültasyon → Tedavi Planı</b> aşamasında maliyet ve vize gerekçeleriyle yaşanıyor.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>🌍 Ülkelere Göre Hasta Performansı & Verimlilik</span>
                <span class="tag">Tekil Ülke Ayrımı</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">
                Her ülke bağımsız değerlendirilir; grup birleştirmesi yapılmaz (örn. Irak ve Ürdün ayrı tutulur).
            </div>
        """, unsafe_allow_html=True)
        
        country_df = get_country_performance_summary(filtered_leads, filtered_spend)
        
        if not country_df.empty:
            # Display formatted table
            display_df = country_df.copy()
            display_df["conversion_rate"] = display_df["conversion_rate"].apply(lambda x: f"%{x:.1f}")
            display_df["marketing_spend"] = display_df["marketing_spend"].apply(lambda x: f"€{x:,.0f}")
            display_df["cac"] = display_df["cac"].apply(lambda x: f"€{x:,.0f}")
            display_df["revenue"] = display_df["revenue"].apply(lambda x: f"€{x:,.0f}")
            
            display_df.rename(columns={
                "code": "Kod",
                "country": "Hedef Ülke",
                "inquiries": "Başvuru",
                "consultations": "Konsültasyon",
                "treatment_starts": "Tedavi",
                "conversion_rate": "Dönüşüm",
                "marketing_spend": "Harcama",
                "cac": "Hasta CAC",
                "revenue": "Gelir"
            }, inplace=True)
            
            st.dataframe(
                display_df[["Kod", "Hedef Ülke", "Başvuru", "Konsültasyon", "Tedavi", "Dönüşüm", "Harcama", "Hasta CAC", "Gelir"]],
                use_container_width=True,
                height=345,
                hide_index=True
            )
        else:
            st.info("Seçili filtre kriterlerine uygun ülke verisi bulunamadı.")
            
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. Bottom Section: Overdue Follow-ups & SLA Alerts + Approved Strategic Action Plans
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    bot_col1, bot_col2 = st.columns([1, 1.2])
    
    with bot_col1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>⏱️ Takibi Geciken Başvurular ve Sorumlular</span>
                <span class="tag" style="background: rgba(239, 68, 68, 0.2); color: #F87171;">Acil Aksiyon</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">
                İlk yanıt süresi SLA hedefi (4 saat) aşılmış veya kritik aşamada beklemede kalan uluslararası hasta kayıtları
            </div>
        """, unsafe_allow_html=True)
        
        overdue_df = get_overdue_tasks(filtered_leads)
        if not overdue_df.empty:
            overdue_view = overdue_df.copy()
            overdue_view["response_time_hrs"] = overdue_view["response_time_hrs"].apply(lambda x: f"{x:.1f} saat")
            overdue_view.rename(columns={
                "lead_id": "Kayıt No",
                "country": "Ülke",
                "language": "Dil",
                "coordinator": "Sorumlu",
                "response_time_hrs": "Yanıt Süresi",
                "stage": "Aşama"
            }, inplace=True)
            st.dataframe(
                overdue_view[["Kayıt No", "Ülke", "Dil", "Sorumlu", "Yanıt Süresi", "Aşama"]].head(6),
                use_container_width=True,
                height=220,
                hide_index=True
            )
        else:
            st.success("Tüm başvurular SLA hedefleri içerisinde yanıtlandı!")
            
        st.markdown("</div>", unsafe_allow_html=True)

    with bot_col2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>📋 Onaylanan Stratejik Eylem Planları (Aksiyon Takibi)</span>
                <span class="tag">Yönetim Kararları</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">
                Sorun / Fırsat → Dayanak Veri → Karar → Sorumlu → Son Tarih → Durum → Gerçekleşen Sonuç
            </div>
        """, unsafe_allow_html=True)
        
        # Display Action Plans with interactive expanders to prevent truncation
        for idx, row in actions_df.iterrows():
            status_color = "#10B981" if row["status"] == "Tamamlandı" else ("#00F0FF" if row["status"] == "Devam Ediyor" else "#F59E0B")
            with st.expander(f"📌 {row['issue_opportunity']} — [{row['status']}]"):
                c_a, c_b = st.columns(2)
                with c_a:
                    st.markdown(f"**📊 Dayanak Veri:**\n{row['evidence_data']}")
                    st.markdown(f"**🎯 Alınan Karar:**\n{row['decision']}")
                with c_b:
                    st.markdown(f"**👤 Sorumlu:** {row['owner']}")
                    st.markdown(f"**📅 Son Tarih:** `{row['deadline']}`")
                    st.markdown(f"**🚀 Gerçekleşen Sonuç / Durum:**\n{row['realized_result']}")
                    
        st.markdown("</div>", unsafe_allow_html=True)
