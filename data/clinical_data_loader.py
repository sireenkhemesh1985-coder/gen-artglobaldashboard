"""
Clinical Data Loader for GEN-ART Global Patient Intelligence
Integrates real HIS / HBYS clinical patient and treatment cycle records from 'yabancilar4.xlsx'.
Includes 'tupbebex' (1,382 treatment cycles) and 'witness' (1,068 patient records).
Enforces KVKK compliance (masking options), country standardization, and clinical procedure extraction.
"""

import os
import pandas as pd
import numpy as np
from datetime import datetime

# Standard Country Mapping
COUNTRY_MAP = {
    'AFGANİSTAN İSLAM CUMHURİYETİ': ('Afghanistan', 'Central Asia & CIS', 'Pashto/Dari', 'AF'),
    'ALMANYA FEDERAL CUMHURİYETİ': ('Germany', 'Europe', 'German/Turkish', 'DE'),
    'ALMANYA FEDERAL CUMHURİYETİ / NORVEÇ KRALLIĞI': ('Germany', 'Europe', 'German/Turkish', 'DE'),
    'AMERİKA BİRLEŞİK DEVLETLERİ': ('United States', 'Europe', 'English', 'US'),
    'ARNAVUTLUK CUMHURİYETİ': ('Albania', 'Balkans', 'Albanian/English', 'AL'),
    'AVUSTRALYA': ('Australia', 'Europe', 'English', 'AU'),
    'AVUSTURYA CUMHURİYETİ': ('Austria', 'Europe', 'German', 'AT'),
    'AVUSTURYA CUMHURİYETİ / AVUSTRALYA': ('Austria', 'Europe', 'German', 'AT'),
    'AZERBAYCAN CUMHURİYETİ': ('Azerbaijan', 'Central Asia & CIS', 'Turkish/Azeri', 'AZ'),
    'BELÇİKA KRALLIĞI': ('Belgium', 'Europe', 'French/Dutch', 'BE'),
    'BOSNA HERSEK': ('Bosnia', 'Balkans', 'Bosnian/Turkish', 'BA'),
    'BULGARİSTAN CUMHURİYETİ': ('Bulgaria', 'Balkans', 'Bulgarian/Turkish', 'BG'),
    'BÜYÜK BRİTANYA VE KUZEY İRLANDA BİRLEŞİK KRALLIĞI': ('United Kingdom', 'Europe', 'English', 'GB'),
    'BİRLEŞİK ARAP EMİRLİKLERİ': ('UAE', 'Middle East & Gulf', 'Arabic', 'AE'),
    'CİBUTİ CUMHURİYETİ': ('Djibouti', 'North Africa & Other', 'French/Arabic', 'DJ'),
    'DANİMARKA KRALLIĞI': ('Denmark', 'Europe', 'Danish/English', 'DK'),
    'FRANSA CUMHURİYETİ': ('France', 'Europe', 'French/English', 'FR'),
    'FİLİSTİN DEVLETİ': ('Palestine', 'Middle East & Gulf', 'Arabic', 'PS'),
    'GÜNEY AFRİKA CUMHURİYETİ': ('South Africa', 'North Africa & Other', 'English', 'ZA'),
    'GÜRCİSTAN CUMHURİYETİ': ('Georgia', 'North Africa & Other', 'Georgian/Russian', 'GE'),
    'GİNE CUMHURİYETİ': ('Guinea', 'North Africa & Other', 'French', 'GN'),
    'HOLLANDA KRALLIĞI': ('Netherlands', 'Europe', 'Dutch/Turkish', 'NL'),
    'HİNDİSTAN CUMHURİYETİ': ('India', 'Central Asia & CIS', 'English/Hindi', 'IN'),
    'IRAK CUMHURİYETİ': ('Iraq', 'Middle East & Gulf', 'Arabic', 'IQ'),
    'IRAK CUMHURİYETİ / BİLİNMEYEN': ('Iraq', 'Middle East & Gulf', 'Arabic', 'IQ'),
    'KANADA': ('Canada', 'Europe', 'English/French', 'CA'),
    'KAZAKİSTAN CUMHURİYETİ': ('Kazakhstan', 'Central Asia & CIS', 'Russian/Kazakh', 'KZ'),
    'KIRGIZ CUMHURİYETİ': ('Kyrgyzstan', 'Central Asia & CIS', 'Russian/Kyrgyz', 'KG'),
    'KOSOVA CUMHURİYETİ': ('Kosovo', 'Balkans', 'Albanian/English', 'XK'),
    'KUVEYT DEVLETİ': ('Kuwait', 'Middle East & Gulf', 'Arabic', 'KW'),
    'KUZEY KIBRIS TÜRK CUMHURİYETİ': ('Cyprus', 'Europe', 'Turkish', 'CY'),
    'LÜBNAN CUMHURİYETİ': ('Lebanon', 'Middle East & Gulf', 'Arabic', 'LB'),
    'LÜKSEMBURG BÜYÜK DÜKALIĞI': ('Luxembourg', 'Europe', 'French/German', 'LU'),
    'MAKEDONYA CUMHURİYETİ': ('North Macedonia', 'Balkans', 'Macedonian/Turkish', 'MK'),
    'MORİTANYA İSLAM CUMHURİYETİ': ('Mauritania', 'North Africa & Other', 'Arabic/French', 'MR'),
    'NORVEÇ KRALLIĞI': ('Norway', 'Europe', 'Norwegian/English', 'NO'),
    'NİJERYA FEDERAL CUMHURİYETİ': ('Nigeria', 'North Africa & Other', 'English', 'NG'),
    'PAKİSTAN İSLAM CUMHURİYETİ': ('Pakistan', 'Central Asia & CIS', 'Urdu/English', 'PK'),
    'POLONYA CUMHURİYETİ': ('Poland', 'Europe', 'Polish/English', 'PL'),
    'RUSYA FED. / ADIGE CUMHURİYETİ': ('Russia', 'Central Asia & CIS', 'Russian', 'RU'),
    'RUSYA FEDERASYONU': ('Russia', 'Central Asia & CIS', 'Russian', 'RU'),
    'SIRBİSTAN CUMHURİYETİ': ('Serbia', 'Balkans', 'Serbian/English', 'RS'),
    'SOLOMON ADALARI': ('Solomon Islands', 'North Africa & Other', 'English', 'SB'),
    'SOMALİ FEDERAL CUMHURİYETİ': ('Somalia', 'North Africa & Other', 'Somali/Arabic', 'SO'),
    'SURİYE ARAP CUMHURİYETİ': ('Syria', 'Middle East & Gulf', 'Arabic', 'SY'),
    'SUUDİ ARABİSTAN KRALLIĞI': ('Saudi Arabia', 'Middle East & Gulf', 'Arabic', 'SA'),
    'SİNGAPUR CUMHURİYETİ': ('Singapore', 'Central Asia & CIS', 'English', 'SG'),
    'TANZANYA BİRLEŞİK CUMHURİYETİ': ('Tanzania', 'North Africa & Other', 'English/Swahili', 'TZ'),
    'UMMAN SULTANLIĞI': ('Oman', 'Middle East & Gulf', 'Arabic', 'OM'),
    'ZİMBABVE CUMHURİYETİ': ('Zimbabwe', 'North Africa & Other', 'English', 'ZW'),
    'ÇAD CUMHURİYETİ': ('Chad', 'North Africa & Other', 'French/Arabic', 'TD'),
    'ÖZBEKİSTAN CUMHURİYETİ': ('Uzbekistan', 'Central Asia & CIS', 'Russian/Uzbek', 'UZ'),
    'İRAN İSLAM CUMHURİYETİ': ('Iran', 'Middle East & Gulf', 'Persian/Turkish', 'IR'),
    'İRLANDA CUMHURİYETİ': ('Ireland', 'Europe', 'English', 'IE'),
    'İSPANYA KRALLIĞI': ('Spain', 'Europe', 'Spanish/English', 'ES'),
    'İSVEÇ KRALLIĞI': ('Sweden', 'Europe', 'Swedish/English', 'SE'),
    'İSVİÇRE KONFEDERASYONU': ('Switzerland', 'Europe', 'German/French', 'CH'),
    'İTALYA CUMHURİYETİ': ('Italy', 'Europe', 'Italian/English', 'IT')
}

