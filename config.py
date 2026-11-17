"""
GEN-ART Global Patient Intelligence Platform Configuration
Visual Identity: Dark Navy & Turquoise Executive Design
"""

APP_TITLE = "GEN-ART | Global Patient Intelligence"
APP_SUBTITLE = "AI-Powered International Patient Acquisition, Market Intelligence & Conversion Management"
HEALTH_TOURISM_AUTH = "ST-0625"
CLINIC_LOCATION = "Ankara, Türkiye"
CLINIC_COORDINATES = [32.8597, 39.9334]  # Ankara Lon, Lat

# Color Palette (Gen-Art Official Brand: Teal #15736D, Cyan #18AEBB, Orange #F5821F)
THEME_COLORS = {
    "background": "#051319",
    "background_gradient": "radial-gradient(circle at 15% 10%, #0d2a35 0%, #051319 65%, #020a0e 100%)",
    "surface": "#09222B",
    "surface_card": "#0E2F3B",
    "surface_card_hover": "#133C4B",
    "border": "#174C5E",
    "teal": "#15736D",
    "turquoise": "#00F0FF",
    "cyan_logo": "#18AEBB",
    "orange_logo": "#F5821F",
    "orange_neon": "#FF8C1A",
    "turquoise_glow": "rgba(0, 240, 255, 0.4)",
    "orange_glow": "rgba(245, 130, 31, 0.4)",
    "text_primary": "#F8FAFC",
    "text_secondary": "#A5C4CF",
    "text_muted": "#6E93A0",
    "success": "#10B981",
    "warning": "#F5821F",
    "danger": "#EF4444",
    "purple": "#8B5CF6"
}

# Country Groups & Focus Markets (Aligned with Official Spec & Global Cross-Border IVF Demand)
MARKET_GROUPS = {
    "Middle East & Gulf": ["Iraq", "Jordan", "Saudi Arabia", "Kuwait", "Qatar", "UAE"],
    "Central Asia & CIS": ["Azerbaijan", "Kazakhstan", "Uzbekistan", "Kyrgyzstan", "Russia"],
    "Europe": ["Germany", "United Kingdom", "Netherlands", "Italy", "France"],
    "Balkans": ["Serbia", "Albania", "Kosovo", "Bosnia"],
    "North Africa & Other": ["Libya", "Algeria", "Egypt", "Georgia"]
}

