"""
Realistic mock data generator for GEN-ART Global Patient Intelligence
Covers 2025 - 2026 international patient inquiries, marketing campaigns, country MCDA scores, and strategic actions.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from config import COUNTRY_COORDINATES, CLINICAL_SEGMENTS, FUNNEL_STAGES, DROP_OFF_REASONS, CHANNELS, COORDINATORS

# Seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_leads_data(num_records=2200):
    """Generates de-identified international patient lead records for 2025-2026"""
    countries = list(COUNTRY_COORDINATES.keys())
    
    # Historical health tourism volume & cross-border demand weights
    weight_map = {
        "Iraq": 0.14,
        "Azerbaijan": 0.12,
        "Jordan": 0.08,
        "Germany": 0.08,
        "Saudi Arabia": 0.07,
        "Uzbekistan": 0.06,
        "Kazakhstan": 0.06,
        "UAE": 0.05,
        "Russia": 0.05,
        "Kuwait": 0.04,
        "Qatar": 0.035,
        "United Kingdom": 0.035,
        "Italy": 0.03,
        "Netherlands": 0.025,
        "Algeria": 0.025,
        "Libya": 0.02,
        "Egypt": 0.02,
        "France": 0.018,
        "Serbia": 0.015,
        "Albania": 0.012,
        "Bosnia": 0.01,
        "Kosovo": 0.008,
        "Kyrgyzstan": 0.008,
        "Georgia": 0.007
    }
    country_weights = [weight_map.get(c, 0.02) for c in countries]
    # Normalize weights
    country_weights = [w / sum(country_weights) for w in country_weights]

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2026, 11, 15)
    days_range = (end_date - start_date).days

    records = []
    
    for i in range(1, num_records + 1):
        lead_id = f"GA-{2025 + (i % 2)}-{1000 + i}"
        country = random.choices(countries, weights=country_weights)[0]
        meta = COUNTRY_COORDINATES[country]
        
        # Primary language based on country
        lang = meta["lang"].split("/")[0]
        if "/" in meta["lang"] and random.random() > 0.4:
            lang = meta["lang"].split("/")[1]

        # Acquisition Channel
        channel = random.choices(
            CHANNELS,
            weights=[0.32, 0.28, 0.16, 0.10, 0.08, 0.06]
        )[0]
        
        campaign = f"{channel.split(' ')[0]}_{country[:3].upper()}_{lang[:3].upper()}"

        # Assign coordinator
        matched_coords = [c["name"] for c in COORDINATORS if any(r in meta["region"] for r in c["region"].split(", ")) or c["region"] == "General"]
        assigned_coord = random.choice(matched_coords) if matched_coords else "Zeynep Karaca"

        # Dates
        inq_date = start_date + timedelta(days=random.randint(0, days_range), hours=random.randint(8, 20))
        # Initial response time in hours (benchmarked: target < 4h)
        response_time_hrs = round(float(np.random.exponential(scale=3.5)) + 0.5, 1)
        first_contact_date = inq_date + timedelta(hours=response_time_hrs)

        segment = random.choice(CLINICAL_SEGMENTS)

        # Progression along the funnel
        # Inquiry -> Qualified (~40%) -> Consultation (~60% of qual) -> Accepted (~55% of consult) -> Started (~60% of accepted)
        # Or Closed-Lost at any stage
        roll = random.random()
        
        if roll < 0.55: # Qualified
            is_qualified = True
            qual_date = inq_date + timedelta(days=random.randint(1, 3))
            
            roll_consult = random.random()
            if roll_consult < 0.62: # Made it to consultation
                consult_date = qual_date + timedelta(days=random.randint(2, 7))
                
                roll_plan = random.random()
                if roll_plan < 0.58: # Treatment plan accepted
                    plan_date = consult_date + timedelta(days=random.randint(3, 10))
                    
                    roll_start = random.random()
                    if roll_start < 0.65: # Treatment started in Ankara
                        start_treat_date = plan_date + timedelta(days=random.randint(10, 30))
                        stage = "5. Treatment Started - Ankara"
                        drop_reason = None
                        
                        # Assign exact protocol from Excel calibrated by country clinical reality
                        c_reg = meta.get("region", "")
                        
                        if c_reg == "Europe":
                            # European patients (Germany, UK, Netherlands, Italy) come heavily for PGT-A due to local restrictions
                            treatment_type = random.choices([
                                "Express PGT-A NGS (Taze Transfer - 17 Gün)",
                                "Standart IVF (Taze Transfer - 17 Gün)",
                                "Donmuş Embriyo Transferi (FET - 15 Gün)",
                                "IVF + PGT (Embriyo Dondurmalı - 12+15 Gün)"
                            ], weights=[0.60, 0.22, 0.14, 0.04])[0]
                        elif "Middle East" in c_reg or "Gulf" in c_reg:
                            # Gulf patients have high consanguinity & monogenic disease screening needs
                            treatment_type = random.choices([
                                "Express PGT-A NGS (Taze Transfer - 17 Gün)",
                                "Standart IVF (Taze Transfer - 17 Gün)",
                                "Donmuş Embriyo Transferi (FET - 15 Gün)",
                                "IVF + PGT (Embriyo Dondurmalı - 12+15 Gün)"
                            ], weights=[0.42, 0.38, 0.12, 0.08])[0]
                        else:
                            # Central Asia, Balkans, North Africa
                            treatment_type = random.choices([
                                "Standart IVF (Taze Transfer - 17 Gün)",
                                "Express PGT-A NGS (Taze Transfer - 17 Gün)",
                                "Donmuş Embriyo Transferi (FET - 15 Gün)",
                                "IVF + PGT (Embriyo Dondurmalı - 12+15 Gün)"
                            ], weights=[0.52, 0.26, 0.18, 0.04])[0]
                            
                        # Set realistic revenues
                        if "Express" in treatment_type:
                            revenue = round(random.uniform(5800, 7800), -2)
                        elif "Dondurmalı" in treatment_type:
                            revenue = round(random.uniform(6400, 8900), -2)
                        elif "Donmuş" in treatment_type:
                            revenue = round(random.uniform(3400, 4800), -2)
                        else:
                            revenue = round(random.uniform(4200, 5600), -2)
                    else:
                        start_treat_date = None
                        stage = "Closed-Lost (Post-Plan)"
                        drop_reason = random.choice(["Treatment Affordability (Maliyet / Bütçe)", "Travel & Visa Barriers (Seyahat & Vize Zorluğu)", "Selected Competitor (Başka Klinik Tercihi)"])
                        revenue = 0
                        treatment_type = "Pending"
                else:
                    plan_date = None
                    start_treat_date = None
                    stage = "Closed-Lost (Post-Consultation)"
                    drop_reason = random.choice(["Treatment Affordability (Maliyet / Bütçe)", "Clinical Non-eligibility (Tıbbi Uygunsuzluk)", "Changed Mind / Postponed (Vazgeçti / Erteledi)"])
                    revenue = 0
                    treatment_type = "Pending"
            else:
                consult_date = None
                plan_date = None
                start_treat_date = None
                stage = "Closed-Lost (Post-Qualification)"
                drop_reason = random.choice(["Slow Response / Follow-up Delay (Gecikmiş İletişim)", "Travel & Visa Barriers (Seyahat & Vize Zorluğu)", "Changed Mind / Postponed (Vazgeçti / Erteledi)"])
                revenue = 0
                treatment_type = "Pending"
        else: # Disqualified early
            is_qualified = False
            qual_date = None
            consult_date = None
            plan_date = None
            start_treat_date = None
            stage = "Closed-Lost (Initial Inquiry)"
            drop_reason = random.choice(["Clinical Non-eligibility (Tıbbi Uygunsuzluk)", "Slow Response / Follow-up Delay (Gecikmiş İletişim)", "Changed Mind / Postponed (Vazgeçti / Erteledi)"])
            revenue = 0
            treatment_type = "None"

        # Check for SLA breach (unanswered > 24 hours while in early stage)
        is_sla_breached = response_time_hrs > 24.0 or (stage == "1. Inquiry Received" and (datetime.now() - inq_date).total_seconds() > 86400)

        records.append({
            "lead_id": lead_id,
            "inquiry_date": inq_date,
            "country": country,
            "country_code": meta["code"],
            "region": meta["region"],
            "language": lang,
            "channel": channel,
            "campaign": campaign,
            "coordinator": assigned_coord,
            "response_time_hrs": response_time_hrs,
            "is_sla_breached": is_sla_breached,
            "clinical_segment": segment,
            "stage": stage,
            "is_qualified": is_qualified,
            "consultation_date": consult_date,
            "treatment_start_date": start_treat_date,
            "drop_reason": drop_reason,
            "revenue": revenue,
            "treatment_type": treatment_type
        })
        
    return pd.DataFrame(records)

def generate_country_mcda_data():
    """Generates market evaluation, MCDA factors and logistics profile for all target countries
    Verified with official T.C. Dışişleri Bakanlığı (mfa.gov.tr) 2025-2026 visa regimes & real Ankara ESB flight corridors.
    """
    data = [
        {
            "country": "Iraq", "code": "IQ", "region": "Middle East & Gulf",
            "demand_score": 92, "affordability_score": 75, "travel_score": 88, 
            "differentiation_score": 85, "digital_score": 80, "regulatory_score": 82,
            "visa_type": "Yaş Şartlı Muafiyet / USHAŞ Medikal Vizesi (15-50 Yaş Vizeye Tabi)",
            "entry_doc": "Pasaport (15-50 yaş arası vizeye tabi; Schengen/ABD varsa e-Vize)",
            "medical_visa_support": "ST-0625 USHAŞ B2B Hızlı Medikal Vize Davetiyesi (48 Saat)",
            "flight_hrs": 2.0, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Bağdat/Erbil - Ankara ESB: Iraqi Airways, Pegasus)",
            "avg_stay_days": 18, "fertility_rate": 3.4, "competitor_density": "High Outbound (%68 yurt dışına çıkış / Akredite PGT yok)"
        },
        {
            "country": "Jordan", "code": "JO", "region": "Middle East & Gulf",
            "demand_score": 85, "affordability_score": 78, "travel_score": 92, 
            "differentiation_score": 70, "digital_score": 84, "regulatory_score": 88,
            "visa_type": "Pasaportla Vizesiz (90 Gün)",
            "entry_doc": "Umuma Mahsus Pasaport (180 günde 90 gün vize muafiyeti)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 1.8, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Amman - Ankara ESB: Pegasus, Royal Jordanian)",
            "avg_stay_days": 16, "fertility_rate": 2.7, "competitor_density": "Domestic IVF Var ($6,000+ pahalı / Express NGS ile %24 Türkiye'ye gelir)"
        },
        {
            "country": "Saudi Arabia", "code": "SA", "region": "Middle East & Gulf",
            "demand_score": 90, "affordability_score": 97, "travel_score": 86, 
            "differentiation_score": 92, "digital_score": 94, "regulatory_score": 88,
            "visa_type": "Pasaportla Vizesiz (23 Aralık 2023 Kararı - 90 Gün)",
            "entry_doc": "Umuma Mahsus Pasaport (Resmi Gazete 7976 sayılı Karar ile vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 3.5, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Cidde/Riyad/Medine - Ankara ESB: Flynas, Saudia, AJet)",
            "avg_stay_days": 18, "fertility_rate": 2.2, "competitor_density": "Moderate (Yüksek bütçe / Akraba evliliği monogenik PGT-M talebi)"
        },
        {
            "country": "Kuwait", "code": "KW", "region": "Middle East & Gulf",
            "demand_score": 80, "affordability_score": 95, "travel_score": 85, 
            "differentiation_score": 88, "digital_score": 90, "regulatory_score": 85,
            "visa_type": "Pasaportla Vizesiz (90 Gün)",
            "entry_doc": "Umuma Mahsus Pasaport (90 gün vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 4.2, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Kuveyt -> IST/SAW -> ESB: THY, Pegasus; yazın charter direkt)",
            "avg_stay_days": 20, "fertility_rate": 2.1, "competitor_density": "Moderate (Yüksek alım gücü / VIP hasta profili)"
        },
        {
            "country": "Qatar", "code": "QA", "region": "Middle East & Gulf",
            "demand_score": 78, "affordability_score": 98, "travel_score": 82, 
            "differentiation_score": 90, "digital_score": 92, "regulatory_score": 86,
            "visa_type": "Pasaportla Vizesiz (90 Gün)",
            "entry_doc": "Umuma Mahsus Pasaport (Resmi Gazete 7976 sayılı Karar ile vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 3.5, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Doha - Ankara ESB: Qatar Airways)",
            "avg_stay_days": 19, "fertility_rate": 1.8, "competitor_density": "Moderate (Premium Segment / PGT-M talebi)"
        },
        {
            "country": "UAE", "code": "AE", "region": "Middle East & Gulf",
            "demand_score": 82, "affordability_score": 96, "travel_score": 86, 
            "differentiation_score": 86, "digital_score": 94, "regulatory_score": 88,
            "visa_type": "Pasaportla Vizesiz (23 Aralık 2023 Kararı - 90 Gün)",
            "entry_doc": "Umuma Mahsus Pasaport (Resmi Gazete 7976 sayılı Karar ile vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 4.8, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Dubai/Abu Dhabi -> IST/SAW -> ESB: THY, Pegasus, Emirates)",
            "avg_stay_days": 18, "fertility_rate": 1.5, "competitor_density": "High (Yerel klinikler pahalı / İleri genetik için Türkiye)"
        },
        {
            "country": "Azerbaijan", "code": "AZ", "region": "Central Asia & CIS",
            "demand_score": 94, "affordability_score": 80, "travel_score": 96, 
            "differentiation_score": 92, "digital_score": 88, "regulatory_score": 95,
            "visa_type": "Kimlikle Giriş (Vizesiz - 90 Gün)",
            "entry_doc": "Yeni Tip Çipli Ulusal Kimlik Kartı veya Pasaport",
            "medical_visa_support": "Vize ve pasaportsuz kimlikle doğrudan giriş",
            "flight_hrs": 2.2, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Bakü - Ankara ESB: AZAL, AJet)",
            "avg_stay_days": 17, "fertility_rate": 1.7, "competitor_density": "Moderate (Türk hekimlerine mutlak güven / Tekrarlayan başarısız vaka)"
        },
        {
            "country": "Kazakhstan", "code": "KZ", "region": "Central Asia & CIS",
            "demand_score": 86, "affordability_score": 82, "travel_score": 80, 
            "differentiation_score": 84, "digital_score": 85, "regulatory_score": 90,
            "visa_type": "Pasaportla Vizesiz (90 Gün)",
            "entry_doc": "Umuma Mahsus Pasaport (90 gün vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 4.5, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Astana/Almatı - Ankara ESB: Scat Airlines, AJet)",
            "avg_stay_days": 21, "fertility_rate": 3.1, "competitor_density": "Moderate (Rusça koordinasyonla yüksek güven)"
        },
        {
            "country": "Uzbekistan", "code": "UZ", "region": "Central Asia & CIS",
            "demand_score": 90, "affordability_score": 72, "travel_score": 78, 
            "differentiation_score": 88, "digital_score": 79, "regulatory_score": 89,
            "visa_type": "Pasaportla Vizesiz (90 Gün)",
            "entry_doc": "Umuma Mahsus Pasaport (90 gün vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 4.2, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Taşkent - Ankara ESB: Uzbekistan Airways, AJet)",
            "avg_stay_days": 20, "fertility_rate": 3.2, "competitor_density": "Low to Moderate (Yüksek infertilite ve akraba genetik ihtiyacı)"
        },
        {
            "country": "Kyrgyzstan", "code": "KG", "region": "Central Asia & CIS",
            "demand_score": 74, "affordability_score": 65, "travel_score": 78, 
            "differentiation_score": 80, "digital_score": 75, "regulatory_score": 85,
            "visa_type": "Pasaportla Vizesiz (90 Gün)",
            "entry_doc": "Umuma Mahsus Pasaport (90 gün vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 4.8, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Bişkek - Ankara ESB: Pegasus, AJet)",
            "avg_stay_days": 20, "fertility_rate": 3.0, "competitor_density": "High Trust (Türk tıp standartlarına güçlü bağlılık)"
        },
        {
            "country": "Russia", "code": "RU", "region": "Central Asia & CIS",
            "demand_score": 85, "affordability_score": 78, "travel_score": 82, 
            "differentiation_score": 88, "digital_score": 84, "regulatory_score": 86,
            "visa_type": "Pasaportla Vizesiz (Her Girişte 60 Gün, Toplam 90 Gün)",
            "entry_doc": "Umuma Mahsus Pasaport (60 gün vize muafiyeti)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 3.2, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Moskova Vnukovo/Domodedovo - Ankara ESB: Pegasus, THY)",
            "avg_stay_days": 18, "fertility_rate": 1.5, "competitor_density": "High Demand (İleri genetik tanı ve NGS için yüksek talep)"
        },
        {
            "country": "Germany", "code": "DE", "region": "Europe",
            "demand_score": 88, "affordability_score": 92, "travel_score": 90, 
            "differentiation_score": 95, "digital_score": 90, "regulatory_score": 92,
            "visa_type": "Kimlikle Giriş (Vizesiz - 90 Gün)",
            "entry_doc": "Alman Ulusal Kimlik Kartı (Personalausweis) veya Pasaport",
            "medical_visa_support": "Kimlikle doğrudan giriş",
            "flight_hrs": 3.2, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Frankfurt/Düsseldorf/Münih/Köln/Stuttgart/Berlin - ESB: SunExpress, Pegasus, THY)",
            "avg_stay_days": 15, "fertility_rate": 1.4, "competitor_density": "Strict Law (Alman Embriyo Koruma Kanunu ile PGT-A yasak / Fırsat)"
        },
        {
            "country": "United Kingdom", "code": "GB", "region": "Europe",
            "demand_score": 84, "affordability_score": 90, "travel_score": 85, 
            "differentiation_score": 92, "digital_score": 92, "regulatory_score": 90,
            "visa_type": "Pasaportla Vizesiz (90 Gün)",
            "entry_doc": "İngiliz Pasaportu (90 gün vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 4.0, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Londra Stansted - Ankara ESB: Pegasus, AJet)",
            "avg_stay_days": 16, "fertility_rate": 1.5, "competitor_density": "NHS Waitlists (1.5-2 yıl sıra / Özel klinik maliyetleri £8,000+)"
        },
        {
            "country": "Netherlands", "code": "NL", "region": "Europe",
            "demand_score": 76, "affordability_score": 92, "travel_score": 88, 
            "differentiation_score": 89, "digital_score": 88, "regulatory_score": 91,
            "visa_type": "Kimlikle Giriş (Vizesiz - 90 Gün)",
            "entry_doc": "Hollanda Ulusal Kimlik Kartı veya Pasaport",
            "medical_visa_support": "Kimlikle doğrudan giriş",
            "flight_hrs": 4.5, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Amsterdam -> IST -> ESB: THY, Pegasus; yazın direkt charter)",
            "avg_stay_days": 15, "fertility_rate": 1.5, "competitor_density": "Strict Guidelines (Katı PGT mevzuatı / Türk diasporası)"
        },
        {
            "country": "Italy", "code": "IT", "region": "Europe",
            "demand_score": 82, "affordability_score": 88, "travel_score": 89, 
            "differentiation_score": 94, "digital_score": 88, "regulatory_score": 90,
            "visa_type": "Kimlikle Giriş (Vizesiz - 90 Gün)",
            "entry_doc": "İtalyan Kimlik Kartı (Carta d'Identità) veya Pasaport",
            "medical_visa_support": "Kimlikle doğrudan giriş",
            "flight_hrs": 4.2, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Roma/Milano -> IST -> ESB: THY, Pegasus)",
            "avg_stay_days": 16, "fertility_rate": 1.2, "competitor_density": "Law 40 Escape (Tarihsel kısıtlar ve ileri anne yaşı arayışı)"
        },
        {
            "country": "France", "code": "FR", "region": "Europe",
            "demand_score": 75, "affordability_score": 90, "travel_score": 86, 
            "differentiation_score": 88, "digital_score": 87, "regulatory_score": 89,
            "visa_type": "Kimlikle Giriş (Vizesiz - 90 Gün)",
            "entry_doc": "Fransız Kimlik Kartı (Carte Nationale d'Identité) veya Pasaport",
            "medical_visa_support": "Kimlikle doğrudan giriş",
            "flight_hrs": 4.8, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Paris CDG/ORY -> IST -> ESB: THY, Pegasus)",
            "avg_stay_days": 16, "fertility_rate": 1.8, "competitor_density": "Strict Age Limits (43 yaş üstü geri ödeme yok / Uzun bekleme)"
        },
        {
            "country": "Serbia", "code": "RS", "region": "Balkans",
            "demand_score": 70, "affordability_score": 68, "travel_score": 88, 
            "differentiation_score": 74, "digital_score": 76, "regulatory_score": 85,
            "visa_type": "Kimlikle Giriş (Vizesiz - 90 Gün)",
            "entry_doc": "Sırbistan Kimlik Kartı (Lična Karta) veya Pasaport",
            "medical_visa_support": "İkili protokol ile kimlikle doğrudan giriş",
            "flight_hrs": 1.8, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Belgrad - Ankara ESB: Air Serbia, AJet)",
            "avg_stay_days": 14, "fertility_rate": 1.5, "competitor_density": "Regional Hub (Prag/Selanik yerine uygun maliyetli Ankara)"
        },
        {
            "country": "Albania", "code": "AL", "region": "Balkans",
            "demand_score": 72, "affordability_score": 65, "travel_score": 86, 
            "differentiation_score": 75, "digital_score": 74, "regulatory_score": 84,
            "visa_type": "Pasaportla Vizesiz (90 Gün)",
            "entry_doc": "Umuma Mahsus Biyometrik Pasaport (90 gün vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 2.8, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Tiran -> IST/SAW -> ESB: Pegasus, Air Albania)",
            "avg_stay_days": 14, "fertility_rate": 1.3, "competitor_density": "Strong Medical Affinity (Türk sağlık sistemine yüksek talep)"
        },
        {
            "country": "Kosovo", "code": "XK", "region": "Balkans",
            "demand_score": 68, "affordability_score": 62, "travel_score": 85, 
            "differentiation_score": 78, "digital_score": 72, "regulatory_score": 82,
            "visa_type": "Pasaportla Vizesiz (90 Gün)",
            "entry_doc": "Kosova Biyometrik Pasaportu (90 gün vizesiz)",
            "medical_visa_support": "Vize muafiyeti nedeniyle doğrudan giriş",
            "flight_hrs": 2.8, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Priştine -> IST/SAW -> ESB: Pegasus, THY)",
            "avg_stay_days": 15, "fertility_rate": 1.6, "competitor_density": "Strong Cultural Ties (Tarihsel ve medikal bağlar)"
        },
        {
            "country": "Bosnia", "code": "BA", "region": "Balkans",
            "demand_score": 71, "affordability_score": 66, "travel_score": 86, 
            "differentiation_score": 76, "digital_score": 75, "regulatory_score": 85,
            "visa_type": "Kimlikle Giriş (Vizesiz - 90 Gün)",
            "entry_doc": "Bosna-Hersek Kimlik Kartı veya Pasaport",
            "medical_visa_support": "İkili protokol ile kimlikle doğrudan giriş",
            "flight_hrs": 3.0, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Saraybosna -> IST -> ESB: THY, Pegasus)",
            "avg_stay_days": 15, "fertility_rate": 1.2, "competitor_density": "Moderate (Boşnakça koordinasyonla yüksek güven)"
        },
        {
            "country": "Georgia", "code": "GE", "region": "North Africa & Other",
            "demand_score": 65, "affordability_score": 64, "travel_score": 92, 
            "differentiation_score": 60, "digital_score": 70, "regulatory_score": 78,
            "visa_type": "Kimlikle Giriş (Vizesiz - 90 Gün)",
            "entry_doc": "Gürcistan Kimlik Kartı veya Pasaport",
            "medical_visa_support": "Kimlikle doğrudan giriş",
            "flight_hrs": 1.5, "direct_flight": True,
            "flight_route": "✅ Direkt Sefer (Tiflis - Ankara ESB: AJet)",
            "avg_stay_days": 14, "fertility_rate": 1.8, "competitor_density": "High Domestic IVF (Yüksek teknoloji genetik için Türkiye)"
        },
        {
            "country": "Libya", "code": "LY", "region": "North Africa & Other",
            "demand_score": 84, "affordability_score": 70, "travel_score": 65, 
            "differentiation_score": 80, "digital_score": 68, "regulatory_score": 72,
            "visa_type": "USHAŞ Hızlı Medikal Vize / Konsolosluk (ST-0625 Davetiyeli)",
            "entry_doc": "Pasaport (16 yaş altı ve 55 yaş üstü vizesiz; 16-55 yaş arası vizeye tabi)",
            "medical_visa_support": "GEN-ART ST-0625 Sağlık Turizmi Davetiyesi ile USHAŞ üzerinden e-Vize onay desteği",
            "flight_hrs": 4.5, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Trablus Mitiga -> IST -> ESB: Afriqiyah, THY)",
            "avg_stay_days": 24, "fertility_rate": 2.2, "competitor_density": "Very High Outbound (%82 dışa çıkış / Yerel altyapı çökmüş durumda)"
        },
        {
            "country": "Algeria", "code": "DZ", "region": "North Africa & Other",
            "demand_score": 79, "affordability_score": 68, "travel_score": 76, 
            "differentiation_score": 82, "digital_score": 72, "regulatory_score": 78,
            "visa_type": "Konsolosluk Vizesi / e-Vize / USHAŞ Medikal Vize",
            "entry_doc": "Pasaport (15 altı & 65 üstü vizesiz; 15-65 yaş arası Schengen/ABD varsa e-Vize)",
            "medical_visa_support": "Konsolosluk veya USHAŞ B2B medikal vize hızlandırma",
            "flight_hrs": 5.2, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Cezayir Houari Boumediene -> IST -> ESB: Air Algerie, THY)",
            "avg_stay_days": 19, "fertility_rate": 2.8, "competitor_density": "High Affinity (Fransızca/Arapça koordinasyonla Türkiye tercihi)"
        },
        {
            "country": "Egypt", "code": "EG", "region": "North Africa & Other",
            "demand_score": 76, "affordability_score": 66, "travel_score": 85, 
            "differentiation_score": 78, "digital_score": 80, "regulatory_score": 80,
            "visa_type": "Kapı Vizesi (Visa on Arrival) & e-Vize (30 Gün)",
            "entry_doc": "Tüm Mısır vatandaşları sınır kapısında kapı vizesi veya e-Vize alabilir (Nisan 2023 kararı)",
            "medical_visa_support": "Sınırda 30 günlük kolay kapı vizesi",
            "flight_hrs": 3.5, "direct_flight": False,
            "flight_route": "✈️ 1 Aktarmalı (Kahire/İskenderiye -> IST -> ESB: EgyptAir, THY, Pegasus)",
            "avg_stay_days": 17, "fertility_rate": 2.9, "competitor_density": "Large Market (Fiyat hassasiyeti yüksek / İleri genetik arayışı)"
        }
    ]
    return pd.DataFrame(data)

def generate_marketing_spend_data():
    """Generates monthly campaign spend and traffic records linked by country and channel"""
    channels = ["Google Ads", "Meta Ads", "Organic SEO", "WhatsApp Healthline"]
    countries = list(COUNTRY_COORDINATES.keys())
    
    rows = []
    # Monthly records for 2026 (Jan - Nov)
    for month in range(1, 12):
        month_str = f"2026-{month:02d}"
        for country in countries:
            # Spend varies by market size
            region = COUNTRY_COORDINATES[country]["region"]
            base_budget = 1400 if "Middle East" in region else (1100 if "Europe" in region else (900 if "Central Asia" in region else 550))
            
            for ch in channels:
                spend = round(base_budget * (0.45 if ch == "Google Ads" else (0.35 if ch == "Meta Ads" else (0.12 if ch == "Organic SEO" else 0.08))) * random.uniform(0.85, 1.15), 1)
                clicks = int(spend / random.uniform(0.45, 1.20))
                impressions = clicks * random.randint(18, 35)
                
                rows.append({
                    "month": month_str,
                    "country": country,
                    "channel": ch,
                    "spend_eur": spend,
                    "clicks": clicks,
                    "impressions": impressions
                })
    return pd.DataFrame(rows)

def get_strategic_action_plans():
    """Returns approved strategic action plans strictly adhering to the prompt requirements:
    Sorun / Fırsat -> Dayanak Veri -> Karar -> Sorumlu -> Son Tarih -> Durum -> Gerçekleşen Sonuç
    """
    plans = [
        {
            "issue_opportunity": "Almanya & Hollanda'da PGT-A ve Genetik Tarama Talebinde %42 Artış",
            "evidence_data": "Almanya'da embriyo koruma kanunu kısıtlamaları nedeniyle son 6 ayda gelen 120 başvurunun 68'i PGT odaklı. Konsültasyon dönüşümü %71.",
            "decision": "Almanya ve Hollanda pazarına özel 'Genetik Danışmanlık & PGT-A Akıllı Karşılaştırma' Almanca/İngilizce bilgi landing page'i yayına alınacak.",
            "owner": "Selin Aydın & Dr. Layla Mansour",
            "deadline": "2026-12-15",
            "status": "Devam Ediyor",
            "realized_result": "İlk taslak hazırlandı, T.C. Sağlık Turizmi Tanıtım Yönetmeliği onayına sunuldu. CVR +%8 artış hedefleniyor."
        },
        {
            "issue_opportunity": "Irak ve Ürdün'de Başvurudan Konsültasyona Geçişte WhatsApp SLA Aşımı",
            "evidence_data": "Arapça gelen başvuruların %28'inde ilk yanıt süresi 4 saati aşıyor; 4 saati aşanlarda konsültasyon kabul oranı %62'den %24'e düşüyor.",
            "decision": "Bağdat ve Amman saat dilimine uygun 2. Arapça hasta koordinatörü işe alındı. 7/24 WhatsApp otomatik triage asistanı devreye girecek.",
            "owner": "Dr. Layla Mansour",
            "deadline": "2026-11-30",
            "status": "Tamamlandı",
            "realized_result": "İlk yanıt süresi 1.8 saate indi, konsültasyon randevu oranı son 30 günde %38'den %54'e yükseldi."
        },
        {
            "issue_opportunity": "Azerbaycan & Özbekistan'da 'Önceki Başarısız IVF' Vaka Akışında Yüksek Potansiyel",
            "evidence_data": "Azerbaycan'dan gelen hastaların %58'i daha önce en az 2 başarısız denemesi olan vakalar. Tedavi tamamlama geliri ortalama €6,400.",
            "decision": "Bakü'de yerel hekim ortaklığıyla 2 ayda bir online vaka değerlendirme paneli ve doğrudan Ankara transfer paketi sunulması.",
            "owner": "Elnur Mammadov",
            "deadline": "2026-12-20",
            "status": "Devam Ediyor",
            "realized_result": "Bakü'deki 3 kadın doğum merkeziyle ön protokol imzalandı, ilk grup için 8 hasta kesin kayıt oluşturdu."
        },
        {
            "issue_opportunity": "Libya Pazarında Vize ve Uçuş Gecikmeleri Nedeniyle %40 Tedavi İptali",
            "evidence_data": "Trablus'tan tedavi planı kabul edilen 15 hastanın 6'sı vize randevu gecikmesi ve direkt uçuş olmaması nedeniyle tedaviye başlayamadı.",
            "decision": "Ankara Esenboğa medikal vize hızlandırma akredite acente protokolü devreye alınacak; vize belgeleri başvuru kabulünde hazırlanacak.",
            "owner": "Zeynep Karaca",
            "deadline": "2026-11-25",
            "status": "Beklemede",
            "realized_result": "Sağlık Bakanlığı USHAŞ portalı üzerinden e-vize hızlandırma mekanizması inceleniyor."
        },
        {
            "issue_opportunity": "Sırbistan ve Balkanlar'da Düşük CAC ile Yüksek İlgi",
            "evidence_data": "Belgrad ve Saraybosna Google Ads kampanyalarında tık başı maliyet €0.42 (Avrupa ortalamasının 1/3'ü). CAC €410 seviyesinde.",
            "decision": "Balkan pazarı için aylık bütçe %25 artırılarak İngilizce/Sırpça mikro kampanya başlatılacak.",
            "owner": "Mirza Kovacevic",
            "deadline": "2026-12-05",
            "status": "Devam Ediyor",
            "realized_result": "Aylık başvuru hacmi 14'ten 28'e çıktı, ilk ayda 3 hasta Ankara'ya gelerek tedaviye başladı."
        }
    ]
    return pd.DataFrame(plans)