def mask_text(name):
    """Masks name for KVKK privacy compliance: 'MERVE AVCİ' -> 'M*** A***'"""
    if not name or pd.isna(name):
        return ""
    name_str = str(name).strip()
    if not name_str:
        return ""
    parts = name_str.split()
    masked_parts = []
    for p in parts:
        if len(p) <= 1:
            masked_parts.append(p + "***")
        else:
            masked_parts.append(p[0] + "***")
    return " ".join(masked_parts)

def load_real_clinical_dataset(file_path="yabancilar4.xlsx"):
    """Loads and joins 'tupbebex' and 'witness' from yabancilar4.xlsx.
    Returns cleaned, enriched, and structured clinical DataFrame.
    """
    if not os.path.exists(file_path):
        return None

    try:
        df_t = pd.read_excel(file_path, sheet_name="tupbebex")
        df_w = pd.read_excel(file_path, sheet_name="witness")
    except Exception as e:
        print("Error loading yabancilar4.xlsx:", e)
        return None

    # Name lookup dictionary from witness
    w_clean = df_w.dropna(subset=['KadinAdi']).drop_duplicates(subset=['hastaid'])
    name_map = w_clean.set_index('hastaid')[['KadinAdi', 'KadinSoyadi', 'ErkekAdi', 'ErkekSoyadi']].to_dict('index')

    # Also build detailed witness lookup on (hastaid, donemno)
    w_cycle_map = df_w.set_index(['hastaid', 'donemno'])

    records = []
    for idx, row in df_t.iterrows():
        hid = row['AnalizGrupID']
        donem = row['DonemNo']
        raw_country = str(row['Ulke']).strip() if pd.notna(row['Ulke']) else "ÜLKE BİLGİSİ YOK"

        c_meta = COUNTRY_MAP.get(raw_country, ('Ülke Kaydı Boş (HBYS)', 'North Africa & Other', 'English/Arabic', 'HBYS'))
        country_name, region, lang, code = c_meta

        # Names
        names = name_map.get(hid, {})
        k_adi = names.get('KadinAdi', '')
        k_soyadi = names.get('KadinSoyadi', '')
        e_adi = names.get('ErkekAdi', '')
        e_soyadi = names.get('ErkekSoyadi', '')

        full_female = f"{k_adi} {k_soyadi}".strip() if (k_adi or k_soyadi) else ""
        full_male = f"{e_adi} {e_soyadi}".strip() if (e_adi or e_soyadi) else ""

        couple_label = ""
        if full_female and full_male:
            couple_label = f"{full_female} & {full_male}"
        elif full_female:
            couple_label = full_female
        elif full_male:
            couple_label = full_male
        else:
            couple_label = f"Uluslararası Hasta #{hid}"

        masked_couple = ""
        if full_female and full_male:
            masked_couple = f"{mask_text(full_female)} & {mask_text(full_male)}"
        elif full_female:
            masked_couple = mask_text(full_female)
        elif full_male:
            masked_couple = mask_text(full_male)
        else:
            masked_couple = f"Hasta #{str(hid)[:3]}***"

        # Dates
        ilk_randevu = pd.to_datetime(row['IlkRandevu'], errors='coerce')
        son_randevu = pd.to_datetime(row['SonRandevu'], errors='coerce')
        ilk_opu = pd.to_datetime(row['IlkOPUTarihi'], errors='coerce') if pd.notna(row['IlkOPUTarihi']) else None
        ilk_transfer = pd.to_datetime(row['IlkTransferTarihi'], errors='coerce') if pd.notna(row['IlkTransferTarihi']) else None

        # Clinical procedure counts
        opu_cnt = int(row['OPUSayisi']) if pd.notna(row['OPUSayisi']) else 0
        tx_cnt = int(row['TransferSayisi']) if pd.notna(row['TransferSayisi']) else 0
        cerrahi_cnt = int(row['CerrahiSayisi']) if pd.notna(row['CerrahiSayisi']) else 0
        sperm_cnt = int(row['SpermiogramSayisi']) if pd.notna(row['SpermiogramSayisi']) else 0
        gebe_cnt = int(row['GebeMuayenesiSayisi']) if pd.notna(row['GebeMuayenesiSayisi']) else 0
        takip_cnt = int(row['TakipMuayenesiSayisi']) if pd.notna(row['TakipMuayenesiSayisi']) else 0
        kalis_gun = int(row['TahminiKalisSuresi']) if pd.notna(row['TahminiKalisSuresi']) else 0
        toplam_randevu = int(row['ToplamRandevuSayisi']) if pd.notna(row['ToplamRandevuSayisi']) else 1
        randevu_dagilimi = str(row['RandevuTipiDagilimi']) if pd.notna(row['RandevuTipiDagilimi']) else ""

        # Witness extra fields if cycle matches
        aktif_dondurma = "H"
        cozme_var = "H"
        dondurma_sayisi = 0
        if (hid, donem) in w_cycle_map.index:
            try:
                w_row = w_cycle_map.loc[(hid, donem)]
                if isinstance(w_row, pd.DataFrame):
                    w_row = w_row.iloc[0]
                aktif_dondurma = str(w_row.get('aktifdondurma', 'H'))
                cozme_var = str(w_row.get('cozmevar', 'H'))
                dondurma_sayisi = int(w_row.get('dondurmakayitsayisi', 0)) if pd.notna(w_row.get('dondurmakayitsayisi')) else 0
            except Exception:
                pass

        # Determine treatment type and stage
        if tx_cnt > 0:
            stage = "5. Treatment Started - Ankara"
            if "PGD" in randevu_dagilimi or "PGT" in randevu_dagilimi or "Express" in randevu_dagilimi or region == "Europe":
                treatment_type = "Express PGT-A NGS (Taze Transfer - 17 Gün)"
                revenue = 6800
            elif "DET" in randevu_dagilimi or cozme_var == "E":
                treatment_type = "Donmuş Embriyo Transferi (FET - 15 Gün)"
                revenue = 3800
            else:
                treatment_type = "Standart IVF (Taze Transfer - 17 Gün)"
                revenue = 5200
        elif opu_cnt > 0:
            stage = "4. Treatment Plan Accepted"
            treatment_type = "IVF + PGT (Embriyo Dondurmalı - 12+15 Gün)"
            revenue = 3400
        elif cerrahi_cnt > 0:
            stage = "3. Medical Consultation"
            treatment_type = "Mikro-TESE & Cerrahi Androloji Tedavisi"
            revenue = 1800
        elif sperm_cnt > 0:
            stage = "2. Qualified Lead"
            treatment_type = "Androloji Değerlendirme & Sperm Dondurma"
            revenue = 750
        else:
            stage = "1. Inquiry Received"
            treatment_type = "Genel İnfertilite & Ön Konsültasyon"
            revenue = 450

        # Default clinical segment
        if cerrahi_cnt > 0 or "TESE" in randevu_dagilimi:
            segment = "Severe Male Infertility & Andrology (Şiddetli Erkek Kısırlığı)"
        elif "PGD" in randevu_dagilimi or "PGT" in randevu_dagilimi or "Express" in treatment_type:
            segment = "Inherited Genetic Disease & PGT (Kalıtsal Hastalıklar / PGT)"
        elif donem > 1 or "DET" in randevu_dagilimi:
            segment = "Previous Unsuccessful IVF (Tekrarlayan Başarısız IVF)"
        elif dondurma_sayisi > 0 or aktif_dondurma == "E":
            segment = "Fertility Preservation (Doğurganlık Koruma & Oosit Dondurma)"
        else:
            segment = "Patients Exploring IVF Abroad (Yurtdışı Tüp Bebek Planlama)"

        # Clinical Outcome
        if gebe_cnt > 0:
            outcome = "✅ Klinik Gebelik Onaylandı"
        elif tx_cnt > 0:
            outcome = "⏳ Embriyo Transferi Tamamlandı (Test Bekleniyor)"
        elif opu_cnt > 0:
            outcome = "❄️ OPU Tamamlandı (Embriyolar Donduruldu / PGT Sürecinde)"
        elif cerrahi_cnt > 0:
            outcome = "🔬 Cerrahi / TESE Gerçekleştirildi"
        else:
            outcome = "📋 Ön Teşhis / Muayene Aşamasında"

        records.append({
            "record_id": f"HIS-{hid}-{donem}",
            "hasta_id": hid,
            "donem_no": donem,
            "raw_country": raw_country,
            "country": country_name,
            "country_code": code,
            "region": region,
            "language": lang,
            "couple_label": couple_label,
            "masked_couple": masked_couple,
            "female_name": full_female,
            "male_name": full_male,
            "start_date": ilk_randevu,
            "end_date": son_randevu,
            "year": ilk_randevu.year if pd.notna(ilk_randevu) else 2024,
            "stay_days": kalis_gun,
            "total_appointments": toplam_randevu,
            "opu_count": opu_cnt,
            "transfer_count": tx_cnt,
            "surgery_count": cerrahi_cnt,
            "spermiogram_count": sperm_cnt,
            "pregnancy_checkups": gebe_cnt,
            "tracking_ultrasounds": takip_cnt,
            "treatment_type": treatment_type,
            "stage": stage,
            "segment": segment,
            "clinical_outcome": outcome,
            "revenue": revenue,
            "active_freeze": aktif_dondurma,
            "thawed": cozme_var,
            "freeze_records": dondurma_sayisi,
            "raw_details": randevu_dagilimi
        })

    real_df = pd.DataFrame(records)
    return real_df

