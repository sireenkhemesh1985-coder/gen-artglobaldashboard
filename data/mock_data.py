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
                        
                        # Assign exact protocol from Excel
                        if "Genetic" in segment:
                            treatment_type = random.choice([
                                "IVF + PGT (Embriyo Dondurmalı - 12+15 Gün)",
                                "Express PGT-A NGS (Taze Transfer - 17 Gün)"
                            ])
                            revenue = round(random.uniform(6200, 8800), -2)
                        elif "Previous" in segment:
                            treatment_type = "Express PGT-A NGS (Taze Transfer - 17 Gün)"
                            revenue = round(random.uniform(5800, 7500), -2)
                        elif "Preservation" in segment:
                            treatment_type = "Donmuş Embriyo Transferi (FET - 15 Gün)"
                            revenue = round(random.uniform(3400, 4800), -2)
                        else:
                            treatment_type = "Standart IVF (Taze Transfer - 17 Gün)"
                            revenue = round(random.uniform(4200, 5400), -2)
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
    """Generates market evaluation, MCDA factors and logistics profile for all target countries"""
    data = [
        {
            "country": "Iraq", "code": "IQ", "region": "Middle East & Gulf",
            "demand_score": 92, "affordability_score": 75, "travel_score": 88, 
            "differentiation_score": 85, "digital_score": 80, "regulatory_score": 82,
            "visa_type": "Easy Sticker / Medical B2B", "flight_hrs": 2.0, "direct_flight": True,
            "avg_stay_days": 18, "fertility_rate": 3.4, "competitor_density": "High (Jordan/Turkey)"
        },
        {
            "country": "Jordan", "code": "JO", "region": "Middle East & Gulf",
            "demand_score": 85, "affordability_score": 78, "travel_score": 92, 
            "differentiation_score": 70, "digital_score": 84, "regulatory_score": 88,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 1.8, "direct_flight": True,
            "avg_stay_days": 16, "fertility_rate": 2.7, "competitor_density": "Very High (Domestic IVF)"
        },
        {
            "country": "Saudi Arabia", "code": "SA", "region": "Middle East & Gulf",
            "demand_score": 90, "affordability_score": 97, "travel_score": 86, 
            "differentiation_score": 92, "digital_score": 94, "regulatory_score": 88,
            "visa_type": "e-Visa / Easy Visa (90 Days)", "flight_hrs": 3.5, "direct_flight": True,
            "avg_stay_days": 18, "fertility_rate": 2.2, "competitor_density": "Moderate (High Purchasing Power / Premium PGT)"
        },
        {
            "country": "Kuwait", "code": "KW", "region": "Middle East & Gulf",
            "demand_score": 80, "affordability_score": 95, "travel_score": 85, 
            "differentiation_score": 88, "digital_score": 90, "regulatory_score": 85,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 3.0, "direct_flight": True,
            "avg_stay_days": 20, "fertility_rate": 2.1, "competitor_density": "Moderate (High Purchasing Power)"
        },
        {
            "country": "Qatar", "code": "QA", "region": "Middle East & Gulf",
            "demand_score": 78, "affordability_score": 98, "travel_score": 82, 
            "differentiation_score": 90, "digital_score": 92, "regulatory_score": 86,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 3.5, "direct_flight": True,
            "avg_stay_days": 19, "fertility_rate": 1.8, "competitor_density": "Moderate (Premium Segment)"
        },
        {
            "country": "UAE", "code": "AE", "region": "Middle East & Gulf",
            "demand_score": 82, "affordability_score": 96, "travel_score": 86, 
            "differentiation_score": 86, "digital_score": 94, "regulatory_score": 88,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 3.8, "direct_flight": True,
            "avg_stay_days": 18, "fertility_rate": 1.5, "competitor_density": "High (Local Hubs)"
        },
        {
            "country": "Azerbaijan", "code": "AZ", "region": "Central Asia & CIS",
            "demand_score": 94, "affordability_score": 80, "travel_score": 96, 
            "differentiation_score": 92, "digital_score": 88, "regulatory_score": 95,
            "visa_type": "Visa Free (Identity Card)", "flight_hrs": 2.2, "direct_flight": True,
            "avg_stay_days": 17, "fertility_rate": 1.7, "competitor_density": "Moderate (Strong Trust in Turkey)"
        },
        {
            "country": "Kazakhstan", "code": "KZ", "region": "Central Asia & CIS",
            "demand_score": 86, "affordability_score": 82, "travel_score": 80, 
            "differentiation_score": 84, "digital_score": 85, "regulatory_score": 90,
            "visa_type": "Visa Free (30 Days)", "flight_hrs": 4.5, "direct_flight": True,
            "avg_stay_days": 21, "fertility_rate": 3.1, "competitor_density": "Moderate (Russian/Local)"
        },
        {
            "country": "Uzbekistan", "code": "UZ", "region": "Central Asia & CIS",
            "demand_score": 90, "affordability_score": 72, "travel_score": 78, 
            "differentiation_score": 88, "digital_score": 79, "regulatory_score": 89,
            "visa_type": "Visa Free (30 Days)", "flight_hrs": 4.2, "direct_flight": True,
            "avg_stay_days": 20, "fertility_rate": 3.2, "competitor_density": "Low to Moderate"
        },
        {
            "country": "Kyrgyzstan", "code": "KG", "region": "Central Asia & CIS",
            "demand_score": 74, "affordability_score": 65, "travel_score": 78, 
            "differentiation_score": 80, "digital_score": 75, "regulatory_score": 85,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 4.8, "direct_flight": True,
            "avg_stay_days": 20, "fertility_rate": 3.0, "competitor_density": "High Trust in Turkish Medical Standards"
        },
        {
            "country": "Russia", "code": "RU", "region": "Central Asia & CIS",
            "demand_score": 85, "affordability_score": 78, "travel_score": 82, 
            "differentiation_score": 88, "digital_score": 84, "regulatory_score": 86,
            "visa_type": "Visa Free (60 Days)", "flight_hrs": 3.2, "direct_flight": True,
            "avg_stay_days": 18, "fertility_rate": 1.5, "competitor_density": "High Demand for Advanced Genetics & NGS"
        },
        {
            "country": "Germany", "code": "DE", "region": "Europe",
            "demand_score": 88, "affordability_score": 92, "travel_score": 90, 
            "differentiation_score": 95, "digital_score": 90, "regulatory_score": 92,
            "visa_type": "Visa Free (EU)", "flight_hrs": 3.2, "direct_flight": True,
            "avg_stay_days": 15, "fertility_rate": 1.4, "competitor_density": "Strict Embryo Laws in DE (Opportunity for PGT)"
        },
        {
            "country": "United Kingdom", "code": "GB", "region": "Europe",
            "demand_score": 84, "affordability_score": 90, "travel_score": 85, 
            "differentiation_score": 92, "digital_score": 92, "regulatory_score": 90,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 4.0, "direct_flight": True,
            "avg_stay_days": 16, "fertility_rate": 1.5, "competitor_density": "NHS Waitlists / High Private Costs"
        },
        {
            "country": "Netherlands", "code": "NL", "region": "Europe",
            "demand_score": 76, "affordability_score": 92, "travel_score": 88, 
            "differentiation_score": 89, "digital_score": 88, "regulatory_score": 91,
            "visa_type": "Visa Free (EU)", "flight_hrs": 3.5, "direct_flight": True,
            "avg_stay_days": 15, "fertility_rate": 1.5, "competitor_density": "Strict Guidelines (High PGT demand)"
        },
        {
            "country": "Italy", "code": "IT", "region": "Europe",
            "demand_score": 82, "affordability_score": 88, "travel_score": 89, 
            "differentiation_score": 94, "digital_score": 88, "regulatory_score": 90,
            "visa_type": "Visa Free (EU)", "flight_hrs": 2.5, "direct_flight": True,
            "avg_stay_days": 16, "fertility_rate": 1.2, "competitor_density": "High Cross-Border Seeker (Law 40 escape)"
        },
        {
            "country": "France", "code": "FR", "region": "Europe",
            "demand_score": 75, "affordability_score": 90, "travel_score": 86, 
            "differentiation_score": 88, "digital_score": 87, "regulatory_score": 89,
            "visa_type": "Visa Free (EU)", "flight_hrs": 3.5, "direct_flight": True,
            "avg_stay_days": 16, "fertility_rate": 1.8, "competitor_density": "Strict Age Limits / Long Waiting Lists"
        },
        {
            "country": "Serbia", "code": "RS", "region": "Balkans",
            "demand_score": 70, "affordability_score": 68, "travel_score": 88, 
            "differentiation_score": 74, "digital_score": 76, "regulatory_score": 85,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 1.8, "direct_flight": True,
            "avg_stay_days": 14, "fertility_rate": 1.5, "competitor_density": "Regional (Prague/Greece)"
        },
        {
            "country": "Albania", "code": "AL", "region": "Balkans",
            "demand_score": 72, "affordability_score": 65, "travel_score": 86, 
            "differentiation_score": 75, "digital_score": 74, "regulatory_score": 84,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 1.5, "direct_flight": True,
            "avg_stay_days": 14, "fertility_rate": 1.3, "competitor_density": "High affinity for Turkish healthcare"
        },
        {
            "country": "Kosovo", "code": "XK", "region": "Balkans",
            "demand_score": 68, "affordability_score": 62, "travel_score": 85, 
            "differentiation_score": 78, "digital_score": 72, "regulatory_score": 82,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 1.6, "direct_flight": True,
            "avg_stay_days": 15, "fertility_rate": 1.6, "competitor_density": "Strong cultural ties"
        },
        {
            "country": "Bosnia", "code": "BA", "region": "Balkans",
            "demand_score": 71, "affordability_score": 66, "travel_score": 86, 
            "differentiation_score": 76, "digital_score": 75, "regulatory_score": 85,
            "visa_type": "Visa Free (90 Days)", "flight_hrs": 1.7, "direct_flight": True,
            "avg_stay_days": 15, "fertility_rate": 1.2, "competitor_density": "Moderate"
        },
        {
            "country": "Georgia", "code": "GE", "region": "North Africa & Other",
            "demand_score": 65, "affordability_score": 64, "travel_score": 92, 
            "differentiation_score": 60, "digital_score": 70, "regulatory_score": 78,
            "visa_type": "Visa Free (Identity Card)", "flight_hrs": 1.5, "direct_flight": True,
            "avg_stay_days": 14, "fertility_rate": 1.8, "competitor_density": "High Domestic IVF / Surrogacy Hub"
        },
        {
            "country": "Libya", "code": "LY", "region": "North Africa & Other",
            "demand_score": 84, "affordability_score": 70, "travel_score": 65, 
            "differentiation_score": 80, "digital_score": 68, "regulatory_score": 72,
            "visa_type": "Consular Visa Required", "flight_hrs": 3.2, "direct_flight": False,
            "avg_stay_days": 24, "fertility_rate": 2.2, "competitor_density": "High Demand / Travel Bottlenecks"
        },
        {
            "country": "Algeria", "code": "DZ", "region": "North Africa & Other",
            "demand_score": 79, "affordability_score": 68, "travel_score": 76, 
            "differentiation_score": 82, "digital_score": 72, "regulatory_score": 78,
            "visa_type": "e-Visa / Consular Visa", "flight_hrs": 3.8, "direct_flight": True,
            "avg_stay_days": 19, "fertility_rate": 2.8, "competitor_density": "High Medical Affinity for Türkiye"
        },
        {
            "country": "Egypt", "code": "EG", "region": "North Africa & Other",
            "demand_score": 76, "affordability_score": 66, "travel_score": 85, 
            "differentiation_score": 78, "digital_score": 80, "regulatory_score": 80,
            "visa_type": "e-Visa / Visa on Arrival", "flight_hrs": 2.2, "direct_flight": True,
            "avg_stay_days": 17, "fertility_rate": 2.9, "competitor_density": "Large Regional Market / Price Sensitive"
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
