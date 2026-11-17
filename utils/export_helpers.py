"""
Export utilities supporting the 3 distinct executive export types specified in the design doc:
1. Yönetici Raporu (Executive Summary Report)
2. Performans Verisi (Aggregated Performance Data - No PII)
3. Operasyon Takip Listesi (Internal Operations Follow-up Register)
"""

import io
import pandas as pd
from datetime import datetime

def export_executive_summary_excel(kpis, country_summary_df, action_plans_df, date_range_label):
    """Generates a structured multi-tab Excel Executive Report"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Tab 1: Executive KPIs
        kpi_rows = [
            {"Gösterge": "Raporlama Dönemi", "Değer": date_range_label},
            {"Gösterge": "Toplam Uluslararası Başvuru (Inquiries)", "Değer": kpis["total_inquiries"]},
            {"Gösterge": "Nitelikli Başvuru (Qualified)", "Değer": kpis["qualified_leads"]},
            {"Gösterge": "Gerçekleşen Konsültasyon", "Değer": kpis["consultations"]},
            {"Gösterge": "Konsültasyon Oranı (%)", "Değer": f"{kpis['consultation_rate']:.1f}%"},
            {"Gösterge": "Tedaviye Başlayan Hasta Sayısı", "Değer": kpis["treatment_starts"]},
            {"Gösterge": "Başvurudan Tedaviye Dönüşüm Oranı (%)", "Değer": f"{kpis['overall_conversion']:.1f}%"},
            {"Gösterge": "Toplam Pazarlama Harcaması (€)", "Değer": f"€{kpis['total_spend']:,.0f}"},
            {"Gösterge": "Hasta Başı Edinme Maliyeti (CAC €)", "Değer": f"€{kpis['cac']:,.0f}"},
            {"Gösterge": "Uluslararası Hasta Geliri (€)", "Değer": f"€{kpis['total_revenue']:,.0f}"},
            {"Gösterge": "Hasta Başı Ortalama Gelir (€)", "Değer": f"€{kpis['avg_revenue_per_patient']:,.0f}"},
            {"Gösterge": "Rapor Üretim Tarihi", "Değer": datetime.now().strftime("%Y-%m-%d %H:%M")}
        ]
        pd.DataFrame(kpi_rows).to_excel(writer, sheet_name="Yönetici Göstergeleri", index=False)
        
        # Tab 2: Country Performance
        country_export = country_summary_df.copy()
        country_export.rename(columns={
            "code": "Ülke Kodu", "country": "Ülke", "region": "Bölge",
            "inquiries": "Başvuru", "consultations": "Konsültasyon",
            "treatment_starts": "Tedavi Başlangıcı", "conversion_rate": "Dönüşüm (%)",
            "marketing_spend": "Pazarlama Harcaması (€)", "cac": "Hasta Edinme Maliyeti (€)",
            "revenue": "Gelir (€)"
        }, inplace=True)
        country_export.to_excel(writer, sheet_name="Ülke Performansı", index=False)
        
        # Tab 3: Approved Strategic Action Plans
        actions_export = action_plans_df.copy()
        actions_export.rename(columns={
            "issue_opportunity": "Sorun / Fırsat",
            "evidence_data": "Dayanak Veri",
            "decision": "Karar",
            "owner": "Sorumlu",
            "deadline": "Son Tarih",
            "status": "Durum",
            "realized_result": "Gerçekleşen Sonuç"
        }, inplace=True)
        actions_export.to_excel(writer, sheet_name="Stratejik Eylem Planları", index=False)
        
    output.seek(0)
    return output.getvalue()

def export_performance_data_csv(country_summary_df, channel_summary_df=None):
    """Exports de-identified country and channel performance data (CSV)"""
    return country_summary_df.to_csv(index=False).encode('utf-8-sig')

def export_operations_followup_csv(leads_df):
    """Exports operations tracking list with follow-up milestones for coordinators"""
    # Exclude any sensitive medical notes; include workflow tracking fields only
    cols = ["lead_id", "inquiry_date", "country", "language", "channel", "coordinator", "response_time_hrs", "is_sla_breached", "stage", "drop_reason"]
    export_df = leads_df[cols].copy()
    export_df.rename(columns={
        "lead_id": "Kayıt No",
        "inquiry_date": "Başvuru Tarihi",
        "country": "Ülke",
        "language": "Dil",
        "channel": "Kanal",
        "coordinator": "Sorumlu Koordinatör",
        "response_time_hrs": "İlk Yanıt Süresi (Saat)",
        "is_sla_breached": "SLA Aşımı",
        "stage": "Mevcut Aşama",
        "drop_reason": "Kayıp Nedeni"
    }, inplace=True)
    return export_df.to_csv(index=False).encode('utf-8-sig')