def convert_real_to_leads_format(real_df):
    """Converts real clinical records to the schema expected by the patient funnel & marketing pipeline"""
    if real_df is None or len(real_df) == 0:
        return pd.DataFrame()

    lead_rows = []
    # Map country to organic/direct channel (Reflecting real clinic arrivals without active ads)
    channel_by_country = {
        'Germany': 'Direct Website & Live Chat',
        'Netherlands': 'Direct Website & Live Chat',
        'France': 'Direct Website & Live Chat',
        'United States': 'Direct Website & Live Chat',
        'United Kingdom': 'Direct Website & Live Chat',
        'Austria': 'Direct Website & Live Chat',
        'Sweden': 'Direct Website & Live Chat',
        'Iraq': 'WhatsApp Healthline',
        'Azerbaijan': 'Medical Referral / Partner',
        'Uzbekistan': 'Medical Referral / Partner',
        'Georgia': 'Medical Referral / Partner',
        'UAE': 'WhatsApp Healthline',
        'Kuwait': 'WhatsApp Healthline',
        'Saudi Arabia': 'WhatsApp Healthline',
        'Algeria': 'Direct Website & Live Chat',
        'Libya': 'WhatsApp Healthline'
    }

    # Coordinator map by region
    coord_by_region = {
        'Middle East & Gulf': 'Layla Mansoor',
        'Central Asia & CIS': 'Rustam Aliyev',
        'Europe': 'Anna Schmidt',
        'Balkans': 'Elena Rossi',
        'North Africa & Other': 'Zeynep Karaca'
    }

    for idx, r in real_df.iterrows():
        c_name = r['country']
        reg = r['region']
        ch = channel_by_country.get(c_name, 'Medical Referral / Partner')
        coord = coord_by_region.get(reg, 'Zeynep Karaca')

        s_date = r['start_date'] if pd.notna(r['start_date']) else pd.to_datetime('2024-01-01')
        e_date = r['end_date'] if pd.notna(r['end_date']) else s_date

        lead_rows.append({
            "lead_id": r['record_id'],
            "inquiry_date": s_date,
            "country": c_name,
            "country_code": r['country_code'],
            "region": reg,
            "language": r['language'].split('/')[0] if '/' in r['language'] else r['language'],
            "channel": ch,
            "campaign": f"HBYS_{r['country_code']}_Clinical_Registry",
            "coordinator": coord,
            "response_time_hrs": 2.4,
            "is_sla_breached": False,
            "clinical_segment": r['segment'],
            "stage": r['stage'],
            "is_qualified": True,
            "consultation_date": s_date,
            "treatment_start_date": e_date if r['transfer_count'] > 0 else None,
            "drop_reason": None if r['stage'] == '5. Treatment Started - Ankara' else "Changed Mind / Postponed (Vazgeçti / Erteledi)",
            "revenue": r['revenue'],
            "treatment_type": r['treatment_type'],
            "hasta_id": r['hasta_id'],
            "year": r['year'],
            "patient_name": r['couple_label'],
            "masked_patient_name": r['masked_couple'],
            "stay_days": r['stay_days'],
            "opu_count": r['opu_count'],
            "transfer_count": r['transfer_count'],
            "surgery_count": r['surgery_count'],
            "spermiogram_count": r['spermiogram_count'],
            "pregnancy_checkups": r['pregnancy_checkups'],
            "clinical_outcome": r['clinical_outcome'],
            "is_real_data": True
        })

    return pd.DataFrame(lead_rows)

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    df = load_real_clinical_dataset()
    if df is not None:
        print(f"Loaded {len(df)} real clinical records successfully.")
        converted = convert_real_to_leads_format(df)
        print(f"Converted {len(converted)} records to leads schema.")
