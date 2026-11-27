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
from modules.patient_crm import render_clinical_excel_charts, COUNTRY_NAME_TR_MAP

def render_executive_cockpit(filtered_leads, filtered_spend, actions_df, date_label, real_clinical_df=None):
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

    # Real Clinical Data Integration Verification Ribbon
    st.markdown("""
    <div style="background: linear-gradient(90deg, rgba(21, 115, 109, 0.4) 0%, rgba(14, 47, 59, 0.6) 100%); border: 1px solid rgba(0, 240, 255, 0.35); border-radius: 8px; padding: 10px 16px; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 18px;">🏥</span>
            <div>
                <span style="font-size: 13px; font-weight: 700; color: #FFFFFF;">Gerçek Klinik HBYS Veritabanı Entegre Edildi</span>
                <span style="font-size: 11px; color: #00F0FF; font-weight: 600; margin-left: 6px;">(yabancilar4.xlsx — tupbebex & witness)</span>
                <div style="font-size: 11px; color: #CBD5E1; margin-top: 2px;">
                    ✓ 1,382 Gerçek Siklus &nbsp;|&nbsp; ✓ 795 OPU İşlemi &nbsp;|&nbsp; ✓ 614 Embriyo Transferi &nbsp;|&nbsp; ✓ 58 Ülke &nbsp;|&nbsp; ✓ KVKK Madde 6 Maskeleme
                </div>
            </div>
        </div>
        <div style="display: flex; gap: 8px; align-items: center;">
            <span style="background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 3px 8px; border-radius: 5px; font-size: 11px; font-weight: 700;">
                ✓ 2016-2026 Aktif
            </span>
            <span style="background: rgba(0, 240, 255, 0.12); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.35); padding: 3px 8px; border-radius: 5px; font-size: 11px; font-weight: 600;">
                Modül 3'te Detaylı İncele ➔
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. Calculate 6 Core KPIs
    kpis = calculate_executive_kpis(filtered_leads, filtered_spend)
    
    # 2. Render 6 KPI Cards in a clean responsive grid
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        render_kpi_card(
            title="Toplam Siklus (Excel)",
            value=f"{kpis['total_inquiries']:,}",
            subtext=f"<span class='highlight'>{kpis['unique_patients']:,}</span> benzersiz hasta çifti",
            icon="📁"
        )
    with col2:
        opu_pct = (kpis['total_opu'] / kpis['total_inquiries'] * 100) if kpis['total_inquiries'] > 0 else 0
        render_kpi_card(
            title="Başarılı OPU (Excel)",
            value=f"{kpis['total_opu']:,}",
            subtext=f"<span class='positive'>%{opu_pct:.1f}</span> Yumurta Toplama",
            icon="🔬"
        )
    with col3:
        render_kpi_card(
            title="Embriyo Transferi",
            value=f"{kpis['total_transfers']:,}",
            subtext=f"{kpis['treatment_starts']:,} transfer siklusu",
            icon="🧬",
            is_highlight=True
        )
    with col4:
        render_kpi_card(
            title="Cerrahi & Spermiogram",
            value=f"{kpis['total_surgeries']:,}",
            subtext=f"{kpis['total_spermiograms']:,} Spermiogram analizi",
            icon="🩺",
            is_highlight=True
        )
    with col5:
        render_kpi_card(
            title="Ort. Kalış Süresi",
            value=f"{kpis['avg_stay_days']:.1f} Gün",
            subtext="Reklam Harcaması: €0 (Verilmedi)",
            icon="⏱️"
        )
    with col6:
        render_kpi_card(
            title="Tahmini Paket Cirosu",
            value=f"~€{kpis['total_revenue']:,.0f}",
            subtext="Model Tahmini (Excel'de Fatura Yok)",
            icon="💎"
        )

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # 3. Main Row: Left Funnel Chart, Right Single-Country Granular Performance Table
    left_col, right_col = st.columns([1, 1.35])
    
    with left_col:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>🔻 Klinik Süreç Hunisi (yabancilar4.xlsx)</span>
                <span class="tag">%100 Gerçek Veri</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">
                Excel'deki 1,382 gerçek klinik kaydın muayene, OPU ve Embriyo Transferi aşama dağılımı
            </div>
        """, unsafe_allow_html=True)
        
        # Prepare Funnel Data strictly from real clinical progression
        total = kpis["total_inquiries"]
        with_consult = len(filtered_leads[filtered_leads["stage"].isin(["2. Qualified Lead", "3. Medical Consultation", "4. Treatment Plan Accepted", "5. Treatment Started - Ankara"])])
        with_proc = len(filtered_leads[filtered_leads["stage"].isin(["3. Medical Consultation", "4. Treatment Plan Accepted", "5. Treatment Started - Ankara"])])
        accepted = len(filtered_leads[filtered_leads["stage"].isin(["4. Treatment Plan Accepted", "5. Treatment Started - Ankara"])])
        treatment = kpis["treatment_starts"]
        
        funnel_data = [
            {"stage": "1. Kayıtlı Toplam Siklus", "value": total, "rate": 100.0},
            {"stage": "2. Ön Tetkik / Androloji", "value": with_consult, "rate": (with_consult/total*100) if total else 0},
            {"stage": "3. Cerrahi / İleri Muayene", "value": with_proc, "rate": (with_proc/total*100) if total else 0},
            {"stage": "4. OPU (Yumurta Toplama) / Onay", "value": accepted, "rate": (accepted/total*100) if total else 0},
            {"stage": "5. Embriyo Transferi (Ankara)", "value": treatment, "rate": (treatment/total*100) if total else 0}
        ]
        
        fig_funnel = build_funnel_figure(funnel_data)
        st.plotly_chart(fig_funnel, use_container_width=True, config={'displayModeBar': False})
        
        # Quick callout
        freeze_or_pending = total - treatment
        st.markdown(f"""
        <div style="background: rgba(0, 240, 255, 0.08); border-left: 3px solid #00F0FF; padding: 8px 12px; border-radius: 4px; font-size: 12px; color: #CBD5E1; margin-top: 4px;">
            ℹ️ <b>Klinik Özet:</b> Excel'deki <b>{total:,}</b> gerçek döngüden <b>{treatment:,}</b> adedinde Embriyo Transferi gerçekleşmiş, <b>{freeze_or_pending:,}</b> kayıt dondurma/PGT bekleme veya ön teşhis aşamasındadır.
        </div>
        </div>
        """, unsafe_allow_html=True)

    with right_col:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>🌍 Excel'e Göre Ülke Sıralaması (En Çoktan En Aza)</span>
                <span class="tag">yabancilar4.xlsx (58 Ülke)</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">
                Yüklediğiniz Excel'deki gerçek hasta sayılarına göre en çoktan en aza sıralanmıştır. (Ülke bilgisi Excel'de boş girilen 458 kayıt tablo sonunda gösterilir.)
            </div>
        """, unsafe_allow_html=True)
        
        avail_yrs = sorted(filtered_leads["year"].dropna().astype(int).unique().tolist(), reverse=True) if "year" in filtered_leads.columns else []
        sel_table_years = st.multiselect(
            "📅 Ülke Sıralaması İçin Yıl Filtresi:",
            avail_yrs,
            default=None,
            placeholder="Tüm Yıllar (2016 - 2026)",
            key="cockpit_country_table_year_filter"
        )
        table_src = filtered_leads[filtered_leads["year"].isin(sel_table_years)] if sel_table_years else filtered_leads
        country_df = get_country_performance_summary(table_src, filtered_spend)
        
        if not country_df.empty:
            # Display formatted table with rank index
            display_df = country_df.copy()
            sira_vals = [str(i) if unk == 0 else "-" for i, unk in enumerate(display_df["is_unknown"].tolist(), 1)]
            display_df.insert(0, "Sıra", sira_vals)
            display_df["country"] = display_df["country"].apply(
                lambda c: f"{COUNTRY_NAME_TR_MAP[c]} ({c})" if c in COUNTRY_NAME_TR_MAP else c
            )
            display_df["conversion_rate"] = display_df["conversion_rate"].apply(lambda x: f"%{x:.1f}")
            display_df["revenue"] = display_df["revenue"].apply(lambda x: f"€{x:,.0f}")
            
            display_df.rename(columns={
                "code": "Kod",
                "country": "Ülke (Excel)",
                "inquiries": "Toplam Vaka",
                "opu_count": "OPU",
                "transfer_count": "Transfer (ET)",
                "surgery_count": "Cerrahi",
                "conversion_rate": "Transfer %",
                "revenue": "Tahmini Ciro (€)"
            }, inplace=True)
            
            st.dataframe(
                display_df[["Sıra", "Kod", "Ülke (Excel)", "Toplam Vaka", "OPU", "Transfer (ET)", "Cerrahi", "Transfer %", "Tahmini Ciro (€)"]],
                use_container_width=True,
                height=345,
                hide_index=True
            )
        else:
            st.info("Seçili filtre kriterlerine uygun ülke verisi bulunamadı.")
            
        st.markdown("</div>", unsafe_allow_html=True)

    # 3.5. Executive Real Clinical Visual Analytics (Top 15 Countries + Yearly Trend 2016-2026 + Stay Duration & Express NGS)
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    render_clinical_excel_charts(filtered_leads, key_prefix="cockpit")

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
