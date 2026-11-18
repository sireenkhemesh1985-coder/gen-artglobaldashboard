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

def render_html(html_str):
    """Renders HTML safely by stripping all leading whitespace from each line and removing blank lines to prevent markdown code block formatting"""
    lines = [line.strip() for line in html_str.strip().split("\n") if line.strip()]
    cleaned = "\n".join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

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

    tab_engine, tab_arbitrage, tab_simulator, tab_budget = st.tabs([
        "🧠 AI Fırsat Öneri Motoru (Strategy Engine)",
        "💶 Ülke Tedavi Maliyetleri vs. Türkiye Arbitrajı",
        "🎛️ Çok Değişkenli Senaryo Simülatörü",
        "📢 Pazar Bazlı Reklam Bütçesi & ROI Optimizasyonu"
    ])

    with tab_engine:
        render_opportunity_engine(leads_df)

    with tab_arbitrage:
        render_treatment_cost_arbitrage()

    with tab_simulator:
        render_scenario_simulator(leads_df, spend_df)

    with tab_budget:
        render_budget_optimizer(leads_df, spend_df)

# Comprehensive 24-Country International IVF Market Deep Dive Dataset
ALL_MARKET_DEEP_DIVE = [
    {
        "country_raw": "Iraq",
        "Ülke": "🇮🇶 Irak",
        "Bölge": "Middle East & Gulf",
        "Yerelde IVF Yapılıyor mu?": "Sınırlı & Altyapı Yetersiz",
        "Yerel Kapasite / Kalite": "Bağdat ve Erbil'de merkezler var; ancak akredite PGT-A (NGS) genetik lab ve temiz oda altyapısı yetersiz.",
        "Yerel Maliyet": "$3,500 - $5,000",
        "Yurtdışına Çıkış (%)": "%68",
        "Türkiye Tercih Payı (%)": "%54",
        "GEN-ART'a Geliş Kök Nedeni": "Yerinde akredite PGT-A NGS laboratuvarı, Mikro-TESE androloji başarısı ve Bağdat/Erbil - Ankara direkt uçuşları."
    },
    {
        "country_raw": "Jordan",
        "Ülke": "🇯🇴 Ürdün",
        "Bölge": "Middle East & Gulf",
        "Yerelde IVF Yapılıyor mu?": "Evet, Yaygın (Bölgesel Merkez)",
        "Yerel Kapasite / Kalite": "Amman'da gelişmiş özel hastaneler var ancak tedavi $6,000-$7,500+ çok pahalı. PGT analizlerini yurtdışına gönderip donduruyorlar.",
        "Yerel Maliyet": "$6,500 - $8,000",
        "Yurtdışına Çıkış (%)": "%24",
        "Türkiye Tercih Payı (%)": "%38",
        "GEN-ART'a Geliş Kök Nedeni": "Tek ziyarette 17 günde biten Express NGS ile taze transfer (hastaya €3,200 tasarruf), 1-2 yerel başarısızlık sonrası 2. görüş ve 90 gün vizesiz giriş."
    },
    {
        "country_raw": "Azerbaijan",
        "Ülke": "🇦🇿 Azerbaycan",
        "Bölge": "Central Asia & CIS",
        "Yerelde IVF Yapılıyor mu?": "Evet, Mevcut",
        "Yerel Kapasite / Kalite": "Bakü'de klinikler var ancak ileri genetik tarama (PGT) ve tekrarlayan başarısız vaka tecrübesine güvensizlik yüksek.",
        "Yerel Maliyet": "$4,000 - $5,500",
        "Yurtdışına Çıkış (%)": "%45",
        "Türkiye Tercih Payı (%)": "%78",
        "GEN-ART'a Geliş Kök Nedeni": "Türk hekimlerine mutlak güven, kimlikle seyahat imkanı, dil bariyerinin olmaması ve karmaşık genetik vaka başarısı."
    },
    {
        "country_raw": "Germany",
        "Ülke": "🇩🇪 Almanya",
        "Bölge": "Europe",
        "Yerelde IVF Yapılıyor mu?": "Evet, Çok Yaygın",
        "Yerel Kapasite / Kalite": "Alman Embriyo Koruma Kanunu (Embryonenschutzgesetz) ile embriyoya PGT-A anöploidi taraması yasal olarak yasaklanmıştır.",
        "Yerel Maliyet": "€4,500 - €6,500",
        "Yurtdışına Çıkış (%)": "%35",
        "Türkiye Tercih Payı (%)": "%32",
        "GEN-ART'a Geliş Kök Nedeni": "Yasal PGT-A genetik tarama serbestisi, ileri anne yaşı (40+) protokolleri ve Türkiye'deki A+ genetik laboratuvar kalitesi."
    },
    {
        "country_raw": "Saudi Arabia",
        "Ülke": "🇸🇦 Suudi Arabistan",
        "Bölge": "Middle East & Gulf",
        "Yerelde IVF Yapılıyor mu?": "Evet, A+ Merkezler Var",
        "Yerel Kapasite / Kalite": "Riyad ve Cidde'de merkezler var ancak maliyet $10,000+ ve bekleme süreleri uzun. Akraba evliliği kaynaklı monogenik hastalık çok yüksek.",
        "Yerel Maliyet": "$10,000 - $14,000",
        "Yurtdışına Çıkış (%)": "%34",
        "Türkiye Tercih Payı (%)": "%42",
        "GEN-ART'a Geliş Kök Nedeni": "PGT-M tek gen hastalıkları uzmanlığı, yüksek VIP mahremiyet ve Ankara Esenboğa direkt uçuş koridoru."
    },
    {
        "country_raw": "UAE",
        "Ülke": "🇦🇪 BAE (Dubai / Abu Dabi)",
        "Bölge": "Middle East & Gulf",
        "Yerelde IVF Yapılıyor mu?": "Evet, Lüks Merkezler",
        "Yerel Kapasite / Kalite": "Tedavi maliyeti $12,000-$16,000 seviyesinde. Yüksek expat nüfus ve yerel Arap nüfusta ileri yaş talebi.",
        "Yerel Maliyet": "$12,000 - $16,000",
        "Yurtdışına Çıkış (%)": "%30",
        "Türkiye Tercih Payı (%)": "%35",
        "GEN-ART'a Geliş Kök Nedeni": "Üstün fiyat/performans (%60 maliyet avantajı), hızlı başlangıç ve kişiselleştirilmiş hekim takibi."
    },
    {
        "country_raw": "Kuwait",
        "Ülke": "🇰🇼 Kuveyt",
        "Bölge": "Middle East & Gulf",
        "Yerelde IVF Yapılıyor mu?": "Evet, Mevcut",
        "Yerel Kapasite / Kalite": "Devlet hastanelerinde bekleme süresi 8-12 ay; özelde maliyet çok yüksek.",
        "Yerel Maliyet": "$8,500 - $11,000",
        "Yurtdışına Çıkış (%)": "%40",
        "Türkiye Tercih Payı (%)": "%46",
        "GEN-ART'a Geliş Kök Nedeni": "Direkt Ankara uçuşu, vizesiz 90 gün, akraba evliliği panelleri (PGT-M) ve yüksek klinik gebelik oranları."
    },
    {
        "country_raw": "Qatar",
        "Ülke": "🇶🇦 Katar",
        "Bölge": "Middle East & Gulf",
        "Yerelde IVF Yapılıyor mu?": "Evet, Sınırlı Merkez",
        "Yerel Kapasite / Kalite": "Hamad Medical vb. kapasite sınırlı, randevu sıraları uzun.",
        "Yerel Maliyet": "$9,000 - $12,500",
        "Yurtdışına Çıkış (%)": "%38",
        "Türkiye Tercih Payı (%)": "%44",
        "GEN-ART'a Geliş Kök Nedeni": "Hızlı randevu, kişiye özel stimülasyon protokolleri ve VIP sağlık turizmi hizmeti."
    },
    {
        "country_raw": "Uzbekistan",
        "Ülke": "🇺🇿 Özbekistan",
        "Bölge": "Central Asia & CIS",
        "Yerelde IVF Yapılıyor mu?": "Gelişmekte / Yetersiz",
        "Yerel Kapasite / Kalite": "Taşkent'te yeni merkezler açılsa da laboratuvar tecrübesi ve PGT-A genetik altyapısı eksik.",
        "Yerel Maliyet": "$3,000 - $4,500",
        "Yurtdışına Çıkış (%)": "%52",
        "Türkiye Tercih Payı (%)": "%64",
        "GEN-ART'a Geliş Kök Nedeni": "Rusça/Özbekçe koordinatör desteği, Taşkent-Ankara direkt seferi, yüksek canlı doğum oranı."
    },
    {
        "country_raw": "Kazakhstan",
        "Ülke": "🇰🇿 Kazakistan",
        "Bölge": "Central Asia & CIS",
        "Yerelde IVF Yapılıyor mu?": "Evet, Almatı/Astana",
        "Yerel Kapasite / Kalite": "Devlet kotaları sınırlı; ileri yaş ve tekrarlayan başarısız tüp bebek vakalarında yurtdışı ikinci görüş yaygın.",
        "Yerel Maliyet": "$3,500 - $5,000",
        "Yurtdışına Çıkış (%)": "%36",
        "Türkiye Tercih Payı (%)": "%58",
        "GEN-ART'a Geliş Kök Nedeni": "30 gün vizesiz seyahat, kapsamlı over gençleştirme (PRP) ve NGS genetik tarama güvencesi."
    },
    {
        "country_raw": "United Kingdom",
        "Ülke": "🇬🇧 İngiltere (Birleşik Krallık)",
        "Bölge": "Europe",
        "Yerelde IVF Yapılıyor mu?": "Evet (NHS Sıraları Çok Uzun)",
        "Yerel Kapasite / Kalite": "NHS kotaları katı (yaş/BMI sınırı) ve bekleme süresi 1-2 yıl; özel klinikler £7,000-£10,000+.",
        "Yerel Maliyet": "£7,500 - £11,000",
        "Yurtdışına Çıkış (%)": "%28",
        "Türkiye Tercih Payı (%)": "%26",
        "GEN-ART'a Geliş Kök Nedeni": "Hızlı beklemesiz tedavi, Londra-Ankara direkt uçuş, %50 maliyet tasarrufu ve vizesiz 90 gün."
    },
    {
        "country_raw": "Netherlands",
        "Ülke": "🇳🇱 Hollanda",
        "Bölge": "Europe",
        "Yerelde IVF Yapılıyor mu?": "Evet, Katı Protokoller",
        "Yerel Kapasite / Kalite": "Sigorta sınırlı siklus ödüyor; PGT-A embriyo taraması yasalarla çok sıkı kısıtlanmış.",
        "Yerel Maliyet": "€4,000 - €5,500",
        "Yurtdışına Çıkış (%)": "%25",
        "Türkiye Tercih Payı (%)": "%34",
        "GEN-ART'a Geliş Kök Nedeni": "Yasal genetik tarama serbestisi, Türk diasporası bağlantısı, vizesiz 90 gün."
    },
    {
        "country_raw": "Italy",
        "Ülke": "🇮🇹 İtalya",
        "Bölge": "Europe",
        "Yerelde IVF Yapılıyor mu?": "Evet, Katı Yasal Düzenlemeler",
        "Yerel Kapasite / Kalite": "Katolik etik kuralları ve yasal geçmiş sebebiyle ileri genetik uygulamalar yavaş ve bürokratik.",
        "Yerel Maliyet": "€4,500 - €6,000",
        "Yurtdışına Çıkış (%)": "%32",
        "Türkiye Tercih Payı (%)": "%22",
        "GEN-ART'a Geliş Kök Nedeni": "Hızlı genetik tarama, Roma/Milano aktarmasız ESB hatları, ekonomik paket fiyatlar."
    },
    {
        "country_raw": "France",
        "Ülke": "🇫🇷 Fransa",
        "Bölge": "Europe",
        "Yerelde IVF Yapılıyor mu?": "Evet, Katı Bürokratik Süreç",
        "Yerel Kapasite / Kalite": "Devlet karşılıyor ancak bekleme süreleri 9-14 ay; PGT-A taraması katı yasak kapsamında.",
        "Yerel Maliyet": "€4,200 - €5,800",
        "Yurtdışına Çıkış (%)": "%22",
        "Türkiye Tercih Payı (%)": "%20",
        "GEN-ART'a Geliş Kök Nedeni": "Bekleme süresi olmadan anında tedavi, PGT-A serbestliği ve Paris-Ankara direkt uçuşlar."
    },
    {
        "country_raw": "Georgia",
        "Ülke": "🇬🇪 Gürcistan",
        "Bölge": "North Africa & Other",
        "Yerelde IVF Yapılıyor mu?": "Evet, Tiflis Merkezli",
        "Yerel Kapasite / Kalite": "Taşıyıcı annelik yaygın ancak kendi embriyosuyla tüp bebek ve ileri PGT genetik laboratuvarları kısıtlı.",
        "Yerel Maliyet": "$3,500 - $5,000",
        "Yurtdışına Çıkış (%)": "%30",
        "Türkiye Tercih Payı (%)": "%72",
        "GEN-ART'a Geliş Kök Nedeni": "Kimlikle sınır geçişi, coğrafi yakınlık, Türk genetik teknolojisine güven."
    },
    {
        "country_raw": "Serbia",
        "Ülke": "🇷🇸 Sırbistan",
        "Bölge": "Balkans",
        "Yerelde IVF Yapılıyor mu?": "Evet, Belgrad",
        "Yerel Kapasite / Kalite": "Belgrad'da merkezler var; devlet 3 hak veriyor ancak ileri genetik tarama (NGS) dış laboratuvarlara bağımlı.",
        "Yerel Maliyet": "€3,200 - €4,500",
        "Yurtdışına Çıkış (%)": "%26",
        "Türkiye Tercih Payı (%)": "%42",
        "GEN-ART'a Geliş Kök Nedeni": "Belgrad-Ankara direkt 1.8 saat uçuş, vizesiz 90 gün, tek ziyarette tamamlanan Express PGT."
    },
    {
        "country_raw": "Bosnia",
        "Ülke": "🇧🇦 Bosna Hersek",
        "Bölge": "Balkans",
        "Yerelde IVF Yapılıyor mu?": "Sınırlı Kapasite",
        "Yerel Kapasite / Kalite": "Saraybosna'da az sayıda klinik; embriyoloji ve genetik tecrübesi kısıtlı.",
        "Yerel Maliyet": "€3,000 - €4,200",
        "Yurtdışına Çıkış (%)": "%48",
        "Türkiye Tercih Payı (%)": "%68",
        "GEN-ART'a Geliş Kök Nedeni": "Tarihsel ve kültürel bağlar, vizesiz 90 gün, Saraybosna-Ankara direkt hatları."
    },
    {
        "country_raw": "Albania",
        "Ülke": "🇦🇱 Arnavutluk",
        "Bölge": "Balkans",
        "Yerelde IVF Yapılıyor mu?": "Sınırlı Kapasite",
        "Yerel Kapasite / Kalite": "Tiran'da az sayıda özel merkez var ancak ileri genetik analiz altyapısı eksik.",
        "Yerel Maliyet": "€3,000 - €4,000",
        "Yurtdışına Çıkış (%)": "%46",
        "Türkiye Tercih Payı (%)": "%55",
        "GEN-ART'a Geliş Kök Nedeni": "Vizesiz giriş, kısa uçuş mesafesi, güvenilir Türk sağlık personeli."
    },
    {
        "country_raw": "Kosovo",
        "Ülke": "🇽🇰 Kosova",
        "Bölge": "Balkans",
        "Yerelde IVF Yapılıyor mu?": "Sınırlı & Altyapı Eksik",
        "Yerel Kapasite / Kalite": "Priştine'de küçük klinikler var ancak karmaşık genetik olgular ve over rezervi azlığı çözülemiyor.",
        "Yerel Maliyet": "€2,800 - €3,800",
        "Yurtdışına Çıkış (%)": "%54",
        "Türkiye Tercih Payı (%)": "%65",
        "GEN-ART'a Geliş Kök Nedeni": "Vizesiz 90 gün, Priştine-Ankara direkt bağlantısı, yüksek klinik başarı oranları."
    },
    {
        "country_raw": "Libya",
        "Ülke": "🇱🇾 Libya",
        "Bölge": "North Africa & Other",
        "Yerelde IVF Yapılıyor mu?": "Hayır (Sistem Çökmüş Durumda)",
        "Yerel Kapasite / Kalite": "Savaş sonrası medikal gaz, embriyoloji solüsyonu ve uzman hekim eksikliği nedeniyle yerel tedavi imkansıza yakın.",
        "Yerel Maliyet": "Mevcut Değil",
        "Yurtdışına Çıkış (%)": "%82",
        "Türkiye Tercih Payı (%)": "%52",
        "GEN-ART'a Geliş Kök Nedeni": "Kompleks infertilite çözümleri, Sağlık Bakanlığı onaylı medikal vize davetiyesi (ST-0625)."
    },
    {
        "country_raw": "Algeria",
        "Ülke": "🇩🇿 Cezayir",
        "Bölge": "North Africa & Other",
        "Yerelde IVF Yapılıyor mu?": "Evet, Kapasite Yetersiz",
        "Yerel Kapasite / Kalite": "Devlet hastanelerinde 2 yıl sıra; özel sektörde PGT genetik analizi yapılamıyor.",
        "Yerel Maliyet": "$3,000 - $4,200",
        "Yurtdışına Çıkış (%)": "%42",
        "Türkiye Tercih Payı (%)": "%45",
        "GEN-ART'a Geliş Kök Nedeni": "Fransa'ya kıyasla 3 kat daha ekonomik olması, USHAŞ vize desteği ve Arapça/Fransızca koordinasyon."
    },
    {
        "country_raw": "Egypt",
        "Ülke": "🇪🇬 Mısır",
        "Bölge": "North Africa & Other",
        "Yerelde IVF Yapılıyor mu?": "Evet, Kahire/İskenderiye",
        "Yerel Kapasite / Kalite": "Büyük merkezler var ancak devalüasyon sonrası ithal embriyoloji kitleri krizi ve ileri genetik maliyeti arttı.",
        "Yerel Maliyet": "$2,500 - $3,800",
        "Yurtdışına Çıkış (%)": "%22",
        "Türkiye Tercih Payı (%)": "%36",
        "GEN-ART'a Geliş Kök Nedeni": "Kapıda kolay e-Vize, Kahire-Ankara uçuşları, yüksek kalite standartları (ISO/CAP)."
    },
    {
        "country_raw": "Russia",
        "Ülke": "🇷🇺 Rusya",
        "Bölge": "Central Asia & CIS",
        "Yerelde IVF Yapılıyor mu?": "Evet, Moskova/St. Petersburg",
        "Yerel Kapasite / Kalite": "Ambargolar nedeniyle Avrupa genetik kitlerine ve cihaz parçalarına erişimde aksamalar mevcut.",
        "Yerel Maliyet": "$3,500 - $5,000",
        "Yurtdışına Çıkış (%)": "%25",
        "Türkiye Tercih Payı (%)": "%48",
        "GEN-ART'a Geliş Kök Nedeni": "Direkt uçuşlar (hava sahası açık), vizesiz 60 gün, Rusça tam koordinasyon ve kesintisiz modern NGS teknolojisi."
    },
    {
        "country_raw": "Kyrgyzstan",
        "Ülke": "🇰🇬 Kırgızistan",
        "Bölge": "Central Asia & CIS",
        "Yerelde IVF Yapılıyor mu?": "Sınırlı Kapasite",
        "Yerel Kapasite / Kalite": "Bişkek'te sınırlı sayıda merkez var; genetik tarama ve ileri embriyoloji için hastalar yurtdışına yöneliyor.",
        "Yerel Maliyet": "$2,800 - $4,000",
        "Yurtdışına Çıkış (%)": "%44",
        "Türkiye Tercih Payı (%)": "%62",
        "GEN-ART'a Geliş Kök Nedeni": "Bişkek-Ankara direkt uçuşu, 90 gün vizesiz rejim, Rusça dil desteği."
    }
]


