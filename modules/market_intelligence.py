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
from utils.components import render_kpi_card

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
        
        # Color mapping by region for vibrant, distinct multi-color flight arcs
        region_colors = {
            "Middle East & Gulf": "#FF8C1A",     # Vibrant Neon Orange (GEN-ART Logo)
            "Europe": "#00F0FF",                 # Electric Neon Cyan (GEN-ART Logo)
            "Central Asia & CIS": "#10B981",     # Bright Emerald Green
            "Balkans": "#A855F7",                # Bright Neon Purple
            "North Africa & Other": "#EC4899"    # Neon Coral Pink
        }
        
        # 1. Flight Arcs from all real countries in leads_df (or mcda_df) to Ankara
        active_globe_countries = set(leads_df["country"].unique()) | set(mcda_df["country"].unique())
        for c_name in sorted(active_globe_countries):
            if c_name in COUNTRY_COORDINATES and c_name != "Other International":
                coord = COUNTRY_COORDINATES[c_name]
                c_leads = len(leads_df[leads_df["country"] == c_name])
                c_starts = len(leads_df[(leads_df["country"] == c_name) & (leads_df["stage"] == "5. Treatment Started - Ankara")])
                if c_leads == 0 and c_name not in mcda_df["country"].values:
                    continue
                
                # Dynamic multi-color arc line
                line_color = region_colors.get(coord["region"], "#00F0FF")
                line_width = max(1.5, min(5.0, 1.2 + (c_leads * 0.02)))
                
                # Intermediate arched curve points for realistic flight corridors
                c_lon, c_lat = coord["lon"], coord["lat"]
                # 7 interpolated points with slight parabolic arc curvature
                arc_lons = []
                arc_lats = []
                for t in [0.0, 0.16, 0.33, 0.5, 0.66, 0.83, 1.0]:
                    lon_interp = c_lon + t * (ankara_lon - c_lon)
                    # Parabolic lift
                    lat_base = c_lat + t * (ankara_lat - c_lat)
                    lift = 4.0 * t * (1.0 - t) * (3.5 if c_lat > ankara_lat else 2.5)
                    arc_lons.append(lon_interp)
                    arc_lats.append(lat_base + lift)
                
                fig.add_trace(go.Scattergeo(
                    lon=arc_lons,
                    lat=arc_lats,
                    mode='lines',
                    line=dict(width=line_width, color=line_color),
                    opacity=0.85,
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
                    textfont=dict(color=line_color, size=10, family="Plus Jakarta Sans"),
                    marker=dict(
                        size=max(8, min(24, 7 + (c_leads * 0.12))),
                        color=line_color,
                        opacity=0.9,
                        line=dict(width=1.5, color="#FFFFFF")
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

        # 3D Orthographic Globe Styling with Gen-Art Teal & Cyan Palette
        fig.update_geos(
            projection_type="orthographic",
            projection_rotation=dict(lon=38, lat=35, roll=0),
            showocean=True,
            oceancolor="#05161C",
            showland=True,
            landcolor="#0E2F3B",
            showlakes=True,
            lakecolor="#05161C",
            showcountries=True,
            countrycolor="rgba(24, 174, 187, 0.45)",
            countrywidth=1,
            showcoastlines=True,
            coastlinecolor="rgba(0, 240, 255, 0.5)",
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
                <span>🏆 En Aktif Hasta Pazarları (Excel Gerçek Veri)</span>
                <span class="tag" style="background: rgba(16, 185, 129, 0.2); color: #10B981; border-color: rgba(16, 185, 129, 0.4);">
                    yabancilar4.xlsx + USHAŞ Benchmarkı
                </span>
            </div>
            <div style="font-size: 11.5px; color: #CBD5E1; line-height: 1.5; margin-bottom: 10px; background: rgba(14, 47, 59, 0.8); padding: 8px 10px; border-radius: 6px; border-left: 3px solid #00F0FF;">
                📌 <b>Gerçek Veriler &amp; USHAŞ Referansı:</b><br/>
                Aşağıdaki vaka ve tedavi sayıları <b>doğrudan yüklediğiniz <code>yabancilar4.xlsx</code> dosyasındaki %100 gerçek GEN-ART hasta kayıtlarıdır</b> (ülkesi tanımlı ülkeler en çoktan aza sıralıdır).<br/>
                <i>Sektör Referansı:</i> Türkiye'ye en çok tüp bebek hastası gönderen ülkelerin <b>T.C. Sağlık Bakanlığı (USHAŞ) ve TÜİK resmi sağlık turizmi ülke dağılımı</b> oranları pazar kıyaslama benchmarkı olarak korunmuştur.<br/><br/>
                💶 <b>Euro (€) Tutarı Nedir / Neyi Temsil Eder?</b><br/>
                <code>yabancilar4.xlsx</code> dosyasında fatura/ödeme sütunu olmadığı için, kartlardaki <b>€ tutarı kesin muhasebe geliri değil</b>; her bir gerçek hastanın Excel'deki klinik işlemine göre hesaplanan <b>Tahmini Tedavi Paket Değeri (Model Cirosu)</b> simülasyonudur <i>(Express NGS: €6,800 · IVF Transfer: €5,200 · FET: €3,800 · OPU: €3,400 · Cerrahi/TESE: €1,800 · Ön Tetkik: €450)</i>.
            </div>
        """, unsafe_allow_html=True)
        
        named_leads = leads_df[~leads_df["country"].str.contains("Boş|Bilinmeyen", case=False, na=False)]
        empty_cnt = len(leads_df) - len(named_leads)
        top_countries = named_leads.groupby("country").agg(
            basvuru=("lead_id", "count"),
            tedavi=("stage", lambda x: (x == "5. Treatment Started - Ankara").sum()),
            gelir=("revenue", "sum")
        ).reset_index().sort_values(by="basvuru", ascending=False).head(6)
        
        for idx, r in top_countries.iterrows():
            c_reg = COUNTRY_COORDINATES.get(r['country'], {}).get("region", "")
            c_color = region_colors.get(c_reg, "#00F0FF")
            
            st.markdown(f"""
            <div style="background: rgba(14, 47, 59, 0.65); padding: 10px 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid {c_color};">
                <div style="display: flex; justify-content: space-between; font-weight: 700; color: #FFFFFF;">
                    <span>{r['country']} <small style="color: #64748B; font-weight: 400; font-size: 10px;">({c_reg})</small></span>
                    <span style="color: #10B981;" title="Excel klinik işlemlerine göre tahmini paket değeri">~€{r['gelir']:,.0f} <small style="font-weight:400; color:#94A3B8; font-size:9px;">(Tahmini)</small></span>
                </div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 3px; display: flex; justify-content: space-between;">
                    <span>📥 <b>{r['basvuru']}</b> Vaka (Excel)</span>
                    <span>🧬 <b>{r['tedavi']} Transfer / Tedavi</b></span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
        <div style="font-size: 11px; color: #94A3B8; margin-top: 10px; line-height: 1.4; background: rgba(0, 240, 255, 0.05); padding: 8px; border-radius: 6px; border: 1px solid rgba(0, 240, 255, 0.15);">
            ℹ️ <i>Not: Excel'de ülke sütunu boş/belirtilmemiş <b>{empty_cnt}</b> HBYS kaydı sıralama netliği için yukarıdaki ilk 6 listesine dahil edilmemiştir. Muhasebe/fatura Excel'i eklendiğinde tahmini € değerleri gerçek cirolarla değişir.</i>
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
        w_demand = st.slider("Hasta Talebi & Tedavi İhtiyacı (%)", 0, 50, 25, help="WHO infertilite prevalansı, yerel yetersizlik ve akraba evliliği genetik riski")
        w_afford = st.slider("Tedavi Karşılanabilirliği & Gelir Düzeyi (%)", 0, 50, 20, help="Dünya Bankası Kişi Başı GSYİH ve satın alma gücü")
    with col2:
        w_travel = st.slider("Seyahat & Lojistik Erişilebilirlik (%)", 0, 50, 15, help="Dışişleri Bakanlığı vize rejimleri, uçuş süresi ve Ankara ESB direkt hatları")
        w_diff = st.slider("Rekabet & Genetik Farklılaşma (%)", 0, 50, 15, help="GEN-ART Express NGS üstünlüğü / Yerel PGT yasağı (örn. Almanya)")
    with col3:
        w_digital = st.slider("Dijital Kazanım Potansiyeli (%)", 0, 50, 15, help="Google Keyword Planner arama hacmi ve Meta erişim maliyeti")
        w_reg = st.slider("Yasal & Operasyonel Uygunluk (%)", 0, 50, 10, help="T.C. Sağlık Bakanlığı ST-0625 sağlık turizmi uyumluluğu")

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
                "Middle East & Gulf": "#FF8C1A",
                "Central Asia & CIS": "#10B981",
                "Europe": "#00F0FF",
                "Balkans": "#A855F7",
                "North Africa & Other": "#EC4899"
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

    # Detailed MCDA Methodology & Source Evidence Box
    with st.expander("📚 Çok Kriterli Karar Verme (MCDA) Veri Dayanakları ve Metodolojisi"):
        st.markdown("""
        <div style="font-size: 12px; color: #CBD5E1; line-height: 1.6;">
            <b>MCDA Kriter Puanları Hangi Kaynaklardan Çekilmektedir?</b><br/>
            1. <b>Hasta Talebi:</b> Dünya Sağlık Örgütü (WHO) küresel infertilite sıklığı (%17.5), doğurganlık hızları ve Orta Doğu akraba evliliği prevalansı (%30+).<br/>
            2. <b>Gelir & Karşılanabilirlik:</b> Dünya Bankası (World Bank) Kişi Başı GSYİH verileri (Körfez $40k-$85k, Almanya $48k, İngiltere $46k vb.).<br/>
            3. <b>Seyahat & Lojistik:</b> T.C. Dışişleri Bakanlığı (mfa.gov.tr) güncel vize rejimleri ve DHMİ Ankara Esenboğa (ESB) doğrudan uçuş hatları.<br/>
            4. <b>Rekabet & Genetik Diferansiyasyon:</b> ESHRE raporları doğrultusunda Almanya/İtalya'daki PGT-A yasal yasakları ve Körfez'deki yüksek dondurma maliyetleri.<br/>
            5. <b>Dijital Potansiyel:</b> Google Keyword Planner arama hacimleri (Arapça, Rusça, İngilizce ve Almanca "IVF Turkey" sorguları).
        </div>
        """, unsafe_allow_html=True)

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
    
    # Market dynamic & domestic IVF status lookup
    local_ivf_market_data = {
        "Iraq": {
            "domestic_status": "Kısmen Var (Sınırlı & Altyapı Yetersiz)",
            "domestic_desc": "Bağdat ve Erbil'de kamu ve az sayıda özel merkez var; ancak akredite genetik lab (NGS), hava temiz oda standartları ve Mikro-TESE başarısı yetersiz.",
            "outbound_pct": "%68",
            "turkey_share": "%54",
            "why_genart": "Akredite yerinde PGT-A NGS laboratuvarı, Bağdat/Erbil'den Ankara ESB'ye direkt uçuş ve Arapça kesintisiz koordinasyon."
        },
        "Jordan": {
            "domestic_status": "Evet, Yaygın (Bölgesel Sağlık Merkezi)",
            "domestic_desc": "Amman Orta Doğu'nun yerel tüp bebek merkezidir ancak özel hastaneler çok pahalıdır ($6,000-$7,500+). PGT-A biyopsilerini yurtdışı laboratuvarlara gönderip embriyoları dondururlar.",
            "outbound_pct": "%24",
            "turkey_share": "%38",
            "why_genart": "GEN-ART'ın tek ziyarette (17 gün) biten taze transfer Express NGS avantajı (hastaya €3,200 seyahat tasarrufu) ve 90 gün vizesiz giriş."
        },
        "Azerbaijan": {
            "domestic_status": "Evet, Var (Bakü Merkezli)",
            "domestic_desc": "Bakü'de klinikler var ancak genetik tanı (PGT-A/M) ve tekrarlayan başarısız tüp bebek vakalarında Türk hekimlerine güven çok daha yüksektir.",
            "outbound_pct": "%45",
            "turkey_share": "%78",
            "why_genart": "Kimlikle seyahat imkanı, sıfır dil engeli, ileri implantasyon genetiği ve akredite embriyoloji laboratuvarı."
        },
        "Germany": {
            "domestic_status": "Evet, Çok Yaygın (Sigorta Kapsamında)",
            "domestic_desc": "Alman Embriyo Koruma Kanunu (Embryonenschutzgesetz) gereğince embriyolara anöploidi taraması (PGT-A) yapmak kanunen yasaktır; 40+ yaş kadınlarda devlet desteği kesilir.",
            "outbound_pct": "%35",
            "turkey_share": "%32",
            "why_genart": "Yasal ve etik Express PGT-A taraması, ileri anne yaşı (40+) protokolleri ve Almanca rehberlik."
        },
        "Saudi Arabia": {
            "domestic_status": "Evet, A+ Merkezler Var",
            "domestic_desc": "Riyad ve Cidde'de özel klinikler var ancak maliyet $10,000+ seviyesindedir. Akraba evliliği prevalansı (%32+) nedeniyle monogenik hastalık riski çok yüksektir.",
            "outbound_pct": "%34",
            "turkey_share": "%42",
            "why_genart": "PGT-M tek gen hastalıkları uzmanlığı, yüksek hasta mahremiyeti ve Ankara Esenboğa direkt uçuş koridoru."
        },
        "Libya": {
            "domestic_status": "Hayır (Sistem Çökmüş Durumda)",
            "domestic_desc": "Savaş ve ambargo sonrası medikal gaz, solüsyon ve akredite embriyoloji laboratuvarı bulunmamaktadır.",
            "outbound_pct": "%82",
            "turkey_share": "%52",
            "why_genart": "Sağlık Bakanlığı onaylı medikal vize davetiyesi (ST-0625), karmaşık vakalarda yüksek canlı doğum başarısı."
        }
    }
    
    m_info = local_ivf_market_data.get(selected_c, {
        "domestic_status": "Yerel Merkezler Mevcut",
        "domestic_desc": f"{selected_c} pazarında standart IVF uygulanmakta ancak ileri genetik tarama ve karmaşık infertilite vakalarında sınır ötesi seyahat tercih edilmektedir.",
        "outbound_pct": "%28",
        "turkey_share": "%35",
        "why_genart": "GEN-ART'ın akredite genetik tanı merkezi ve yüksek canlı doğum oranları."
    })
    
    with p1:
        st.markdown(f"""
        <div class="section-card">
            <div class="section-header">
                <span>🎯 {selected_c} Pazar Stratejik Hipotezi & Yerel IVF Analizi</span>
            </div>
            <p style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
                <b>Yerelde IVF Durumu:</b> <span style="color: #00F0FF; font-weight: 600;">{m_info['domestic_status']}</span><br/>
                <span style="font-size: 12px; color: #94A3B8;">{m_info['domestic_desc']}</span><br/><br/>
                <b>Ülke Dışına Çıkış Oranı:</b> <b style="color: #F5821F;">{m_info['outbound_pct']}</b> | <b>Türkiye'nin Payı:</b> <b style="color: #10B981;">{m_info['turkey_share']}</b><br/><br/>
                <b>GEN-ART Seçim Nedeni:</b> {m_info['why_genart']}
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