COUNTRY_COORDINATES = {
    "Iraq": {"lat": 33.3152, "lon": 44.3661, "code": "IQ", "region": "Middle East & Gulf", "lang": "Arabic"},
    "Jordan": {"lat": 31.9522, "lon": 35.2332, "code": "JO", "region": "Middle East & Gulf", "lang": "Arabic"},
    "Saudi Arabia": {"lat": 24.7136, "lon": 46.6753, "code": "SA", "region": "Middle East & Gulf", "lang": "Arabic"},
    "Kuwait": {"lat": 29.3759, "lon": 47.9774, "code": "KW", "region": "Middle East & Gulf", "lang": "Arabic"},
    "Qatar": {"lat": 25.2854, "lon": 51.5310, "code": "QA", "region": "Middle East & Gulf", "lang": "Arabic"},
    "UAE": {"lat": 24.4539, "lon": 54.3773, "code": "AE", "region": "Middle East & Gulf", "lang": "Arabic"},
    "Azerbaijan": {"lat": 40.4093, "lon": 49.8671, "code": "AZ", "region": "Central Asia & CIS", "lang": "Turkish/Azeri"},
    "Kazakhstan": {"lat": 51.1694, "lon": 71.4491, "code": "KZ", "region": "Central Asia & CIS", "lang": "Russian/Kazakh"},
    "Uzbekistan": {"lat": 41.2995, "lon": 69.2401, "code": "UZ", "region": "Central Asia & CIS", "lang": "Russian/Uzbek"},
    "Kyrgyzstan": {"lat": 42.8746, "lon": 74.5698, "code": "KG", "region": "Central Asia & CIS", "lang": "Russian/Kyrgyz"},
    "Russia": {"lat": 55.7558, "lon": 37.6173, "code": "RU", "region": "Central Asia & CIS", "lang": "Russian"},
    "Germany": {"lat": 52.5200, "lon": 13.4050, "code": "DE", "region": "Europe", "lang": "German/Turkish"},
    "United Kingdom": {"lat": 51.5074, "lon": -0.1278, "code": "GB", "region": "Europe", "lang": "English"},
    "Netherlands": {"lat": 52.3676, "lon": 4.9041, "code": "NL", "region": "Europe", "lang": "Dutch/Turkish"},
    "Italy": {"lat": 41.9028, "lon": 12.4964, "code": "IT", "region": "Europe", "lang": "Italian/English"},
    "France": {"lat": 48.8566, "lon": 2.3522, "code": "FR", "region": "Europe", "lang": "French/English"},
    "Serbia": {"lat": 44.7866, "lon": 20.4489, "code": "RS", "region": "Balkans", "lang": "Serbian/English"},
    "Albania": {"lat": 41.3275, "lon": 19.8187, "code": "AL", "region": "Balkans", "lang": "Albanian/English"},
    "Kosovo": {"lat": 42.6629, "lon": 21.1655, "code": "XK", "region": "Balkans", "lang": "Albanian/English"},
    "Bosnia": {"lat": 43.8563, "lon": 18.4131, "code": "BA", "region": "Balkans", "lang": "Bosnian/Turkish"},
    "Georgia": {"lat": 41.7151, "lon": 44.8271, "code": "GE", "region": "North Africa & Other", "lang": "Georgian/Russian"},
    "Libya": {"lat": 32.8872, "lon": 13.1913, "code": "LY", "region": "North Africa & Other", "lang": "Arabic"},
    "Algeria": {"lat": 36.7538, "lon": 3.0588, "code": "DZ", "region": "North Africa & Other", "lang": "Arabic/French"},
    "Egypt": {"lat": 30.0444, "lon": 31.2357, "code": "EG", "region": "North Africa & Other", "lang": "Arabic/English"}
}

# Infertility / Genetics Clinical Segments
CLINICAL_SEGMENTS = [
    "Previous Unsuccessful IVF (Tekrarlayan Başarısız IVF)",
    "Severe Male Infertility & Andrology (Şiddetli Erkek Kısırlığı)",
    "Inherited Genetic Disease & PGT (Kalıtsal Hastalıklar / PGT)",
    "Patients Exploring IVF Abroad (Yurtdışı Tüp Bebek Planlama)",
    "Fertility Preservation (Doğurganlık Koruma & Oosit Dondurma)"
]

# Funnel Stages & Sequence
FUNNEL_STAGES = [
    "1. Inquiry Received (Yeni Başvuru)",
    "2. Qualified Lead (Nitelikli Ön Değerlendirme)",
    "3. Medical Consultation (Doktor Konsültasyonu)",
    "4. Treatment Plan Accepted (Tedavi Planı Kabulü)",
    "5. Treatment Started - Ankara (Tedavi Başlangıcı)"
]

# Drop-off Reasons (Closed-Lost)
DROP_OFF_REASONS = [
    "Treatment Affordability (Maliyet / Bütçe)",
    "Travel & Visa Barriers (Seyahat & Vize Zorluğu)",
    "Changed Mind / Postponed (Vazgeçti / Erteledi)",
    "Clinical Non-eligibility (Tıbbi Uygunsuzluk)",
    "Slow Response / Follow-up Delay (Gecikmiş İletişim)",
    "Selected Competitor (Başka Klinik Tercihi)"
]

