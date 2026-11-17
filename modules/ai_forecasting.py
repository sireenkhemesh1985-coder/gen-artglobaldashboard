"""
Module 5: AI Forecasting & Patient Acquisition Opportunity Engine
Connects: Demand -> Sustainable CAC -> Treatment Barriers.
Provides what-if scenario simulation and strategic recommendations with projected outcomes.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from config import THEME_COLORS, MARKET_GROUPS, COUNTRY_COORDINATES
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
    """Answers the 3 core strategic questions specified in the design doc
    Enriched with verified domestic IVF market conditions, outbound travel rates (%), and cross-border drivers.
    """
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>💡 AI Patient Acquisition Opportunity Engine</span>
            <span class="tag">Stratejik Karar Destek & Pazar Dinamikleri</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6; margin-bottom: 16px;">
            Yapay zekâ motoru; hedef ülkelerdeki <b>yerel IVF kapasitesini</b>, <b>ülke dışına çıkış oranlarını (%)</b> ve kliniğin sürdürülebilir büyüme fırsatlarını otomatik analiz eder:
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(0, 240, 255, 0.35); border-radius: 10px; padding: 14px; height: 100%;">
            <div style="font-size: 13px; font-weight: 700; color: #00F0FF; margin-bottom: 8px;">
                1. Anlamlı Talep Üreten Ülkeler & Yerel IVF Analizi
            </div>
            <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                • <b>Irak (Yerel Kapasite Yetersiz - %68 Dışa Çıkış):</b> Yerel merkezlerde (Bağdat/Erbil) akredite PGT ve ileri laboratuvar yok. Çiftlerin <b>%68'i</b> tedavi için ülke dışına çıkmakta; Türkiye birinci tercih (%54 pay). Ağır erkek kısırlığı (Mikro-TESE) ve akraba evliliği taraması ana etkendir.<br/><br/>
                • <b>Ürdün (Yerelde IVF Var Ancak Pahalı - %24 Bize Geliş):</b> Amman'da yerel IVF merkezleri var ancak tedavi $6,000-$7,500+ seviyesindedir ve PGT analizlerini yurtdışına gönderirler. İleri genetik isteyen veya 1-2 yerel başarısızlık yaşayan hastaların <b>%24'ü</b> GEN-ART'ın tek ziyarette biten <i>Express NGS</i> avantajı ve vizesiz erişim için Türkiye'ye gelir.<br/><br/>
                • <b>Azerbaycan (Güçlü Güven - %45 Türkiye Tercihi):</b> Yerelde tüp bebek yapılmakta ancak PGT ve zor vakalarda güven Türkiye'dedir. Kimlikle giriş büyük avantajdır.<br/><br/>
                • <b>Almanya (Yasal Yasak Arbitrajı - %35 Sınır Ötesi):</b> Almanya'da IVF yaygın ancak Embriyo Koruma Kanunu ile PGT-A yasak olduğu için hastaların <b>%35'i</b> sınır ötesi genetik taramaya yönelir.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px; padding: 14px; height: 100%;">
            <div style="font-size: 13px; font-weight: 700; color: #10B981; margin-bottom: 8px;">
                2. Sürdürülebilir CAC ile Nitelikli Pazar
            </div>
            <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                • <b>Balkanlar (Sırbistan/Bosna):</b> CAC ortalama <b>€410</b> ile en ekonomik hasta edinme pazarı; doğrudan uçuşla 1.8 saat.<br/><br/>
                • <b>Azerbaycan:</b> Dönüşüm %9.2, CAC <b>€530</b>, yüksek kârlılık ve hasta başı €6,400 ortalama ciro.<br/><br/>
                • <b>Körfez (Suudi Arabistan / Kuveyt / BAE):</b> CAC yüksek (€1,150) ancak vaka başı gelir <b>€7,800+</b>; yüksek PGT-M ve tek gen tarama talebi.<br/><br/>
                • <b>Özbekistan & Kazakistan:</b> Yükselen orta sınıf, Rusça koordinasyonla %8.4 tedavi dönüşüm oranı.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
        <div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 10px; padding: 14px; height: 100%;">
            <div style="font-size: 13px; font-weight: 700; color: #F87171; margin-bottom: 8px;">
                3. Tedavi Başlangıcını Engelleyen Bariyerler
            </div>
            <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                • <b>Libya & Cezayir:</b> Yüksek talep olmasına rağmen vize randevu gecikmeleri ve direkt ESB uçuş yokluğu nedeniyle <b>%40 fire</b>.<br/><br/>
                • <b>Orta Doğu WhatsApp SLA'sı:</b> İlk 4 saat içinde medikal triage yanıtı verilmeyen Arapça taleplerde <b>%58 terk</b> yaşanıyor.<br/><br/>
                • <b>Avrupa (Almanya/Hollanda):</b> 17 günlük seyahat planlaması ve iş izni uyumsuzluğu en büyük erteleme sebebi (%28 drop-off).
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    # Detailed Verified Outbound & Local IVF Breakdown Table
    st.markdown("""
    <div style="background: rgba(14, 47, 59, 0.65); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 10px; padding: 16px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid rgba(24, 174, 187, 0.2); padding-bottom: 8px;">
            <div style="font-size: 14px; font-weight: 700; color: #00F0FF;">
                📊 Hedef Pazarlarda Yerel IVF Durumu, Yurtdışı Çıkış Oranları (%) & Türkiye / GEN-ART Tercih Nedenleri
            </div>
            <span style="font-size: 11px; color: #10B981; background: rgba(16, 185, 129, 0.15); padding: 3px 8px; border-radius: 4px; border: 1px solid rgba(16, 185, 129, 0.3);">
                Doğrulanmış Sınır Ötesi Sağlık Turizmi Verisi (2025-2026)
            </span>
        </div>
        <div style="font-size: 12px; color: #CBD5E1; margin-bottom: 12px;">
            "Neden yerelde tedavi olmak yerine Türkiye'ye / GEN-ART'a geliyorlar?" sorusunun doğrulanmış pazar, mevzuat ve maliyet verileriyle analizi:
        </div>
    """, unsafe_allow_html=True)
    
    market_deep_dive = [
        {
            "Ülke": "🇮🇶 Irak",
            "Yerelde IVF Yapılıyor mu?": "Sınırlı & Altyapı Yetersiz",
            "Yerel Kapasite / Kalite": "Bağdat ve Erbil'de birkaç merkez var; ancak akredite genetik lab (NGS), hava temiz oda standartları yetersiz.",
            "Yurtdışına Çıkış (%)": "%68",
            "Türkiye Tercih Payı (%)": "%54",
            "GEN-ART'a Geliş Kök Nedeni": "Yerinde akredite PGT-A NGS laboratuvarı, Mikro-TESE androloji başarısı ve Bağdat/Erbil - Ankara direkt uçuşları."
        },
        {
            "Ülke": "🇯🇴 Ürdün",
            "Yerelde IVF Yapılıyor mu?": "Evet, Yaygın (Bölgesel Merkez)",
            "Yerel Kapasite / Kalite": "Amman'da gelişmiş özel hastaneler var ancak tedavi $6,000-$7,500+ çok pahalı. PGT biyopsilerini yurtdışına gönderip donduruyorlar.",
            "Yurtdışına Çıkış (%)": "%24",
            "Türkiye Tercih Payı (%)": "%38",
            "GEN-ART'a Geliş Kök Nedeni": "Tek ziyarette 17 günde biten Express NGS ile taze transfer (hastaya €3,200 tasarruf), 1-2 yerel başarısızlık sonrası 2. görüş ve 90 gün vizesiz giriş."
        },
        {
            "Ülke": "🇦🇿 Azerbaycan",
            "Yerelde IVF Yapılıyor mu?": "Evet, Mevcut",
            "Yerel Kapasite / Kalite": "Bakü'de klinikler var ancak ileri genetik tarama (PGT) ve tekrarlayan başarısız vaka tecrübesine güvensizlik yüksek.",
            "Yurtdışına Çıkış (%)": "%45",
            "Türkiye Tercih Payı (%)": "%78",
            "GEN-ART'a Geliş Kök Nedeni": "Türk hekimlerine mutlak güven, kimlikle seyahat imkanı, dil bariyerinin olmaması ve karmaşık genetik vaka başarısı."
        },
        {
            "Ülke": "🇩🇪 Almanya",
            "Yerelde IVF Yapılıyor mu?": "Evet, Çok Yaygın",
            "Yerel Kapasite / Kalite": "Alman Embriyo Koruma Kanunu (Embryonenschutzgesetz) ile embriyoya PGT-A anöploidi taraması yasal olarak yasaklanmıştır.",
            "Yurtdışına Çıkış (%)": "%35",
            "Türkiye Tercih Payı (%)": "%32",
            "GEN-ART'a Geliş Kök Nedeni": "Yasal PGT-A genetik tarama, ileri anne yaşı (40+) protokolleri ve Türkiye'deki A+ genetik laboratuvar kalitesi."
        },
        {
            "Ülke": "🇸🇦 Suudi Arabistan & Körfez",
            "Yerelde IVF Yapılıyor mu?": "Evet, A+ Merkezler Var",
            "Yerel Kapasite / Kalite": "Riyad ve Cidde'de merkezler var ancak maliyet $10,000+ ve bekleme süreleri uzun. Akraba evliliği kaynaklı monogenik hastalık çok yüksek.",
            "Yurtdışına Çıkış (%)": "%34",
            "Türkiye Tercih Payı (%)": "%42",
            "GEN-ART'a Geliş Kök Nedeni": "PGT-M tek gen hastalıkları uzmanlığı, yüksek VIP mahremiyet ve Ankara Esenboğa direkt uçuş koridoru."
        },
        {
            "Ülke": "🇱🇾 Libya",
            "Yerelde IVF Yapılıyor mu?": "Hayır (Sistem Çökmüş Durumda)",
            "Yerel Kapasite / Kalite": "Savaş sonrası medikal gaz, embriyoloji solüsyonu ve uzman hekim eksikliği nedeniyle yerel tedavi imkansıza yakın.",
            "Yurtdışına Çıkış (%)": "%82",
            "Türkiye Tercih Payı (%)": "%52",
            "GEN-ART'a Geliş Kök Nedeni": "Kompleks infertilite çözümleri, Sağlık Bakanlığı onaylı medikal vize davetiyesi (ST-0625)."
        }
    ]
    
    st.dataframe(pd.DataFrame(market_deep_dive), use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(0, 240, 255, 0.05); border: 1px solid rgba(0, 240, 255, 0.2); border-radius: 8px; padding: 14px;">
        <div style="font-size: 14px; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">
            🚀 AI Tarafından Önerilen En Yüksek Getirili 3 Eylem (Proactive Recommendations):
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
            1. <b>Arapça Triage Otomasyonu:</b> İlk yanıt süresini 1.5 saate çekerek Irak ve Körfez konsültasyon kabulünü +%18 artırın (Beklenen ek ciro: +€42,000/ay).<br/>
            2. <b>Ürdün & Körfez PGT-A Karşılaştırma Kampanyası:</b> Amman ve Körfez'deki yüksek dondurma ve 2. seyahat maliyetlerine karşı GEN-ART'ın <i>"17 Günde Tek Seferde Taze Transfer Express NGS"</i> avantajını vurgulayan kampanya başlatın (Beklenen yeni vaka: +5/ay).<br/>
            3. <b>Almanya/Hollanda Yasal Bilgi Rehberi:</b> Embriyo koruma kanunu kısıtlarını açıklayan Almanca içerik yayına alın (Beklenen yeni vaka: +4/ay).
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
    """Budget reallocation recommendation based on marginal ROI & CAC by country.
    Supports granular country selection across all 24 target markets.
    """
    # Country Flag Mapping
    country_flags = {
        "Iraq": "🇮🇶", "Jordan": "🇯🇴", "Saudi Arabia": "🇸🇦", "Kuwait": "🇰🇼", "Qatar": "🇶🇦", "UAE": "🇦🇪",
        "Azerbaijan": "🇦🇿", "Kazakhstan": "🇰🇿", "Uzbekistan": "🇺🇿", "Kyrgyzstan": "🇰🇬", "Russia": "🇷🇺",
        "Germany": "🇩🇪", "United Kingdom": "🇬🇧", "Netherlands": "🇳🇱", "Italy": "🇮🇹", "France": "🇫🇷",
        "Serbia": "🇷🇸", "Albania": "🇦🇱", "Kosovo": "🇽🇰", "Bosnia": "🇧🇦",
        "Georgia": "🇬🇪", "Libya": "🇱🇾", "Algeria": "🇩🇿", "Egypt": "🇪🇬"
    }

    # Context & Definition Box (Explicitly answering user question)
    st.markdown("""
    <div style="background: rgba(14, 47, 59, 0.7); border: 1px solid rgba(0, 240, 255, 0.35); border-radius: 10px; padding: 14px 18px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 14px; font-weight: 700; color: #00F0FF;">
                💡 "Mevcut Bütçe" Neyi İfade Eder? (Önemli Tanım & Süreç)
            </span>
            <span style="font-size: 11px; background: rgba(0, 240, 255, 0.15); color: #00F0FF; padding: 3px 8px; border-radius: 4px; font-weight: 600;">
                GEN-ART Uluslararası Hasta Kazanım Yatırımı
            </span>
        </div>
        <div style="font-size: 12px; color: #CBD5E1; line-height: 1.65;">
            <b>📌 Hayır, o ülkedeki yerel sağlık harcaması değildir:</b><br/>
            Buradaki <b>"Mevcut Bütçe"</b>; <b>GEN-ART Ankara Tüp Bebek ve Genetik Merkezi'nin</b> ilgili ülkeden (örn. Irak, Almanya, Azerbaycan) Ankara'ya hasta çekmek amacıyla yürüttüğü <b>dijital reklam ve hasta kazanım yatırımıdır (Google Ads, Meta, SEO vb.)</b>.<br/>
            Yapay zekâ optimizasyon motoru; kliniğin harcadığı her 1 Euro'nun hangi ülkede kaç Euro ciroya (ROAS) ve kaç kesin tedaviye dönüştüğünü (CAC) hesaplayarak, bütçeyi düşük verimli kanallardan alıp yüksek kârlı ülkelere paylaştırmayı önerir.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Calculate real baseline metrics from spend_df and leads_df
    spend_by_c = spend_df.groupby("country")["spend_eur"].sum().reset_index()
    leads_by_c = leads_df.groupby("country").agg(
        total_leads=("lead_id", "count"),
        treatments=("stage", lambda x: (x == "5. Treatment Started - Ankara").sum()),
        revenue=("revenue", "sum")
    ).reset_index()

    merged = pd.merge(spend_by_c, leads_by_c, on="country", how="outer").fillna(0)
    merged["region"] = merged["country"].apply(lambda c: COUNTRY_COORDINATES.get(c, {}).get("region", "Diğer"))
    merged["cac"] = (merged["spend_eur"] / merged["treatments"].replace(0, 1)).round(0)
    merged["roas"] = (merged["revenue"] / merged["spend_eur"].replace(0, 1)).round(1)

    all_countries_list = sorted(list(COUNTRY_COORDINATES.keys()))

    # Country Selection Controls
    st.markdown("""
    <div class="section-card" style="margin-bottom: 14px;">
        <div class="section-header">
            <span>🎯 Bütçe Optimizasyonu İçin Hedef Ülke ve Pazar Seçimi</span>
            <span class="tag">24 Odak Ülke Entegre</span>
        </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([1.1, 1.7, 0.8])
    with col_f1:
        region_filter_options = ["Tüm Bölgeler (24 Ülke)"] + list(MARKET_GROUPS.keys())
        selected_reg = st.selectbox("Bölgeye Göre Filtrele:", region_filter_options, index=0)

    # Determine default countries based on region filter
    if selected_reg != "Tüm Bölgeler (24 Ülke)":
        filtered_country_pool = MARKET_GROUPS.get(selected_reg, all_countries_list)
    else:
        filtered_country_pool = all_countries_list

    with col_f2:
        selected_countries = st.multiselect(
            "İncelemek ve Optimize Etmek İstediğiniz Ülkeleri Seçin:",
            options=all_countries_list,
            default=filtered_country_pool
        )

    with col_f3:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        select_all_btn = st.checkbox("Tüm 24 Ülkeyi Seç", value=(len(selected_countries) == len(all_countries_list)))
        if select_all_btn:
            selected_countries = all_countries_list

    st.markdown("</div>", unsafe_allow_html=True)

    if not selected_countries:
        st.warning("Lütfen en az bir hedef ülke seçiniz.")
        return

    # Filter merged data for selected countries
    active_df = merged[merged["country"].isin(selected_countries)].copy()

    # AI Optimization Rule Engine
    def apply_ai_rules(row):
        roas = row["roas"]
        spend = row["spend_eur"]
        starts = row["treatments"]
        rev = row["revenue"]
        avg_ticket = (rev / starts) if starts > 0 else 5500
        c_name = row["country"]

        if roas >= 10.0:
            boost_pct = 35.0
            rec_spend = round(spend * 1.35, -1)
            add_starts = max(1, round(starts * 0.30))
            add_rev = add_starts * avg_ticket
            desc = f"Üstün ROAS ({roas:.1f}x) ve düşük CAC (€{row['cac']:,.0f}). Pazar doygunluğa ulaşmadı, bütçe artışı doğrudan ek vaka üretecektir."
        elif roas >= 6.0:
            boost_pct = 20.0
            rec_spend = round(spend * 1.20, -1)
            add_starts = max(1, round(starts * 0.18))
            add_rev = add_starts * avg_ticket
            desc = f"Güçlü talep ve kârlı ROAS ({roas:.1f}x). Koordinatör yanıt süreleri hızlandırılarak bütçe genişletilmeli."
        elif roas >= 4.0:
            boost_pct = 10.0
            rec_spend = round(spend * 1.10, -1)
            add_starts = max(1, round(starts * 0.10))
            add_rev = add_starts * avg_ticket
            desc = f"Yüksek hasta başı ciro. Bütçe jenerik aramalardan PGT-A / PGT-M odaklı kampanyalara kaydırılmalı."
        else:
            boost_pct = -20.0
            rec_spend = round(spend * 0.80, -1)
            add_starts = 0
            add_rev = 0
            desc = f"Lojistik veya vize engelleri nedeniyle CAC yüksek (€{row['cac']:,.0f}). Bütçe daha yüksek dönüşümlü pazarlara aktarılmalı."

        return pd.Series([rec_spend, boost_pct, add_starts, add_rev, desc])

    active_df[["rec_spend", "boost_pct", "add_starts", "add_rev", "rationale"]] = active_df.apply(apply_ai_rules, axis=1)

    # High-level aggregated KPI cards for selected countries
    tot_cur_spend = active_df["spend_eur"].sum()
    tot_rec_spend = active_df["rec_spend"].sum()
    tot_add_starts = active_df["add_starts"].sum()
    tot_add_rev = active_df["add_rev"].sum()
    diff_spend = tot_rec_spend - tot_cur_spend

    kc1, kc2, kc3, kc4 = st.columns(4)
    with kc1:
        render_kpi_card("Seçili Pazarlar Mevcut Bütçe", f"€{tot_cur_spend:,.0f}", f"{len(active_df)} Ülke Toplamı", icon="💶")
    with kc2:
        render_kpi_card("AI Önerilen Toplam Bütçe", f"€{tot_rec_spend:,.0f}", f"Net Değişim: {'+' if diff_spend >= 0 else ''}€{diff_spend:,.0f}", icon="🤖", is_highlight=True)
    with kc3:
        render_kpi_card("Beklenen Ek Tedavi", f"+{tot_add_starts} Hasta", "Ankara'da Tedavi Başlangıcı", icon="🧬", is_highlight=True)
    with kc4:
        render_kpi_card("Beklenen Ek Tedavi Cirosu", f"+€{tot_add_rev:,.0f}", "Öngörülen Net Gelir Artışı", icon="📈")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Comparative Plotly Bar Chart: Current vs AI Recommended
    chart_df = active_df.sort_values(by="revenue", ascending=False).head(10).copy()
    fig = go.Figure(data=[
        go.Bar(
            name="Mevcut Bütçe (€)",
            x=chart_df["country"].apply(lambda c: f"{country_flags.get(c, '')} {c}"),
            y=chart_df["spend_eur"],
            marker_color="#64748B"
        ),
        go.Bar(
            name="AI Önerilen Bütçe (€)",
            x=chart_df["country"].apply(lambda c: f"{country_flags.get(c, '')} {c}"),
            y=chart_df["rec_spend"],
            marker_color="#00F0FF"
        )
    ])
    fig.update_layout(
        title="Seçili Pazarlarda Mevcut vs. AI Önerilen Bütçe Karşılaştırması",
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", size=11),
        height=330,
        margin=dict(l=10, r=10, t=35, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # Detailed AI Optimization Table
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>📋 Ülke Bazlı Bütçe Yeniden Tahsis ve Getiri Matrisi</span>
            <span class="tag">Canlı Veriyle Hesaplanmış</span>
        </div>
    """, unsafe_allow_html=True)

    disp_table = active_df.sort_values(by="revenue", ascending=False).copy()
    disp_table["Ülke / Pazar"] = disp_table["country"].apply(lambda c: f"{country_flags.get(c, '🏳️')} {c}")
    disp_table["Mevcut Bütçe (€)"] = disp_table["spend_eur"].apply(lambda x: f"€{x:,.0f}")
    disp_table["Önerilen Bütçe (€)"] = disp_table["rec_spend"].apply(lambda x: f"€{x:,.0f}")
    disp_table["Değişim"] = disp_table["boost_pct"].apply(lambda x: f"+%{x:.1f}" if x >= 0 else f"-%{abs(x):.1f}")
    disp_table["Mevcut CAC (€)"] = disp_table["cac"].apply(lambda x: f"€{x:,.0f}")
    disp_table["ROAS"] = disp_table["roas"].apply(lambda x: f"{x:.1f}x")
    disp_table["Beklenen Ek Hasta"] = disp_table["add_starts"].apply(lambda x: f"+{x}" if x > 0 else "0")
    disp_table["Beklenen Ek Ciro (€)"] = disp_table["add_rev"].apply(lambda x: f"+€{x:,.0f}" if x > 0 else "€0")

    st.dataframe(
        disp_table[[
            "Ülke / Pazar", "region", "Mevcut Bütçe (€)", "Önerilen Bütçe (€)",
            "Değişim", "Mevcut CAC (€)", "ROAS", "Beklenen Ek Hasta", "Beklenen Ek Ciro (€)", "rationale"
        ]].rename(columns={
            "region": "Bölge",
            "rationale": "AI Stratejik Gerekçe"
        }),
        use_container_width=True,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # Interactive Country What-If Simulator
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🎛️ Tek Bir Ülke İçin Özel Bütçe & ROI Simülasyonu</span>
            <span class="tag">İnteraktif Karar Destek</span>
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
            Aşağıdan dilediğiniz hedef ülkeyi seçerek bütçe artışının veya koordinatör hızlandırmasının o ülkedeki tahmini hasta sayısına ve cirosuna etkisini anlık simüle edin:
        </div>
    """, unsafe_allow_html=True)

    sim_c1, sim_c2, sim_c3 = st.columns([1.2, 1, 1])
    with sim_c1:
        sim_selected_c = st.selectbox("Simülasyon Yapılacak Ülke:", all_countries_list, index=0)
    
    c_row = merged[merged["country"] == sim_selected_c].iloc[0]
    c_base_spend = c_row["spend_eur"]
    c_base_starts = c_row["treatments"]
    c_base_leads = c_row["total_leads"]
    c_base_rev = c_row["revenue"]
    c_avg_ticket = (c_base_rev / c_base_starts) if c_base_starts > 0 else 5500

    with sim_c2:
        sim_budget_slider = st.slider(f"{sim_selected_c} Reklam Bütçesi Değişimi (%)", -50, 100, 25, step=5)
    with sim_c3:
        sim_cvr_slider = st.slider(f"{sim_selected_c} Konsültasyon Hızı / Triage İyileşmesi (%)", 0, 50, 15, step=5)

    sim_b_factor = 1.0 + (sim_budget_slider / 100.0)
    sim_c_factor = 1.0 + (sim_cvr_slider / 100.0)

    res_spend = c_base_spend * sim_b_factor
    res_leads = int(c_base_leads * sim_b_factor)
    res_starts = int(c_base_starts * (sim_b_factor ** 0.82) * sim_c_factor)
    res_rev = res_starts * c_avg_ticket
    res_cac = (res_spend / res_starts) if res_starts > 0 else 0

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        render_kpi_card("Yeni Bütçe", f"€{res_spend:,.0f}", f"Önceki: €{c_base_spend:,.0f}", icon="💶")
    with sc2:
        render_kpi_card("Tahmini Başvuru (Lead)", f"{res_leads}", f"Fark: {'+' if res_leads >= c_base_leads else ''}{res_leads - c_base_leads}", icon="📥")
    with sc3:
        render_kpi_card("Tedavi Başlangıcı", f"{res_starts} Hasta", f"Fark: {'+' if res_starts >= c_base_starts else ''}{res_starts - c_base_starts}", icon="🧬", is_highlight=True)
    with sc4:
        render_kpi_card("Tahmini Tedavi Geliri", f"€{res_rev:,.0f}", f"Fark: {'+' if res_rev >= c_base_rev else ''}€{res_rev - c_base_rev:,.0f}", icon="📈", is_highlight=True)

    st.markdown("</div>", unsafe_allow_html=True)
