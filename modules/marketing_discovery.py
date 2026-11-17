"""
Module 4: Digital Marketing & Patient Discovery
Analyzes GA4 traffic, Google Search Console terms, Google Ads & Meta campaigns.
Focuses on clinical segmentation (PGT, Male Infertility, Repeated IVF Failures) to evaluate which channels produce actual treatments rather than empty clicks.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import THEME_COLORS, CLINICAL_SEGMENTS
from utils.components import render_kpi_card

def render_marketing_discovery(filtered_leads, filtered_spend):
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
            🎯 Dijital Pazarlama, Arama & Hasta Keşif Zekası
        </h2>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
            Salt tıklama veya form sayısı yerine; hangi dil, arama terimi ve medikal segmentin Ankara'da tedavi başlangıcı ürettiğini analiz edin
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_channel, tab_segments, tab_protocols, tab_lang = st.tabs([
        "📢 Kanal & Kampanya Verimliliği (Attribution)",
        "🧬 Medikal Segment Analizi (Genetik, PGT, ICSI)",
        "📋 Klinik Tedavi Protokolleri (Excel)",
        "🗣️ Dil & Pazar Keşfi (Arapça, Rusça, İngilizce)"
    ])

    with tab_channel:
        render_channel_performance(filtered_leads, filtered_spend)

    with tab_segments:
        render_clinical_segments(filtered_leads)

    with tab_protocols:
        render_protocols_performance(filtered_leads)

    with tab_lang:
        render_language_performance(filtered_leads)

def render_channel_performance(filtered_leads, filtered_spend):
    """Channel breakdown comparing spend, leads, consultations, and completed treatments"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>📊 Edinme Kanalları Başarı Matrisi</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Calculate channel metrics
    channel_data = []
    unique_channels = filtered_leads["channel"].unique()
    
    for ch in unique_channels:
        ch_leads = filtered_leads[filtered_leads["channel"] == ch]
        inquiries = len(ch_leads)
        consults = len(ch_leads[ch_leads["consultation_date"].notna()])
        starts = len(ch_leads[ch_leads["stage"] == "5. Treatment Started - Ankara"])
        cvr = (starts / inquiries * 100) if inquiries > 0 else 0
        revenue = ch_leads["revenue"].sum()
        
        # Spend estimation
        ch_spend = filtered_spend[filtered_spend["channel"].str.contains(ch[:6], na=False)]["spend_eur"].sum()
        if ch_spend == 0:
            ch_spend = inquiries * 45.0 # fallback organic attribution cost
        cac = (ch_spend / starts) if starts > 0 else 0
        
        channel_data.append({
            "channel": ch,
            "inquiries": inquiries,
            "consultations": consults,
            "treatment_starts": starts,
            "cvr": cvr,
            "spend": ch_spend,
            "cac": cac,
            "revenue": revenue
        })
        
    ch_df = pd.DataFrame(channel_data).sort_values(by="treatment_starts", ascending=False)
    
    c_chart, c_tbl = st.columns([1.2, 1])
    
    with c_chart:
        fig = px.bar(
            ch_df,
            x="channel",
            y=["inquiries", "consultations", "treatment_starts"],
            title="Kanala Göre Hacim Aşamaları",
            barmode="group",
            color_discrete_map={
                "inquiries": "#00B4D8",
                "consultations": "#8B5CF6",
                "treatment_starts": "#10B981"
            },
            labels={"value": "Hasta Sayısı", "channel": "Kanal", "variable": "Aşama"}
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1"),
            height=320,
            margin=dict(l=10, r=10, t=30, b=10),
            legend=dict(orientation="h", y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with c_tbl:
        disp_ch = ch_df.copy()
        disp_ch["cvr"] = disp_ch["cvr"].apply(lambda x: f"%{x:.1f}")
        disp_ch["spend"] = disp_ch["spend"].apply(lambda x: f"€{x:,.0f}")
        disp_ch["cac"] = disp_ch["cac"].apply(lambda x: f"€{x:,.0f}")
        disp_ch["revenue"] = disp_ch["revenue"].apply(lambda x: f"€{x:,.0f}")
        
        st.dataframe(
            disp_ch.rename(columns={
                "channel": "Kanal", "inquiries": "Başvuru", "consultations": "Konsültasyon",
                "treatment_starts": "Tedavi", "cvr": "Dönüşüm", "spend": "Harcama", "cac": "CAC", "revenue": "Gelir"
            }),
            use_container_width=True,
            height=320,
            hide_index=True
        )
        
    st.markdown("</div>", unsafe_allow_html=True)

def render_clinical_segments(filtered_leads):
    """Clinical condition and specialty segmentation performance"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🧬 Medikal Segment Ayrımı: PGT, Androloji & Başarısız Tüp Bebek</span>
            <span class="tag">Diferansiyasyon</span>
        </div>
        <div style="font-size: 13px; color: #94A3B8; margin-bottom: 14px;">
            GEN-ART'ın akredite genetik laboratuvarı ve karmaşık vaka uzmanlığı jenerik IVF kliniklerinden ayrışmanın anahtarıdır.
        </div>
    """, unsafe_allow_html=True)
    
    seg_stats = filtered_leads.groupby("clinical_segment").agg(
        toplam_basvuru=("lead_id", "count"),
        tedavi_baslangici=("stage", lambda x: (x == "5. Treatment Started - Ankara").sum()),
        toplam_gelir=("revenue", "sum")
    ).reset_index()
    
    seg_stats["donusum_orani"] = (seg_stats["tedavi_baslangici"] / seg_stats["toplam_basvuru"] * 100).round(1)
    seg_stats["hasta_basi_gelir"] = (seg_stats["toplam_gelir"] / seg_stats["tedavi_baslangici"]).fillna(0).round(0)
    
    fig = px.scatter(
        seg_stats,
        x="donusum_orani",
        y="hasta_basi_gelir",
        size="tedavi_baslangici",
        color="clinical_segment",
        text="clinical_segment",
        title="Medikal Segment Matrisi (Dönüşüm Oranı vs. Hasta Başı Gelir)",
        labels={"donusum_orani": "Tedaviye Dönüşüm Oranı (%)", "hasta_basi_gelir": "Hasta Başı Ortalama Gelir (€)"}
    )
    fig.update_traces(textposition='top center')
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1"),
        height=380,
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_protocols_performance(filtered_leads):
    """Clinical IVF Treatment Protocol breakdown (Extracted from IVF SÜREÇLERİ.xlsx)"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>📋 IVF Tedavi Protokolleri Dağılımı (Klinik Süreçler)</span>
            <span class="tag">IVF SÜREÇLERİ.xlsx</span>
        </div>
        <div style="font-size: 13px; color: #94A3B8; margin-bottom: 14px;">
            Ankara'da kesin tedaviye başlayan hastaların uygulanan 4 ana klinik protokole göre dağılımı, vaka gelirleri ve ortalama kalış süreleri
        </div>
    """, unsafe_allow_html=True)
    
    treatment_leads = filtered_leads[filtered_leads["stage"] == "5. Treatment Started - Ankara"]
    
    proto_stats = treatment_leads.groupby("treatment_type").agg(
        hasta_sayisi=("lead_id", "count"),
        toplam_gelir=("revenue", "sum")
    ).reset_index().sort_values(by="hasta_sayisi", ascending=False)
    
    proto_stats["hasta_basi_gelir"] = (proto_stats["toplam_gelir"] / proto_stats["hasta_sayisi"]).round(0)
    
    c1, c2 = st.columns([1.2, 1])
    
    with c1:
        fig_bar = px.bar(
            proto_stats,
            x="treatment_type",
            y="hasta_sayisi",
            color="treatment_type",
            title="Tedaviye Başlayan Hastaların Protokol Tercihi",
            labels={"treatment_type": "Klinik Protokol", "hasta_sayisi": "Hasta Sayısı"},
            color_discrete_sequence=["#00F0FF", "#10B981", "#8B5CF6", "#00B4D8"]
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            height=320,
            showlegend=False,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with c2:
        disp_p = proto_stats.copy()
        disp_p["toplam_gelir"] = disp_p["toplam_gelir"].apply(lambda x: f"€{x:,.0f}")
        disp_p["hasta_basi_gelir"] = disp_p["hasta_basi_gelir"].apply(lambda x: f"€{x:,.0f}")
        
        st.dataframe(
            disp_p.rename(columns={
                "treatment_type": "Protokol Adı",
                "hasta_sayisi": "Vaka Sayısı",
                "toplam_gelir": "Toplam Ciro (€)",
                "hasta_basi_gelir": "Hasta Başı Ciro (€)"
            }),
            use_container_width=True,
            height=320,
            hide_index=True
        )
    st.markdown("</div>", unsafe_allow_html=True)

def render_language_performance(filtered_leads):
    """Language efficiency breakdown (Arabic vs Russian vs English vs Turkish)"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🗣️ Dil Bazlı Hasta Akışı ve Talep Analizi</span>
        </div>
    """, unsafe_allow_html=True)
    
    lang_stats = filtered_leads.groupby("language").agg(
        basvuru=("lead_id", "count"),
        tedavi=("stage", lambda x: (x == "5. Treatment Started - Ankara").sum()),
        gelir=("revenue", "sum"),
        ort_yanit_suresi=("response_time_hrs", "mean")
    ).reset_index().sort_values(by="tedavi", ascending=False)
    
    lang_stats["donusum"] = (lang_stats["tedavi"] / lang_stats["basvuru"] * 100).round(1)
    lang_stats["ort_yanit_suresi"] = lang_stats["ort_yanit_suresi"].round(1)
    
    c1, c2 = st.columns([1, 1.2])
    with c1:
        fig_pie = px.pie(
            lang_stats,
            names="language",
            values="tedavi",
            hole=0.4,
            title="Tedaviye Başlayan Hastaların Dil Dağılımı",
            color_discrete_sequence=["#00F0FF", "#10B981", "#8B5CF6", "#F59E0B", "#EC4899"]
        )
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1"),
            height=300,
            margin=dict(l=10, r=10, t=30, b=10)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with c2:
        st.dataframe(
            lang_stats.rename(columns={
                "language": "İletişim Dili",
                "basvuru": "Başvuru",
                "tedavi": "Tedavi Başlangıcı",
                "gelir": "Gelir (€)",
                "ort_yanit_suresi": "Ort. Yanıt (Saat)",
                "donusum": "Dönüşüm (%)"
            }),
            use_container_width=True,
            height=300,
            hide_index=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