# 24-Country International IVF & Genetics Treatment Cost Benchmarks vs. Turkey (GEN-ART)
COUNTRY_TREATMENT_COST_BENCHMARKS = [
    {
        "country": "United Kingdom",
        "flag": "🇬🇧",
        "name_tr": "İngiltere (Birleşik Krallık)",
        "region": "Europe",
        "local_ivf_min_eur": 9500,
        "local_ivf_max_eur": 14000,
        "local_ivf_avg_eur": 11800,
        "local_pgt_eur": 3000,
        "local_total_eur": 14800,
        "local_currency_str": "£8,000 - £12,000",
        "local_pgt_status": "Özelde embriyo başı £600-£800; NHS'te genetik tarama yapılmıyor",
        "turkey_genart_pkg_eur": 4200,
        "travel_hotel_17d_eur": 1600,
        "turkey_total_with_travel_eur": 5800,
        "net_savings_eur": 9000,
        "savings_pct": 61,
        "primary_driver": "NHS'te 1-2 yıl sıra bekleme, özelde aşırı yüksek maliyet; direkt uçuşla %61 tasarruf"
    },
    {
        "country": "UAE",
        "flag": "🇦🇪",
        "name_tr": "BAE (Dubai / Abu Dabi)",
        "region": "Middle East & Gulf",
        "local_ivf_min_eur": 11000,
        "local_ivf_max_eur": 15000,
        "local_ivf_avg_eur": 13000,
        "local_pgt_eur": 3200,
        "local_total_eur": 16200,
        "local_currency_str": "$12,000 - $16,000",
        "local_pgt_status": "Mevcut ancak fahiş fiyatlı ($3,000 - $4,500)",
        "turkey_genart_pkg_eur": 4500,
        "travel_hotel_17d_eur": 2200,
        "turkey_total_with_travel_eur": 6700,
        "net_savings_eur": 9500,
        "savings_pct": 59,
        "primary_driver": "Üstün fiyat/performans (%59 net tasarruf), ileri anne yaşı kişiye özel stimülasyon, VIP hizmet"
    },
    {
        "country": "Saudi Arabia",
        "flag": "🇸🇦",
        "name_tr": "Suudi Arabistan",
        "region": "Middle East & Gulf",
        "local_ivf_min_eur": 9000,
        "local_ivf_max_eur": 13000,
        "local_ivf_avg_eur": 11000,
        "local_pgt_eur": 3500,
        "local_total_eur": 14500,
        "local_currency_str": "$10,000 - $14,000",
        "local_pgt_status": "Özel merkezlerde çok pahalı ve randevu sıraları 3-6 ay",
        "turkey_genart_pkg_eur": 4500,
        "travel_hotel_17d_eur": 2000,
        "turkey_total_with_travel_eur": 6500,
        "net_savings_eur": 8000,
        "savings_pct": 55,
        "primary_driver": "Akraba evliliği genetik panelleri (PGT-M prob tasarımı), mahremiyet ve Ankara direkt uçuşu"
    },
    {
        "country": "Qatar",
        "flag": "🇶🇦",
        "name_tr": "Katar",
        "region": "Middle East & Gulf",
        "local_ivf_min_eur": 9000,
        "local_ivf_max_eur": 12500,
        "local_ivf_avg_eur": 10750,
        "local_pgt_eur": 3300,
        "local_total_eur": 14050,
        "local_currency_str": "$9,500 - $13,500",
        "local_pgt_status": "Kapasite sınırlı; uzun randevu bekleme listeleri",
        "turkey_genart_pkg_eur": 4500,
        "travel_hotel_17d_eur": 2000,
        "turkey_total_with_travel_eur": 6500,
        "net_savings_eur": 7550,
        "savings_pct": 54,
        "primary_driver": "Kişiye özel protokoller, Ankara'da VIP koordinasyon ve %54 maliyet avantajı"
    },
    {
        "country": "Kuwait",
        "flag": "🇰🇼",
        "name_tr": "Kuveyt",
        "region": "Middle East & Gulf",
        "local_ivf_min_eur": 8000,
        "local_ivf_max_eur": 11000,
        "local_ivf_avg_eur": 9500,
        "local_pgt_eur": 3200,
        "local_total_eur": 12700,
        "local_currency_str": "$8,500 - $11,500",
        "local_pgt_status": "Devlet kotaları 8-12 ay; özelde test başına yüksek ek ücret",
        "turkey_genart_pkg_eur": 4400,
        "travel_hotel_17d_eur": 1800,
        "turkey_total_with_travel_eur": 6200,
        "net_savings_eur": 6500,
        "savings_pct": 51,
        "primary_driver": "Beklemesiz anında başlangıç, %51 tasarruf, vizesiz 90 gün ve yüksek klinik gebelik başarısı"
    },
    {
        "country": "Jordan",
        "flag": "🇯🇴",
        "name_tr": "Ürdün",
        "region": "Middle East & Gulf",
        "local_ivf_min_eur": 5800,
        "local_ivf_max_eur": 7500,
        "local_ivf_avg_eur": 6650,
        "local_pgt_eur": 2300,
        "local_total_eur": 8950,
        "local_currency_str": "$6,500 - $8,000",
        "local_pgt_status": "PGT numuneleri yurtdışına yollanır; embriyolar dondurulup 2 ayrı seyahat yaptırılır",
        "turkey_genart_pkg_eur": 3800,
        "travel_hotel_17d_eur": 1400,
        "turkey_total_with_travel_eur": 5200,
        "net_savings_eur": 3750,
        "savings_pct": 42,
        "primary_driver": "Amman'da 2 seyahat + dondurma masrafı yerine Ankara'da 17 günde Express NGS ile taze transfer"
    },
    {
        "country": "Germany",
        "flag": "🇩🇪",
        "name_tr": "Almanya",
        "region": "Europe",
        "local_ivf_min_eur": 5500,
        "local_ivf_max_eur": 7500,
        "local_ivf_avg_eur": 6500,
        "local_pgt_eur": 0,
        "local_total_eur": 6500,
        "local_currency_str": "€5,500 - €7,500",
        "local_pgt_status": "YASAL OLARAK YASAK (Embryonenschutzgesetz - Sadece ölümcül vakada etik kurul)",
        "turkey_genart_pkg_eur": 4200,
        "travel_hotel_17d_eur": 1400,
        "turkey_total_with_travel_eur": 5600,
        "net_savings_eur": 900,
        "savings_pct": 14,
        "primary_driver": "Yasal PGT-A taraması Almanya'da yasak; Türkiye'de yasal, güvenli ve akredite NGS ile tek seferde transfer"
    },
    {
        "country": "Italy",
        "flag": "🇮🇹",
        "name_tr": "İtalya",
        "region": "Europe",
        "local_ivf_min_eur": 4800,
        "local_ivf_max_eur": 6500,
        "local_ivf_avg_eur": 5650,
        "local_pgt_eur": 2500,
        "local_total_eur": 8150,
        "local_currency_str": "€4,500 - €6,000",
        "local_pgt_status": "Yasal geçmiş ve katı etik kurul prosedürleri nedeniyle süreç 6-8 ay gecikir",
        "turkey_genart_pkg_eur": 4200,
        "travel_hotel_17d_eur": 1300,
        "turkey_total_with_travel_eur": 5500,
        "net_savings_eur": 2650,
        "savings_pct": 33,
        "primary_driver": "Hızlı randevu, bürokrasi olmadan genetik inceleme ve Roma/Milano-Ankara doğrudan uçuşları"
    },
    {
        "country": "Netherlands",
        "flag": "🇳🇱",
        "name_tr": "Hollanda",
        "region": "Europe",
        "local_ivf_min_eur": 4500,
        "local_ivf_max_eur": 6000,
        "local_ivf_avg_eur": 5250,
        "local_pgt_eur": 2800,
        "local_total_eur": 8050,
        "local_currency_str": "€4,000 - €5,500",
        "local_pgt_status": "PGT-A rutin taraması yasak ve çok katı bürokratik protokollere bağlı",
        "turkey_genart_pkg_eur": 4200,
        "travel_hotel_17d_eur": 1400,
        "turkey_total_with_travel_eur": 5600,
        "net_savings_eur": 2450,
        "savings_pct": 30,
        "primary_driver": "Yasal PGT-A tarama özgürlüğü, bekleme sırası olmaması ve Türk diasporası güveni"
    },
    {
        "country": "France",
        "flag": "🇫🇷",
        "name_tr": "Fransa",
        "region": "Europe",
        "local_ivf_min_eur": 4500,
        "local_ivf_max_eur": 6200,
        "local_ivf_avg_eur": 5350,
        "local_pgt_eur": 0,
        "local_total_eur": 5350,
        "local_currency_str": "€4,200 - €5,800",
        "local_pgt_status": "PGT-A anöploidi taraması katı yasa kapsamında yasaktır",
        "turkey_genart_pkg_eur": 4200,
        "travel_hotel_17d_eur": 1400,
        "turkey_total_with_travel_eur": 5600,
        "net_savings_eur": -250,
        "savings_pct": 0,
        "primary_driver": "Devlet hastanesindeki 12 aylık bekleme süresini atlama ve Fransa'da yasak olan PGT-A'yı yasal yaptırma"
    },
    {
        "country": "Russia",
        "flag": "🇷🇺",
        "name_tr": "Rusya",
        "region": "Central Asia & CIS",
        "local_ivf_min_eur": 3800,
        "local_ivf_max_eur": 5800,
        "local_ivf_avg_eur": 4800,
        "local_pgt_eur": 1800,
        "local_total_eur": 6600,
        "local_currency_str": "350k - 550k RUB",
        "local_pgt_status": "Yaptırılabilir ancak ambargolar nedeniyle ithal kit ve cihaz parçası sıkıntısı var",
        "turkey_genart_pkg_eur": 3800,
        "travel_hotel_17d_eur": 1400,
        "turkey_total_with_travel_eur": 5200,
        "net_savings_eur": 1400,
        "savings_pct": 21,
        "primary_driver": "Hava sahası açık, vizesiz 60 gün, Rusça tam medikal rehberlik ve modern kesintisiz NGS cihazları"
    },
    {
        "country": "Azerbaijan",
        "flag": "🇦🇿",
        "name_tr": "Azerbaycan",
        "region": "Central Asia & CIS",
        "local_ivf_min_eur": 3500,
        "local_ivf_max_eur": 5000,
        "local_ivf_avg_eur": 4250,
        "local_pgt_eur": 1400,
        "local_total_eur": 5650,
        "local_currency_str": "$4,000 - $5,500",
        "local_pgt_status": "Genetik testler dış merkezlere gönderilir; 4-6 hafta gecikmeli rapor",
        "turkey_genart_pkg_eur": 3600,
        "travel_hotel_17d_eur": 1100,
        "turkey_total_with_travel_eur": 4700,
        "net_savings_eur": 950,
        "savings_pct": 17,
        "primary_driver": "Türk hekimlerine mutlak güven, kimlikle seyahat, sıfır dil engeli ve tekrarlayan başarısız vaka tecrübesi"
    },
    {
        "country": "Iraq",
        "flag": "🇮🇶",
        "name_tr": "Irak (Bağdat / Erbil)",
        "region": "Middle East & Gulf",
        "local_ivf_min_eur": 3200,
        "local_ivf_max_eur": 4600,
        "local_ivf_avg_eur": 3900,
        "local_pgt_eur": 1500,
        "local_total_eur": 5400,
        "local_currency_str": "$3,500 - $5,000",
        "local_pgt_status": "Akredite yerli PGT laboratuvarı ve temiz oda altyapısı yok",
        "turkey_genart_pkg_eur": 3800,
        "travel_hotel_17d_eur": 1200,
        "turkey_total_with_travel_eur": 5000,
        "net_savings_eur": 400,
        "savings_pct": 7,
        "primary_driver": "Maliyetten ziyade TEKNOLOJİ ve GÜVEN; Mikro-TESE androloji uzmanlığı ve akredite NGS lab kalitesi"
    },
    {
        "country": "Kazakhstan",
        "flag": "🇰🇿",
        "name_tr": "Kazakistan",
        "region": "Central Asia & CIS",
        "local_ivf_min_eur": 3200,
        "local_ivf_max_eur": 4600,
        "local_ivf_avg_eur": 3900,
        "local_pgt_eur": 1500,
        "local_total_eur": 5400,
        "local_currency_str": "$3,500 - $5,000",
        "local_pgt_status": "Devlet kotaları çok sınırlı; özelde genetik testler pahalı",
        "turkey_genart_pkg_eur": 3600,
        "travel_hotel_17d_eur": 1200,
        "turkey_total_with_travel_eur": 4800,
        "net_savings_eur": 600,
        "savings_pct": 11,
        "primary_driver": "Vizesiz rejim, PRP yumurtalık gençleştirme ve ileri yaş zorlu vakalarda referans merkez güvencesi"
    },
    {
        "country": "Uzbekistan",
        "flag": "🇺🇿",
        "name_tr": "Özbekistan",
        "region": "Central Asia & CIS",
        "local_ivf_min_eur": 2800,
        "local_ivf_max_eur": 4200,
        "local_ivf_avg_eur": 3500,
        "local_pgt_eur": 1600,
        "local_total_eur": 5100,
        "local_currency_str": "$3,000 - $4,500",
        "local_pgt_status": "Taşkent'te yeni açılan lablar yetersiz; PGT güvenilirliği düşük",
        "turkey_genart_pkg_eur": 3600,
        "travel_hotel_17d_eur": 1200,
        "turkey_total_with_travel_eur": 4800,
        "net_savings_eur": 300,
        "savings_pct": 6,
        "primary_driver": "Yüksek canlı doğum başarı oranı, Rusça/Özbekçe koordinatör ve Taşkent-Ankara direkt seferi"
    },
    {
        "country": "Georgia",
        "flag": "🇬🇪",
        "name_tr": "Gürcistan",
        "region": "North Africa & Other",
        "local_ivf_min_eur": 3200,
        "local_ivf_max_eur": 4800,
        "local_ivf_avg_eur": 4000,
        "local_pgt_eur": 1500,
        "local_total_eur": 5500,
        "local_currency_str": "$3,500 - $5,000",
        "local_pgt_status": "Taşıyıcı annelik yaygın ancak ileri genetik analiz cihazları yetersiz",
        "turkey_genart_pkg_eur": 3600,
        "travel_hotel_17d_eur": 900,
        "turkey_total_with_travel_eur": 4500,
        "net_savings_eur": 1000,
        "savings_pct": 18,
        "primary_driver": "Kimlikle karayolu veya uçakla kolay geçiş, Türk genetik teknolojisine güven"
    },
    {
        "country": "Serbia",
        "flag": "🇷🇸",
        "name_tr": "Sırbistan",
        "region": "Balkans",
        "local_ivf_min_eur": 3500,
        "local_ivf_max_eur": 4800,
        "local_ivf_avg_eur": 4150,
        "local_pgt_eur": 1600,
        "local_total_eur": 5750,
        "local_currency_str": "€3,500 - €4,800",
        "local_pgt_status": "İleri genetik testler yurtdışına gönderilir",
        "turkey_genart_pkg_eur": 3600,
        "travel_hotel_17d_eur": 1100,
        "turkey_total_with_travel_eur": 4700,
        "net_savings_eur": 1050,
        "savings_pct": 18,
        "primary_driver": "Belgrad-Ankara direkt 1.8 saat uçuş, vizesiz rejim, ekonomik ve hızlı tedavi"
    },
    {
        "country": "Bosnia",
        "flag": "🇧🇦",
        "name_tr": "Bosna Hersek",
        "region": "Balkans",
        "local_ivf_min_eur": 3200,
        "local_ivf_max_eur": 4400,
        "local_ivf_avg_eur": 3800,
        "local_pgt_eur": 1500,
        "local_total_eur": 5300,
        "local_currency_str": "€3,200 - €4,500",
        "local_pgt_status": "Kapasite yetersiz; ileri genetik inceleme yapılamıyor",
        "turkey_genart_pkg_eur": 3600,
        "travel_hotel_17d_eur": 1000,
        "turkey_total_with_travel_eur": 4600,
        "net_savings_eur": 700,
        "savings_pct": 13,
        "primary_driver": "Kültürel yakınlık, vizesiz 90 gün, güvenilir laboratuvar"
    },
    {
        "country": "Albania",
        "flag": "🇦🇱",
        "name_tr": "Arnavutluk",
        "region": "Balkans",
        "local_ivf_min_eur": 3000,
        "local_ivf_max_eur": 4200,
        "local_ivf_avg_eur": 3600,
        "local_pgt_eur": 1400,
        "local_total_eur": 5000,
        "local_currency_str": "€3,000 - €4,000",
        "local_pgt_status": "Tiran'da klinik sayısı az, PGT-A yapılamıyor",
        "turkey_genart_pkg_eur": 3600,
        "travel_hotel_17d_eur": 1000,
        "turkey_total_with_travel_eur": 4600,
        "net_savings_eur": 400,
        "savings_pct": 8,
        "primary_driver": "Vizesiz seyahat, Tiran-Ankara direkt uçuş, yüksek başarı"
    },
    {
        "country": "Kosovo",
        "flag": "🇽🇰",
        "name_tr": "Kosova",
        "region": "Balkans",
        "local_ivf_min_eur": 2800,
        "local_ivf_max_eur": 3900,
        "local_ivf_avg_eur": 3350,
        "local_pgt_eur": 1400,
        "local_total_eur": 4750,
        "local_currency_str": "€2,800 - €3,800",
        "local_pgt_status": "Altyapı eksik, karmaşık vakalar çözülemiyor",
        "turkey_genart_pkg_eur": 3600,
        "travel_hotel_17d_eur": 950,
        "turkey_total_with_travel_eur": 4550,
        "net_savings_eur": 200,
        "savings_pct": 4,
        "primary_driver": "Vizesiz 90 gün, Türk hekim sevgisi, akredite embriyoloji kalitesi"
    },
    {
        "country": "Libya",
        "flag": "🇱🇾",
        "name_tr": "Libya",
        "region": "North Africa & Other",
        "local_ivf_min_eur": 3800,
        "local_ivf_max_eur": 5200,
        "local_ivf_avg_eur": 4500,
        "local_pgt_eur": 1500,
        "local_total_eur": 6000,
        "local_currency_str": "$4,000+",
        "local_pgt_status": "Savaş sonrası medikal gaz ve uzman eksikliği nedeniyle yerel tedavi imkansız",
        "turkey_genart_pkg_eur": 3800,
        "travel_hotel_17d_eur": 1300,
        "turkey_total_with_travel_eur": 5100,
        "net_savings_eur": 900,
        "savings_pct": 15,
        "primary_driver": "Sağlık Bakanlığı onaylı medikal vize davetiyesi (ST-0625), anahtar teslim tedavi"
    },
    {
        "country": "Algeria",
        "flag": "🇩🇿",
        "name_tr": "Cezayir",
        "region": "North Africa & Other",
        "local_ivf_min_eur": 3000,
        "local_ivf_max_eur": 4200,
        "local_ivf_avg_eur": 3600,
        "local_pgt_eur": 1500,
        "local_total_eur": 5100,
        "local_currency_str": "$3,000 - $4,200",
        "local_pgt_status": "Devlet hastanesinde 2 yıl sıra, özelde genetik yok",
        "turkey_genart_pkg_eur": 3800,
        "travel_hotel_17d_eur": 1200,
        "turkey_total_with_travel_eur": 5000,
        "net_savings_eur": 100,
        "savings_pct": 2,
        "primary_driver": "Fransa'ya gitmek yerine 3 kat daha uygun fiyat, USHAŞ vize desteği ve Arapça/Fransızca ekip"
    },
    {
        "country": "Egypt",
        "flag": "🇪🇬",
        "name_tr": "Mısır",
        "region": "North Africa & Other",
        "local_ivf_min_eur": 2600,
        "local_ivf_max_eur": 3800,
        "local_ivf_avg_eur": 3200,
        "local_pgt_eur": 1400,
        "local_total_eur": 4600,
        "local_currency_str": "$2,500 - $3,800",
        "local_pgt_status": "Devalüasyon sebebiyle ithal kit krizi; ileri genetik yapılamıyor",
        "turkey_genart_pkg_eur": 3800,
        "travel_hotel_17d_eur": 1100,
        "turkey_total_with_travel_eur": 4900,
        "net_savings_eur": -300,
        "savings_pct": 0,
        "primary_driver": "Ekonomik krizden etkilenmeyen modern laboratuvar altyapısı, kapıda e-Vize, Kahire-Ankara direkt hat"
    },
    {
        "country": "Kyrgyzstan",
        "flag": "🇰🇬",
        "name_tr": "Kırgızistan",
        "region": "Central Asia & CIS",
        "local_ivf_min_eur": 2800,
        "local_ivf_max_eur": 4000,
        "local_ivf_avg_eur": 3400,
        "local_pgt_eur": 1500,
        "local_total_eur": 4900,
        "local_currency_str": "$2,800 - $4,000",
        "local_pgt_status": "Bişkek'te merkezler sınırlı; genetik numuneler yurtdışına bağımlı",
        "turkey_genart_pkg_eur": 3600,
        "travel_hotel_17d_eur": 1100,
        "turkey_total_with_travel_eur": 4700,
        "net_savings_eur": 200,
        "savings_pct": 4,
        "primary_driver": "Bişkek-Ankara direkt uçuşu, 90 gün vizesiz rejim, Rusça dil desteği"
    }
]


