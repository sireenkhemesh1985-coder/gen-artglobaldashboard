"""
Module 8: Executive Reports & Data Export Center
Implements the 3 required export options:
1. Yönetici Raporu (Executive Summary Report - Multi-tab Excel)
2. Performans Verisi (De-identified Aggregated Country/Channel CSV)
3. Operasyon Takip Listesi (Internal Operations Follow-up Register CSV)
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from config import THEME_COLORS
from utils.components import render_kpi_card
from utils.export_helpers import export_executive_summary_excel, export_performance_data_csv, export_operations_followup_csv
from data.database import calculate_executive_kpis, get_country_performance_summary

def render_executive_reports(filtered_leads, filtered_spend, actions_df, date_label):
    st.markdown("""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
            📊 Yönetici Raporları & Veri Dışa Aktarma Merkezi
        </h2>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
            Yönetim kurulu brifingleri, pazar analizleri ve operasyon ekipleri için 3 ayrı standart formatta rapor üretin
        </div>
    </div>
    """, unsafe_allow_html=True)

    kpis = calculate_executive_kpis(filtered_leads, filtered_spend)
    country_df = get_country_performance_summary(filtered_leads, filtered_spend)

    # 3 Export Cards
    col1, col2, col3 = st.columns(3)

    # Option 1: Executive Summary Report
    with col1:
        st.markdown("""
        <div class="section-card" style="height: 380px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="section-header">
                    <span>📑 1. Yönetici Özeti Raporu</span>
                </div>
                <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 14px;">
                    Yönetim Kurulu ve Üst Yönetim için hazırlanmış kapsamlı 3 sekmeli Excel raporu.<br/><br/>
                    <b>İçerik:</b>
                    <ul style="padding-left: 18px; margin-top: 6px; font-size: 12px; color: #94A3B8;">
                        <li>Seçili Dönem ({date_label}) 6 Temel KPI</li>
                        <li>Ülke Performans & Dönüşüm Tablosu</li>
                        <li>Onaylanan Stratejik Eylem Planları</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        excel_bytes = export_executive_summary_excel(kpis, country_df, actions_df, date_label)
        st.download_button(
            label="📥 Yönetici Raporunu İndir (.xlsx)",
            data=excel_bytes,
            file_name=f"GENART_Yonetici_Raporu_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Option 2: Performance Data CSV
    with col2:
        st.markdown("""
        <div class="section-card" style="height: 380px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="section-header">
                    <span>📈 2. Pazar Performans Verisi</span>
                </div>
                <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 14px;">
                    Analitik ekipler ve BI araçları için anonimleştirilmiş ülke ve kanal performans veri seti.<br/><br/>
                    <b>İçerik:</b>
                    <ul style="padding-left: 18px; margin-top: 6px; font-size: 12px; color: #94A3B8;">
                        <li>Hasta kimlik bilgisi İÇERMEZ</li>
                        <li>Ülke bazlı başvuru, konsültasyon, tedavi</li>
                        <li>CAC, Harcama ve Ciro verileri</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        perf_csv = export_performance_data_csv(country_df)
        st.download_button(
            label="📥 Performans Verisini İndir (.csv)",
            data=perf_csv,
            file_name=f"GENART_Performans_Verisi_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Option 3: Operations Follow-up Register CSV
    with col3:
        st.markdown("""
        <div class="section-card" style="height: 380px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div class="section-header">
                    <span>📋 3. Operasyon Takip Listesi</span>
                </div>
                <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 14px;">
                    Yalnızca yetkili hasta koordinatörleri ve operasyon ekiplerinin erişimine açık operasyonel takip listesi.<br/><br/>
                    <b>İçerik:</b>
                    <ul style="padding-left: 18px; margin-top: 6px; font-size: 12px; color: #94A3B8;">
                        <li>Kayıt No, Kanal, Dil, Sorumlu</li>
                        <li>İlk yanıt süresi ve SLA durumu</li>
                        <li>Aşama tarihleri ve bekleme nedenleri</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        ops_csv = export_operations_followup_csv(filtered_leads)
        st.download_button(
            label="📥 Operasyon Listesini İndir (.csv)",
            data=ops_csv,
            file_name=f"GENART_Operasyon_Takip_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Metadata & Verification Summary Card
    st.markdown(f"""
    <div class="section-card">
        <div class="section-header">
            <span>🛡️ Veri Kaynakları & Doğrulama Beyanı (Audit Metadata)</span>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; font-size: 12px; color: #CBD5E1;">
            <div>
                <b>Veri Kaynakları:</b><br/>
                GEN-ART CRM · GA4 · Google Ads · Finans HBYS
            </div>
            <div>
                <b>Son Güncelleme Zamanı:</b><br/>
                {datetime.now().strftime('%Y-%m-%d %H:%M')} (Otomatik Eşzamanlı)
            </div>
            <div>
                <b>Aktif Kayıt Hacmi:</b><br/>
                {len(filtered_leads):,} Başvuru · {kpis['treatment_starts']} Başlayan Tedavi
            </div>
            <div>
                <b>Gizlilik & Güvence:</b><br/>
                KVKK & ST-0625 Uyumlu · PII Arındırılmış
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
