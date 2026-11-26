"""
Data Access & Processing Engine for GEN-ART Global Patient Intelligence
Handles caching, unified filtering, metrics aggregation, and privacy-conscious transformations.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
from config import IVF_TREATMENT_PROTOCOLS
from data.mock_data import generate_leads_data, generate_country_mcda_data, generate_marketing_spend_data, get_strategic_action_plans
from data.clinical_data_loader import load_real_clinical_dataset, convert_real_to_leads_format
import openpyxl
import os

@st.cache_data(ttl=3600)
def load_all_data():
    """Loads and caches base datasets including official IVF Treatment Processes from Excel and real clinical records (yabancilar4.xlsx)"""
    real_clinical_df = load_real_clinical_dataset("yabancilar4.xlsx")
    if real_clinical_df is not None and not real_clinical_df.empty:
        # 100% pure real clinical records from yabancilar4.xlsx (no synthetic leads mixed in)
        leads_df = convert_real_to_leads_format(real_clinical_df)
    else:
        leads_df = generate_leads_data(num_records=2100)
        real_clinical_df = pd.DataFrame()

    mcda_df = generate_country_mcda_data()
    spend_df = generate_marketing_spend_data()
    actions_df = get_strategic_action_plans()
    protocols = load_ivf_protocols()
    return leads_df, mcda_df, spend_df, actions_df, protocols, real_clinical_df

def load_ivf_protocols():
    """Reads official IVF treatment protocols directly from the uploaded Excel file"""
    excel_path = "data/ivf_treatment_processes.xlsx"
    protocols = IVF_TREATMENT_PROTOCOLS.copy()
    
    if os.path.exists(excel_path):
        try:
            wb = openpyxl.load_workbook(excel_path, data_only=True)
            ws = wb["Sayfa1"]
            excel_rows = []
            for r in range(2, ws.max_row + 1):
                p_name = ws.cell(r, 1).value
                p_desc = ws.cell(r, 2).value
                if p_name:
                    excel_rows.append({"raw_protocol": str(p_name).strip(), "raw_description": str(p_desc).strip() if p_desc else ""})
            
            # Map raw strings into structured protocols
            for i, row in enumerate(excel_rows):
                if i < len(protocols):
                    protocols[i]["excel_raw_protocol"] = row["raw_protocol"]
                    protocols[i]["excel_raw_description"] = row["raw_description"]
        except Exception as e:
            print("Excel read notice:", e)
            
    return protocols

def apply_filters(leads_df, spend_df, start_date=None, end_date=None, selected_countries=None, selected_languages=None, selected_channels=None, selected_coordinator=None):
    """Applies unified executive filters across patient leads and marketing spend"""
    filtered_leads = leads_df.copy()
    filtered_spend = spend_df.copy()
    
    # Date Filtering
    if start_date:
        start_ts = pd.to_datetime(start_date)
        filtered_leads = filtered_leads[filtered_leads["inquiry_date"] >= start_ts]
    if end_date:
        end_ts = pd.to_datetime(end_date) + pd.Timedelta(days=1)
        filtered_leads = filtered_leads[filtered_leads["inquiry_date"] <= end_ts]
        
    # Country Filtering (Strict 1-to-1 country matching)
    if selected_countries and len(selected_countries) > 0:
        filtered_leads = filtered_leads[filtered_leads["country"].isin(selected_countries)]
        filtered_spend = filtered_spend[filtered_spend["country"].isin(selected_countries)]
        
    # Language Filtering
    if selected_languages and len(selected_languages) > 0:
        filtered_leads = filtered_leads[filtered_leads["language"].isin(selected_languages)]
        
    # Channel Filtering
    if selected_channels and len(selected_channels) > 0:
        filtered_leads = filtered_leads[filtered_leads["channel"].isin(selected_channels)]
        filtered_spend = filtered_spend[filtered_spend["channel"].isin(selected_channels)]
        
    # Coordinator Filtering
    if selected_coordinator and selected_coordinator != "Tümü (All)":
        filtered_leads = filtered_leads[filtered_leads["coordinator"] == selected_coordinator]
        
    return filtered_leads, filtered_spend

def calculate_executive_kpis(filtered_leads, filtered_spend):
    """Calculates the 6 core executive KPIs strictly requested in the genart-dashboard spec:
    1. Yeni Başvuru Sayısı (Total Leads / Inquiries)
    2. Konsültasyon Gerçekleşme Oranı (% of Inquiries reaching Consultation)
    3. Tedaviye Başlayan Hasta Sayısı (Treatment Starts)
    4. Başvurudan Tedaviye Dönüşüm Oranı (Overall Conversion %)
    5. Hasta Başına Pazarlama Maliyeti (Cost per Patient / CAC)
    6. Uluslararası Hasta Geliri (International Patient Revenue in EUR)
    """
    total_inquiries = len(filtered_leads)
    qualified_leads = len(filtered_leads[filtered_leads["is_qualified"] == True])
    
    # Consultations
    consultations = len(filtered_leads[filtered_leads["consultation_date"].notna()])
    
    # Treatment starts
    treatment_starts = len(filtered_leads[filtered_leads["stage"] == "5. Treatment Started - Ankara"])
    
    # Total Revenue
    total_revenue = filtered_leads["revenue"].sum()
    
    # Total Marketing Spend
    total_spend = filtered_spend["spend_eur"].sum()
    
    # Ratios
    consultation_rate = (consultations / total_inquiries * 100) if total_inquiries > 0 else 0.0
    overall_conversion = (treatment_starts / total_inquiries * 100) if total_inquiries > 0 else 0.0
    cac = (total_spend / treatment_starts) if treatment_starts > 0 else 0.0
    avg_revenue_per_patient = (total_revenue / treatment_starts) if treatment_starts > 0 else 0.0
    
    # Clinical Excel Metrics (when real HIS columns are present)
    total_opu = int(filtered_leads["opu_count"].sum()) if "opu_count" in filtered_leads.columns else 0
    total_transfers = int(filtered_leads["transfer_count"].sum()) if "transfer_count" in filtered_leads.columns else 0
    total_surgeries = int(filtered_leads["surgery_count"].sum()) if "surgery_count" in filtered_leads.columns else 0
    total_spermiograms = int(filtered_leads["spermiogram_count"].sum()) if "spermiogram_count" in filtered_leads.columns else 0
    unique_patients = int(filtered_leads["hasta_id"].nunique()) if "hasta_id" in filtered_leads.columns else total_inquiries
    stay_gt0 = filtered_leads[filtered_leads["stay_days"] > 0]["stay_days"] if "stay_days" in filtered_leads.columns else pd.Series(dtype=float)
    avg_stay_days = float(stay_gt0.mean()) if len(stay_gt0) > 0 else 0.0
    is_real = bool(filtered_leads["is_real_data"].all()) if "is_real_data" in filtered_leads.columns and len(filtered_leads) > 0 else False

    return {
        "total_inquiries": total_inquiries,
        "qualified_leads": qualified_leads,
        "consultations": consultations,
        "treatment_starts": treatment_starts,
        "consultation_rate": consultation_rate,
        "overall_conversion": overall_conversion,
        "total_spend": total_spend,
        "cac": cac,
        "total_revenue": total_revenue,
        "avg_revenue_per_patient": avg_revenue_per_patient,
        "total_opu": total_opu,
        "total_transfers": total_transfers,
        "total_surgeries": total_surgeries,
        "total_spermiograms": total_spermiograms,
        "unique_patients": unique_patients,
        "avg_stay_days": avg_stay_days,
        "is_real": is_real
    }

def get_country_performance_summary(filtered_leads, filtered_spend):
    """Summarizes performance strictly country-by-country sorted by total Excel case volume descending.
    Places empty/unknown HBYS country entries at the end so named countries rank #1 to #N accurately.
    """
    country_groups = []
    unique_countries = sorted(list(filtered_leads["country"].unique()))
    
    for country in unique_countries:
        c_leads = filtered_leads[filtered_leads["country"] == country]
        c_spend = filtered_spend[filtered_spend["country"] == country]
        
        inquiries = len(c_leads)
        consultations = len(c_leads[c_leads["consultation_date"].notna()])
        starts = len(c_leads[c_leads["stage"] == "5. Treatment Started - Ankara"])
        cvr = (starts / inquiries * 100) if inquiries > 0 else 0.0
        spend = c_spend["spend_eur"].sum()
        cac = (spend / starts) if starts > 0 else (spend if starts == 0 and spend > 0 else 0)
        revenue = c_leads["revenue"].sum()
        opu = int(c_leads["opu_count"].sum()) if "opu_count" in c_leads.columns else 0
        tx = int(c_leads["transfer_count"].sum()) if "transfer_count" in c_leads.columns else 0
        surg = int(c_leads["surgery_count"].sum()) if "surgery_count" in c_leads.columns else 0
        code = c_leads["country_code"].iloc[0] if len(c_leads) > 0 else ""
        region = c_leads["region"].iloc[0] if len(c_leads) > 0 else ""
        
        country_groups.append({
            "code": code,
            "country": country,
            "region": region,
            "inquiries": inquiries,
            "consultations": consultations,
            "treatment_starts": starts,
            "opu_count": opu,
            "transfer_count": tx,
            "surgery_count": surg,
            "conversion_rate": cvr,
            "marketing_spend": spend,
            "cac": cac,
            "revenue": revenue,
            "is_unknown": 1 if "Boş" in str(country) or "Bilinmeyen" in str(country) else 0
        })
        
    res_df = pd.DataFrame(country_groups)
    if not res_df.empty:
        # Sort named countries strictly from highest to lowest Excel case count, keeping empty HBYS rows at bottom
        res_df = res_df.sort_values(by=["is_unknown", "inquiries", "transfer_count"], ascending=[True, False, False]).reset_index(drop=True)
    return res_df

def get_overdue_tasks(filtered_leads):
    """Retrieves delayed follow-ups and SLA breached inquiries for the executive action list"""
    # Leads with SLA breach or response time > 12 hours that haven't converted
    delayed = filtered_leads[
        (filtered_leads["is_sla_breached"] == True) | 
        (filtered_leads["response_time_hrs"] > 8.0)
    ].copy()
    
    # Select key tracking fields
    cols = ["lead_id", "inquiry_date", "country", "language", "channel", "coordinator", "response_time_hrs", "stage", "drop_reason"]
    available_cols = [c for c in cols if c in delayed.columns]
    delayed = delayed[available_cols].sort_values(by="response_time_hrs", ascending=False)
    return delayed.head(15)