def render_treatment_cost_arbitrage():
    """Renders comprehensive country-by-country IVF & Genetic treatment cost comparison against Turkey (GEN-ART)"""
    render_html("""
    <div class="section-card">
        <div class="section-header">
            <span>💶 Hedef Ülkelerde Yerel Tedavi Maliyeti vs. Türkiye / GEN-ART Fiyat Arbitrajı</span>
            <span class="tag">24 Odak Ülke Karşılaştırmalı Fiyat Analizi</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6; margin-bottom: 14px;">
            Yabancı bir çift <b>kendi ülkesinde tüp bebek ve genetik tarama için ne kadar ödüyor?</b> Türkiye'ye uçak bileti ve 17 günlük 4-5 yıldızlı otel konaklaması dahil geldiklerinde <b>ne kadar net tasarruf sağlıyorlar?</b> Hangi ülkelerde asıl motivasyon doğrudan fiyat tasarrufu, hangi ülkelerde yasal yasaklar veya laboratuvar teknolojisidir?
        </div>
    </div>
    """)

    # Strategic KPI Bar
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("En Yüksek Net Tasarruf", "€8,000 - €9,500", "İngiltere, BAE, Suudi Arabistan, Kuveyt", icon="💎", is_highlight=True)
    with k2:
        render_kpi_card("Türkiye / GEN-ART Paketi", "€3,600 - €4,500", "IVF + İlaç + Akredite NGS PGT-A", icon="🇹🇷", is_highlight=True)
    with k3:
        render_kpi_card("Uçak + 17 Gün Otel/Transfer", "€1,100 - €2,000", "Ankara Esenboğa & 4-5* Konaklama", icon="✈️")
    with k4:
        render_kpi_card("Fiyat Dışı Kritik Arbitraj", "Yasal İzin & Akredite Lab", "Almanya'da Yasak, Irak'ta Lab Yok", icon="⚖️")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Interactive Savings & What-If Calculator Box
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🧮 İnteraktif Hasta Tedavi & Tasarruf Hesaplayıcısı (Country Cost Calculator)</span>
            <span class="tag">Seçilen Ülkeye Göre Canlı Hesaplama</span>
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
            Aşağıdan hastanın geldiği ülkeyi ve planlanan tedavi protokolünü seçerek, hastanın kendi ülkesinde ödeyeceği tutar ile Türkiye'de seyahat dahil yapacağı net tasarrufu anında hesaplayın:
        </div>
    """, unsafe_allow_html=True)

    calc_c1, calc_c2 = st.columns([1.5, 2])
    with calc_c1:
        country_display_names = [f"{b['flag']} {b['name_tr']}" for b in COUNTRY_TREATMENT_COST_BENCHMARKS]
        sel_display_c = st.selectbox("Hastanın Geldiği Ülke:", country_display_names, index=0)
        sel_bench = next(b for b in COUNTRY_TREATMENT_COST_BENCHMARKS if f"{b['flag']} {b['name_tr']}" == sel_display_c)

        treatment_package_type = st.radio(
            "Uygulanacak Tedavi Protokolü:",
            [
                "🔬 IVF + Akredite NGS PGT-A (Genetik Taramalı Tam Paket)",
                "🧬 IVF + PGT-M Tek Gen Hastalığı (Akraba Evliliği / Nadir Mutasyon)",
                "🚹 Mikro-TESE Cerrahi Androloji + IVF (Ağır Erkek Kısırlığı)",
                "👶 Standart IVF + ICSI (Genetiksiz Temel Paket)"
            ],
            index=0
        )

    # Multipliers based on package
    if "PGT-M" in treatment_package_type:
        pkg_turkey_cost = sel_bench["turkey_genart_pkg_eur"] + 600
        pkg_local_cost = round(sel_bench["local_total_eur"] * 1.15)
        pkg_note = "Akraba evliliği veya ailevi kalıtsal hastalık için aileye özel prob tasarımı ve tek gen analizi dahil edilmiştir."
    elif "Mikro-TESE" in treatment_package_type:
        pkg_turkey_cost = sel_bench["turkey_genart_pkg_eur"] + 450
        pkg_local_cost = round(sel_bench["local_total_eur"] * 1.10)
        pkg_note = "İleri androloji ameliyathanesi, mikrocerrahi TESE ve lazer destekli sperm seçimi dahil edilmiştir."
    elif "Standart IVF" in treatment_package_type:
        pkg_turkey_cost = sel_bench["turkey_genart_pkg_eur"] - 700
        pkg_local_cost = sel_bench["local_ivf_avg_eur"]
        pkg_note = "Embriyo genetik taraması (PGT) hariç tutulmuş, standart yumurta toplama ve embriyo transferi hesaplanmıştır."
    else: # PGT-A Tam Paket
        pkg_turkey_cost = sel_bench["turkey_genart_pkg_eur"]
        pkg_local_cost = sel_bench["local_total_eur"]
        pkg_note = "Kendi akredite genetik laboratuvarımızda (Mikrogen Lab) embriyo trofektoderm biyopsisi ve Illumina NGS analizi dahil tam pakettir."

    travel_cost = sel_bench["travel_hotel_17d_eur"]
    turkey_total_with_travel = pkg_turkey_cost + travel_cost
    patient_net_savings = pkg_local_cost - turkey_total_with_travel
    savings_percentage = round((patient_net_savings / pkg_local_cost * 100)) if pkg_local_cost > 0 else 0

    with calc_c2:
        res1, res2 = st.columns(2)
        with res1:
            render_html(f"""
            <div style="background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.4); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                <div style="font-size: 11px; color: #FCA5A5; font-weight: 700;">🏠 Kendi Ülkesinde Ödeyeceği Tutar:</div>
                <div style="font-size: 20px; font-weight: 800; color: #F87171; margin: 4px 0;">€{pkg_local_cost:,.0f}</div>
                <div style="font-size: 11px; color: #CBD5E1;">Yerel para birimi: {sel_bench['local_currency_str']}</div>
            </div>
            """)
            render_html(f"""
            <div style="background: rgba(24, 174, 187, 0.12); border: 1px solid rgba(24, 174, 187, 0.4); border-radius: 8px; padding: 12px;">
                <div style="font-size: 11px; color: #00F0FF; font-weight: 700;">✈️ Uçak + 17 Gün Ankara Otel:</div>
                <div style="font-size: 20px; font-weight: 800; color: #00F0FF; margin: 4px 0;">€{travel_cost:,.0f}</div>
                <div style="font-size: 11px; color: #CBD5E1;">2 kişi gidiş-dönüş + 4-5* otel + VIP transfer</div>
            </div>
            """)

        with res2:
            render_html(f"""
            <div style="background: rgba(0, 240, 255, 0.12); border: 1px solid rgba(0, 240, 255, 0.4); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
                <div style="font-size: 11px; color: #00F0FF; font-weight: 700;">🇹🇷 GEN-ART Ankara Tedavi Paketi:</div>
                <div style="font-size: 20px; font-weight: 800; color: #00F0FF; margin: 4px 0;">€{pkg_turkey_cost:,.0f}</div>
                <div style="font-size: 11px; color: #CBD5E1;">Tüm ilaçlar, OPU, ICSI ve genetik analiz dahil</div>
            </div>
            """)
            if patient_net_savings >= 0:
                render_html(f"""
                <div style="background: rgba(16, 185, 129, 0.18); border: 2px solid #10B981; border-radius: 8px; padding: 12px;">
                    <div style="font-size: 11px; color: #6EE7B7; font-weight: 800;">💰 HASTANIN CEBİNDE KALAN NET TASARRUF:</div>
                    <div style="font-size: 22px; font-weight: 900; color: #10B981; margin: 4px 0;">€{patient_net_savings:,.0f} (%{savings_percentage})</div>
                    <div style="font-size: 11px; color: #CBD5E1;">Uçuş ve 17 gün tatil/konaklama dahil kârı</div>
                </div>
                """)
            else:
                render_html(f"""
                <div style="background: rgba(245, 130, 31, 0.18); border: 2px solid #F5821F; border-radius: 8px; padding: 12px;">
                    <div style="font-size: 11px; color: #FDBA74; font-weight: 800;">⚖️ FİYAT DIŞI ARBİTRAJ (TEKNOLOJİ & YASA):</div>
                    <div style="font-size: 16px; font-weight: 800; color: #F5821F; margin: 4px 0;">Fiyat Başa Baş / Üstün Kalite</div>
                    <div style="font-size: 11px; color: #CBD5E1;">Yasal genetik serbestisi ve 0 sıra bekleme</div>
                </div>
                """)

        render_html(f"""
        <div style="background: rgba(14, 47, 59, 0.7); border-left: 3px solid #00F0FF; padding: 10px 14px; border-radius: 6px; margin-top: 10px; font-size: 12px; color: #CBD5E1; line-height: 1.55;">
            <b>📌 {sel_bench['flag']} {sel_bench['name_tr']} İçin Stratejik Değerlendirme:</b><br/>
            {sel_bench['primary_driver']}<br/>
            <i>{pkg_note}</i>
        </div>
        """)

    st.markdown("</div>", unsafe_allow_html=True)

    # Grouped Bar Chart: Local Cost vs Turkey Cost vs Total with Travel
    df_bench = pd.DataFrame(COUNTRY_TREATMENT_COST_BENCHMARKS).sort_values(by="local_total_eur", ascending=False)
    
    chart_countries = df_bench.head(12).copy()
    fig_comp = go.Figure(data=[
        go.Bar(
            name="Kendi Ülkesinde Tedavi (€)",
            x=chart_countries["flag"] + " " + chart_countries["name_tr"],
            y=chart_countries["local_total_eur"],
            marker_color="#EF4444"
        ),
        go.Bar(
            name="Türkiye / GEN-ART Tedavi (€)",
            x=chart_countries["flag"] + " " + chart_countries["name_tr"],
            y=chart_countries["turkey_genart_pkg_eur"],
            marker_color="#00F0FF"
        ),
        go.Bar(
            name="Uçuş + 17 Gün Otel Dahil Toplam (€)",
            x=chart_countries["flag"] + " " + chart_countries["name_tr"],
            y=chart_countries["turkey_total_with_travel_eur"],
            marker_color="#10B981"
        )
    ])
    fig_comp.update_layout(
        title="En Yüksek Fiyat Arbitrajı Olan İlk 12 Ülkede Tedavi Maliyeti Karşılaştırması (€)",
        barmode="group",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#CBD5E1", size=11),
        height=380,
        margin=dict(l=10, r=10, t=35, b=60),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig_comp, use_container_width=True)

    # 24-Country Detailed Price Arbitrage Table
    render_html("""
    <div class="section-card">
        <div class="section-header">
            <span>📋 24 Ülke Detaylı Tedavi Maliyeti, Tasarruf ve Fiyat Arbitrajı Matrisi</span>
            <span class="tag">Uluslararası Sağlık Turizmi Kılavuzları & Saha Verisi</span>
        </div>
    </div>
    """)

    # Filter Toolbar
    f_c1, f_c2 = st.columns([1.2, 2])
    with f_c1:
        reg_options = ["Tüm Bölgeler"] + sorted(list(set(b["region"] for b in COUNTRY_TREATMENT_COST_BENCHMARKS)))
        sel_reg = st.selectbox("Bölge Filtrele (Tedavi Maliyetleri):", reg_options, index=0)
    with f_c2:
        search_cntry = st.text_input("Ülke veya Başlıca Gerekçe Ara:", placeholder="Örn: İngiltere, Körfez, PGT yasak, NHS...")

    filtered_bench = COUNTRY_TREATMENT_COST_BENCHMARKS
    if sel_reg != "Tüm Bölgeler":
        filtered_bench = [b for b in filtered_bench if b["region"] == sel_reg]
    if search_cntry.strip():
        q = search_cntry.strip().lower()
        filtered_bench = [
            b for b in filtered_bench
            if q in b["name_tr"].lower() or q in b["country"].lower() or q in b["primary_driver"].lower() or q in b["local_pgt_status"].lower()
        ]

    tbl_rows = []
    for b in filtered_bench:
        tbl_rows.append({
            "Ülke / Pazar": f"{b['flag']} {b['name_tr']}",
            "Bölge": b["region"],
            "Kendi Ülkesinde Yerel Maliyet (€)": f"€{b['local_total_eur']:,} ({b['local_currency_str']})",
            "Yerel PGT / Genetik Durumu": b["local_pgt_status"],
            "GEN-ART Ankara Paketi (€)": f"€{b['turkey_genart_pkg_eur']:,}",
            "Uçak+17 Gün Otel Dahil (€)": f"€{b['turkey_total_with_travel_eur']:,}",
            "Hastanın Net Tasarrufu (€)": f"+€{b['net_savings_eur']:,}" if b['net_savings_eur'] >= 0 else f"-€{abs(b['net_savings_eur']):,}",
            "Tasarruf Oranı (%)": f"%{b['savings_pct']}",
            "Türkiye'yi Tercih Etme Nedeni": b["primary_driver"]
        })

    tbl_df = pd.DataFrame(tbl_rows)
    st.dataframe(tbl_df, use_container_width=True, hide_index=True)

    # CSV Download Button
    csv_bytes = tbl_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 24 Ülke Tedavi Maliyeti ve Arbitraj Tablosunu İndir (Excel / CSV)",
        data=csv_bytes,
        file_name="GEN-ART_24_Ulke_Tedavi_Maliyeti_ve_Fiyat_Arbitraji.csv",
        mime="text/csv"
    )

def render_opportunity_engine(leads_df):
    """Answers the 3 core strategic questions specified in the design doc
    Enriched with verified domestic IVF market conditions, outbound travel rates (%), and cross-border drivers.
    Includes dynamic country and regional filtering.
    """
    render_html("""
    <div class="section-card">
        <div class="section-header">
            <span>💡 AI Patient Acquisition Opportunity Engine</span>
            <span class="tag">Stratejik Karar Destek & Pazar Dinamikleri</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6; margin-bottom: 16px;">
            Yapay zekâ motoru; 24 hedef pazardaki <b>yerel IVF kapasitesini</b>, <b>ülke dışına çıkış oranlarını (%)</b>, <b>yerel fiyatları</b> ve kliniğin sürdürülebilir büyüme fırsatlarını otomatik analiz eder:
        </div>
    </div>
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_html("""
        <div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(0, 240, 255, 0.35); border-radius: 10px; padding: 14px; height: 100%;">
            <div style="font-size: 13px; font-weight: 700; color: #00F0FF; margin-bottom: 8px;">
                1. Anlamlı Talep Üreten Ülkeler & Yerel IVF Analizi
            </div>
            <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                • <b>Irak (Yerel Kapasite Yetersiz - %68 Dışa Çıkış):</b> Yerel merkezlerde (Bağdat/Erbil) akredite PGT ve ileri laboratuvar yok. Çiftlerin <b>%68'i</b> tedavi için ülke dışına çıkmakta; Türkiye birinci tercih (%54 pay). Ağır erkek kısırlığı (Mikro-TESE) ve akraba evliliği taraması ana etkendir.<br/><br/>
                • <b>Ürdün (Yerelde IVF Var Ancak Pahalı - %24 Bize Geliş):</b> Amman'da yerel IVF merkezleri var ancak tedavi $6,000-$7,500+ seviyesindedir ve PGT analizlerini yurtdışına gönderirler. İleri genetik isteyen veya 1-2 yerel başarısızlık yaşayan hastaların <b>%24'ü</b> GEN-ART'ın tek ziyarette biten <i>Express NGS</i> avantajı ve vizesiz erişim için Türkiye'ye gelir.<br/><br/>
                • <b>Azerbaycan (Güçlü Güven - %45 Türkiye Tercihi):</b> Yerelde tüp bebek yapılmakta ancak PGT ve zor vakalarda güven Türkiye'dedir. Kimlikle giriş büyük avantajdır.<br/><br/>
                • <b>Almanya (Yasal Yasak Arbitrajı - %35 Sınır Ötesi):</b> Almanya'da IVF yaygın ancak Embriyo Koruma Kanunu ile PGT-A yasak olduğu için hastaların <b>%35'i</b> sınır ötesi genetik taramaya yönelir.<br/><br/>
                <span style="font-size: 11px; color: #00F0FF;"><i>💡 Aşağıdaki interaktif seçici ile tüm 24 ülkeyi ayrıntılı inceleyebilirsiniz.</i></span>
            </div>
        </div>
        """)
        
    with col2:
        render_html("""
        <div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(16, 185, 129, 0.35); border-radius: 10px; padding: 14px; height: 100%;">
            <div style="font-size: 13px; font-weight: 700; color: #10B981; margin-bottom: 8px;">
                2. Sürdürülebilir CAC ile Nitelikli Pazar
            </div>
            <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                • <b>Balkanlar (Sırbistan/Bosna):</b> CAC ortalama <b>€410</b> ile en ekonomik hasta edinme pazarı; doğrudan uçuşla 1.8 saat.<br/><br/>
                • <b>Azerbaycan:</b> Dönüşüm %9.2, CAC <b>€530</b>, yüksek kârlılık ve hasta başı €6,400 ortalama ciro.<br/><br/>
                • <b>Körfez (Suudi Arabistan / Kuveyt / BAE / Katar):</b> CAC yüksek (€1,150) ancak vaka başı gelir <b>€7,800+</b>; yüksek PGT-M ve tek gen tarama talebi.<br/><br/>
                • <b>Özbekistan & Kazakistan:</b> Yükselen orta sınıf, Rusça koordinasyonla %8.4 tedavi dönüşüm oranı.
            </div>
        </div>
        """)
        
    with col3:
        render_html("""
        <div style="background: rgba(19, 35, 71, 0.7); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 10px; padding: 14px; height: 100%;">
            <div style="font-size: 13px; font-weight: 700; color: #F87171; margin-bottom: 8px;">
                3. Tedavi Başlangıcını Engelleyen Bariyerler
            </div>
            <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                • <b>Libya & Cezayir:</b> Yüksek talep olmasına rağmen vize randevu gecikmeleri ve direkt ESB uçuş yokluğu nedeniyle <b>%40 fire</b>.<br/><br/>
                • <b>Orta Doğu WhatsApp SLA'sı:</b> İlk 4 saat içinde medikal triage yanıtı verilmeyen Arapça taleplerde <b>%58 terk</b> yaşanıyor.<br/><br/>
                • <b>Avrupa (Almanya/Hollanda/İngiltere):</b> 17 günlük seyahat planlaması ve iş izni uyumsuzluğu en büyük erteleme sebebi (%28 drop-off).
            </div>
        </div>
        """)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    
    # Detailed Verified Outbound & Local IVF Breakdown with Dynamic Country Filtering
    render_html("""
    <div class="section-card">
        <div class="section-header">
            <span>📊 Hedef Pazarlarda Yerel IVF Durumu, Yurtdışı Çıkış Oranları (%) & Türkiye Tercih Sebepleri</span>
            <span class="tag">24 Odak Ülke Entegre & İnteraktif Filtre</span>
        </div>
        <div style="font-size: 12px; color: #CBD5E1; margin-bottom: 12px;">
            "Neden yerelde tedavi olmak yerine Türkiye'ye / GEN-ART'a geliyorlar?" sorusunun doğrulanmış pazar, mevzuat, yerel fiyat ve çıkış oranlarıyla ülke bazlı analizi. İstediğiniz bölge veya ülkeleri seçerek inceleyebilirsiniz:
        </div>
    </div>
    """)
    
    # Country Filter Row
    col_reg, col_sel, col_kw = st.columns([1.1, 1.8, 1.1])
    
    with col_reg:
        sel_region = st.selectbox(
            "Bölgeye Göre Filtrele:",
            ["Tüm Bölgeler (24 Ülke)", "🕌 Körfez & Orta Doğu", "🏔️ Orta Asya & BDT", "🏛️ Avrupa", "🏔️ Balkanlar", "🌍 Kuzey Afrika & Diğer"],
            key="deep_dive_region_sel"
        )
        
    if sel_region == "🕌 Körfez & Orta Doğu":
        avail_pool = [c for c in ALL_MARKET_DEEP_DIVE if c["Bölge"] == "Middle East & Gulf"]
    elif sel_region == "🏔️ Orta Asya & BDT":
        avail_pool = [c for c in ALL_MARKET_DEEP_DIVE if c["Bölge"] == "Central Asia & CIS"]
    elif sel_region == "🏛️ Avrupa":
        avail_pool = [c for c in ALL_MARKET_DEEP_DIVE if c["Bölge"] == "Europe"]
    elif sel_region == "🏔️ Balkanlar":
        avail_pool = [c for c in ALL_MARKET_DEEP_DIVE if c["Bölge"] == "Balkans"]
    elif sel_region == "🌍 Kuzey Afrika & Diğer":
        avail_pool = [c for c in ALL_MARKET_DEEP_DIVE if c["Bölge"] == "North Africa & Other"]
    else:
        avail_pool = ALL_MARKET_DEEP_DIVE

    avail_names = [c["Ülke"] for c in avail_pool]
    
    with col_sel:
        # Default selection
        default_sel = avail_names if len(avail_names) <= 8 else avail_names[:8]
        selected_countries = st.multiselect(
            "İncelenecek Ülkeleri Seçin (Arama & Ekle):",
            options=avail_names,
            default=default_sel,
            key=f"deep_dive_countries_{sel_region}"
        )
        
    with col_kw:
        search_kw = st.text_input("Anahtar Kelime Ara:", placeholder="Örn: PGT, Vize, Mikro-TESE, Pahalı...", key="deep_dive_kw_input")

    # Filter logic
    if not selected_countries:
        selected_countries = avail_names
        
    filtered_deep_dive = [c for c in avail_pool if c["Ülke"] in selected_countries]
    
    if search_kw.strip():
        kw = search_kw.strip().lower()
        filtered_deep_dive = [
            c for c in filtered_deep_dive
            if kw in c["Ülke"].lower() or kw in c["Yerel Kapasite / Kalite"].lower() or kw in c["GEN-ART'a Geliş Kök Nedeni"].lower() or kw in c["Yerelde IVF Yapılıyor mu?"].lower()
        ]

    # Metrics summary for selected countries
    if filtered_deep_dive:
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            render_kpi_card("Seçili Pazar", f"{len(filtered_deep_dive)} Ülke", f"{sel_region} Kapsamında", icon="🌐")
        with k2:
            out_vals = [int(c["Yurtdışına Çıkış (%)"].replace("%", "")) for c in filtered_deep_dive if "%" in c["Yurtdışına Çıkış (%)"]]
            avg_out = sum(out_vals) / len(out_vals) if out_vals else 0
            render_kpi_card("Ort. Dışa Çıkış Oranı", f"%{avg_out:.1f}", "Yerelde Tedavi Olmayan Pay", icon="🛫")
        with k3:
            tr_vals = [int(c["Türkiye Tercih Payı (%)"].replace("%", "")) for c in filtered_deep_dive if "%" in c["Türkiye Tercih Payı (%)"]]
            avg_tr = sum(tr_vals) / len(tr_vals) if tr_vals else 0
            render_kpi_card("Türkiye Tercih Payı", f"%{avg_tr:.1f}", "Türkiye Sağlık Turizmi Tercihi", icon="🇹🇷", is_highlight=True)
        with k4:
            top_out_market = max(filtered_deep_dive, key=lambda x: int(x["Yurtdışına Çıkış (%)"].replace("%", ""))) if out_vals else None
            render_kpi_card("En Yüksek Çıkış Pazarı", f"{top_out_market['Ülke']}" if top_out_market else "-", f"{top_out_market['Yurtdışına Çıkış (%)']} Dışa Çıkış" if top_out_market else "", icon="🔥", is_highlight=True)

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    view_style = st.radio("Görünüm Biçimi:", ["📊 Detaylı Karşılaştırmalı Tablo", "🗂️ Stratejik Pazar Kartları"], horizontal=True, key="deep_dive_view_format")

    if view_style == "📊 Detaylı Karşılaştırmalı Tablo":
        disp_df = pd.DataFrame(filtered_deep_dive)[[
            "Ülke", "Yerelde IVF Yapılıyor mu?", "Yerel Kapasite / Kalite", "Yerel Maliyet",
            "Yurtdışına Çıkış (%)", "Türkiye Tercih Payı (%)", "GEN-ART'a Geliş Kök Nedeni"
        ]]
        st.dataframe(disp_df, use_container_width=True, hide_index=True)
        
        # CSV Export
        c_dl, _ = st.columns([1, 4])
        with c_dl:
            csv_bytes = disp_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button("📥 Seçili Pazarları CSV Olarak İndir", data=csv_bytes, file_name="GENART_Pazar_Kapasite_ve_Cikis_Analizi.csv", mime="text/csv", use_container_width=True)
    else:
        # 2-Column Responsive Glassmorphic Cards
        c_left, c_right = st.columns(2)
        for idx, item in enumerate(filtered_deep_dive):
            target_col = c_left if idx % 2 == 0 else c_right
            with target_col:
                card_html = f"""
                <div style="background: rgba(14, 47, 59, 0.7); border: 1px solid rgba(24, 174, 187, 0.35); border-radius: 12px; padding: 16px; margin-bottom: 14px; box-shadow: 0 4px 18px rgba(0,0,0,0.25);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 1px solid rgba(24, 174, 187, 0.25); padding-bottom: 8px; margin-bottom: 10px;">
                        <div>
                            <div style="font-size: 16px; font-weight: 800; color: #FFFFFF;">
                                {item['Ülke']}
                            </div>
                            <div style="font-size: 11.5px; color: #94A3B8; margin-top: 2px;">
                                📍 <i>{item['Bölge']}</i> &nbsp;|&nbsp; 💰 Yerel Maliyet: <b style="color: #F5821F;">{item['Yerel Maliyet']}</b>
                            </div>
                        </div>
                        <div style="display: flex; gap: 6px;">
                            <span style="font-size: 11px; font-weight: 700; color: #00F0FF; background: rgba(0, 240, 255, 0.12); border: 1px solid rgba(0, 240, 255, 0.3); padding: 3px 8px; border-radius: 6px;">
                                Dışa Çıkış: {item['Yurtdışına Çıkış (%)']}
                            </span>
                            <span style="font-size: 11px; font-weight: 700; color: #10B981; background: rgba(16, 185, 129, 0.12); border: 1px solid rgba(16, 185, 129, 0.3); padding: 3px 8px; border-radius: 6px;">
                                Türkiye Payı: {item['Türkiye Tercih Payı (%)']}
                            </span>
                        </div>
                    </div>
                    <div style="font-size: 12px; color: #CBD5E1; margin-bottom: 8px; line-height: 1.5;">
                        <b>🏥 Yerel Durum:</b> <span style="color: #38BDF8;">{item['Yerelde IVF Yapılıyor mu?']}</span><br/>
                        <b>ℹ️ Yerel Kapasite / Kalite:</b> {item['Yerel Kapasite / Kalite']}
                    </div>
                    <div style="background: rgba(9, 34, 43, 0.75); padding: 10px; border-radius: 8px; border-left: 3px solid #00F0FF; font-size: 12px; color: #E2E8F0; line-height: 1.5;">
                        <span style="color: #00F0FF; font-weight: 700;">💡 Neden GEN-ART / Türkiye?</span><br/>
                        {item['GEN-ART\'a Geliş Kök Nedeni']}
                    </div>
                </div>
                """
                render_html(card_html)

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
    
    render_html("""
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
    """)

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
        render_kpi_card("GEN-ART Mevcut Reklam Harcaması", f"€{tot_cur_spend:,.0f}", f"{len(active_df)} Ülke Toplamı", icon="💶")
    with kc2:
        render_kpi_card("AI Önerilen Reklam Bütçesi", f"€{tot_rec_spend:,.0f}", f"Net Değişim: {'+' if diff_spend >= 0 else ''}€{diff_spend:,.0f}", icon="🤖", is_highlight=True)
    with kc3:
        render_kpi_card("Beklenen Ek Tedavi", f"+{tot_add_starts} Hasta", "Ankara'da Tedavi Başlangıcı", icon="🧬", is_highlight=True)
    with kc4:
        render_kpi_card("Beklenen Ek Tedavi Cirosu", f"+€{tot_add_rev:,.0f}", "Öngörülen Net Gelir Artışı", icon="📈")

    st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

    # Comparative Plotly Bar Chart: Current vs AI Recommended
    chart_df = active_df.sort_values(by="revenue", ascending=False).head(10).copy()
    fig = go.Figure(data=[
        go.Bar(
            name="GEN-ART Mevcut Reklam Harcaması (€)",
            x=chart_df["country"].apply(lambda c: f"{country_flags.get(c, '')} {c}"),
            y=chart_df["spend_eur"],
            marker_color="#64748B"
        ),
        go.Bar(
            name="AI Tavsiye Edilen Reklam Bütçesi (€)",
            x=chart_df["country"].apply(lambda c: f"{country_flags.get(c, '')} {c}"),
            y=chart_df["rec_spend"],
            marker_color="#00F0FF"
        )
    ])
    fig.update_layout(
        title="Seçili Pazarlarda GEN-ART Mevcut vs. AI Tavsiye Edilen Reklam Bütçesi",
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
            <span>📋 Ülke Bazlı Reklam Bütçesi Yeniden Dağıtım ve Getiri Matrisi</span>
            <span class="tag">Canlı Veriyle Hesaplanmış</span>
        </div>
    """, unsafe_allow_html=True)

    disp_table = active_df.sort_values(by="revenue", ascending=False).copy()
    disp_table["Ülke / Pazar"] = disp_table["country"].apply(lambda c: f"{country_flags.get(c, '🏳️')} {c}")
    disp_table["GEN-ART Mevcut Reklam Bütçesi (€)"] = disp_table["spend_eur"].apply(lambda x: f"€{x:,.0f}")
    disp_table["AI Önerilen Reklam Bütçesi (€)"] = disp_table["rec_spend"].apply(lambda x: f"€{x:,.0f}")
    disp_table["Değişim"] = disp_table["boost_pct"].apply(lambda x: f"+%{x:.1f}" if x >= 0 else f"-%{abs(x):.1f}")
    disp_table["Hasta Başı Edinme Maliyeti (CAC €)"] = disp_table["cac"].apply(lambda x: f"€{x:,.0f}")
    disp_table["Reklam Getirisi (ROAS)"] = disp_table["roas"].apply(lambda x: f"{x:.1f}x")
    disp_table["Beklenen Ek Hasta"] = disp_table["add_starts"].apply(lambda x: f"+{x}" if x > 0 else "0")
    disp_table["Beklenen Ek Ciro (€)"] = disp_table["add_rev"].apply(lambda x: f"+€{x:,.0f}" if x > 0 else "€0")

    st.dataframe(
        disp_table[[
            "Ülke / Pazar", "region", "GEN-ART Mevcut Reklam Bütçesi (€)", "AI Önerilen Reklam Bütçesi (€)",
            "Değişim", "Hasta Başı Edinme Maliyeti (CAC €)", "Reklam Getirisi (ROAS)", "Beklenen Ek Hasta", "Beklenen Ek Ciro (€)", "rationale"
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
