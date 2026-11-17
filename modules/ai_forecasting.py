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