# Clinical IVF Protocols (Extracted directly from IVF SÜREÇLERİ.xlsx)
IVF_TREATMENT_PROTOCOLS = [
    {
        "id": "standard_fresh",
        "name": "Standart IVF Protokolü (PGT'siz & Taze Transfer)",
        "original_text": "Standart ivf protocol( no pgt and fresh embrio transfer)",
        "start_day": "Adetin 2. veya 3. günü",
        "stay_days": 17,
        "visits": 1,
        "description": "Adetin 2. veya 3. gününde başlar ve 17 gün kesintisiz kalış gerektirir. Stimülasyon, OPU ve 5. gün taze embriyo transferi tamamlanır.",
        "target_group": "Genetik risk taşımayan standart infertilite vakaları",
        "visa_req": "Tek girişli (Single Entry) 30 günlük vize yeterli",
        "color": "#00B4D8"
    },
    {
        "id": "pgt_freeze",
        "name": "IVF + PGT (Embriyo Dondurmalı - 2 Aşamalı)",
        "original_text": "Ivf + pgt , with embrio freezing.",
        "start_day": "1. Aşama Adetin 2-3. günü / 2. Aşama 1-2 ay sonra",
        "stay_days": 27, # 12 + 15
        "first_stay": 12,
        "second_stay": 15,
        "visits": 2,
        "description": "1. Ziyaret: Adetin 2-3. günü başlar, 12 gün kalış (OPU + Biyopsi + Dondurma). 1-2 ay sonra 2. Ziyaret: 14-15 gün kalış ile donmuş embriyo transferi yapılır.",
        "target_group": "Kalıtsal genetik hastalık (PGT-M/SR), translokasyon ve detaylı genetik tarama vakaları",
        "visa_req": "Çift girişli veya Çoklu (Multiple Entry) medikal vize gerektirir",
        "color": "#8B5CF6"
    },
    {
        "id": "pgt_express",
        "name": "IVF + PGT (Express PGT-A NGS - Taze Transfer)",
        "original_text": "Ivf+pgt (express pgt -A NGS ) Fresh embrio transfer",
        "start_day": "Adetin 2. veya 3. günü",
        "stay_days": 17,
        "visits": 1,
        "description": "Adetin 2. veya 3. gününde başlar ve 17 gün kesintisiz kalış gerektirir. GEN-ART akredite genetik laboratuvarında Express NGS ile embriyolar dondurulmadan taze transfer edilir.",
        "target_group": "İleri anne yaşı, tekrarlayan başarısız IVF ve 2. kez seyahat masrafı istemeyen uluslararası hastalar",
        "visa_req": "Tek girişli (Single Entry) 30 günlük vize yeterli (Yüksek maliyet/zaman tasarrufu)",
        "color": "#00F0FF"
    },
    {
        "id": "fet_transfer",
        "name": "Donmuş Embriyo Transferi (FET - Frozen Embryo Transfer)",
        "original_text": "Frozen embrio transfer",
        "start_day": "Adetin 2. veya 3. günü",
        "stay_days": 15,
        "visits": 1,
        "description": "Adetin 2. veya 3. gününde başlar ve 14-15 gün kalış gerektirir. Endometrium hazırlığı sonrasında dondurulmuş embriyonun transferi gerçekleştirilir.",
        "target_group": "Dondurulmuş embriyosu bulunan veya 2. aşamaya gelen hastalar",
        "visa_req": "Tek girişli 30 günlük vize yeterli",
        "color": "#10B981"
    }
]
CHANNELS = [
    "Google Ads (Search & Discovery)",
    "Meta Campaigns (IG & FB)",
    "Organic Search & SEO",
    "Direct Website & Live Chat",
    "WhatsApp Healthline",
    "Medical Referral / Partner"
]

# Multilingual Coordinators
COORDINATORS = [
    {"name": "Dr. Layla Mansour", "languages": "Arabic, English", "region": "Middle East & Gulf, North Africa"},
    {"name": "Elnur Mammadov", "languages": "Turkish, Azeri, Russian", "region": "Central Asia & CIS"},
    {"name": "Selin Aydin", "languages": "English, German, French, Turkish", "region": "Europe"},
    {"name": "Mirza Kovacevic", "languages": "Bosnian, Serbian, Italian, English", "region": "Balkans"},
    {"name": "Zeynep Karaca", "languages": "Turkish, English, Russian, Arabic", "region": "General"}
]
