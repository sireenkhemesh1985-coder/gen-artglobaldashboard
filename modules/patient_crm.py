"""
Module 3: International Patient CRM & Conversion Drop-off Analyzer
Pinpoints exactly where and why international patients are lost across the acquisition pipeline.
Distinguishes marketing drop-offs from operational, clinical, and logistics roadblocks.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import THEME_COLORS, DROP_OFF_REASONS, MARKET_GROUPS
from utils.components import render_kpi_card

def render_patient_crm(filtered_leads, real_clinical_df=None):
    if real_clinical_df is None or real_clinical_df.empty:
        from data.clinical_data_loader import load_real_clinical_dataset
        real_clinical_df = load_real_clinical_dataset()

    st.markdown("""
    <div style="margin-bottom: 12px;">
        <h2 style="color: #FFFFFF; font-size: 20px; font-weight: 700; margin: 0;">
            👥 Uluslararası Hasta CRM & Gerçek Klinik HBYS Veritabanı
        </h2>
        <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
            Gerçek klinik hasta döngüleri (OPU, Transfer, Cerrahi, Kalış Süreleri) ile lead kazanım hunisi kayıp kök nedenlerini tek ekranda yönetin
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_real_his, tab_dropoff, tab_simulator, tab_leads = st.tabs([
        "🏥 Gerçek Klinik HBYS Veritabanı (1,382 Vaka)",
        "🔍 Kayıp Nedenleri Kök Neden Analizi",
        "🎛️ Hasta Dönüşüm Simülatörü",
        "📋 CRM Lead Takip Listesi"
    ])

    with tab_real_his:
        render_real_his_database(real_clinical_df)

    with tab_dropoff:
        render_dropoff_breakdown(filtered_leads)

    with tab_simulator:
        render_conversion_simulator()

    with tab_leads:
        render_leads_table(filtered_leads)

def render_real_his_database(real_df):
    """Renders the comprehensive real clinical database (yabancilar4.xlsx: tupbebex & witness)"""
    if real_df is None or real_df.empty:
        st.warning("⚠️ Gerçek klinik veri seti (yabancilar4.xlsx) bulunamadı.")
        return

    # Top Context Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(14, 47, 59, 0.8) 0%, rgba(21, 115, 109, 0.45) 100%); border: 1px solid rgba(0, 240, 255, 0.35); border-radius: 10px; padding: 14px 18px; margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
            <div>
                <span style="font-size: 15px; font-weight: 800; color: #00F0FF; letter-spacing: 0.5px;">
                    🏥 GEN-ART Gerçek Klinik & HBYS Vaka Veritabanı
                </span>
                <span style="font-size: 11px; background: rgba(0, 240, 255, 0.15); color: #00F0FF; padding: 3px 8px; border-radius: 4px; font-weight: 600; margin-left: 8px;">
                    yabancilar4.xlsx (tupbebex & witness)
                </span>
                <div style="font-size: 12px; color: #CBD5E1; margin-top: 4px; line-height: 1.5;">
                    Kliniğinize ait <b>1,382 tedavi siklusu</b> ve <b>1,068 uluslararası hasta ailesi</b> doğrudan sistemle bütünleştirilmiştir.
                    Tüm OPU (Yumurta Toplama), Embriyo Transferi, Cerrahi Operasyon, Dondurma/Çözme ve Ankara Kalış Süreleri canlı olarak incelenebilir.
                </div>
            </div>
            <div style="display: flex; gap: 8px;">
                <span style="background: rgba(16, 185, 129, 0.15); color: #10B981; border: 1px solid rgba(16, 185, 129, 0.4); padding: 5px 12px; border-radius: 6px; font-size: 11px; font-weight: 700;">
                    ✓ Doğrulanmış HBYS
                </span>
                <span style="background: rgba(245, 130, 31, 0.15); color: #F5821F; border: 1px solid rgba(245, 130, 31, 0.4); padding: 5px 12px; border-radius: 6px; font-size: 11px; font-weight: 700;">
                    🛡️ ST-0625 Akredite
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 1. KPI Cards
    total_cycles = len(real_df)
    unique_patients = real_df["hasta_id"].nunique()
    total_opu = int(real_df["opu_count"].sum())
    total_tx = int(real_df["transfer_count"].sum())
    total_surgery = int(real_df["surgery_count"].sum())
    total_sperm = int(real_df["spermiogram_count"].sum())
    avg_stay = real_df["stay_days"].mean()
    est_total_rev = real_df["revenue"].sum()

    kcol1, kcol2, kcol3, kcol4, kcol5, kcol6 = st.columns(6)
    with kcol1:
        render_kpi_card("Toplam Siklus", f"{total_cycles:,}", f"{unique_patients:,} benzersiz çift", icon="📁")
    with kcol2:
        opu_rate = (total_opu / total_cycles * 100) if total_cycles > 0 else 0
        render_kpi_card("Başarılı OPU", f"{total_opu:,}", f"%{opu_rate:.1f} Yumurta Toplama", icon="🔬", is_highlight=True)
    with kcol3:
        tx_rate = (total_tx / total_cycles * 100) if total_cycles > 0 else 0
        render_kpi_card("Embriyo Transferi", f"{total_tx:,}", f"%{tx_rate:.1f} ET/DET Transferi", icon="🧬", is_highlight=True)
    with kcol4:
        render_kpi_card("Cerrahi & TESE", f"{total_surgery:,}", f"{total_sperm} Spermiogram", icon="🩺")
    with kcol5:
        render_kpi_card("Ort. Kalış Süresi", f"{avg_stay:.1f} Gün", "17 Gün Express NGS Modeli", icon="⏱️")
    with kcol6:
        render_kpi_card("Klinik Ciro Hacmi", f"€{est_total_rev:,.0f}", f"Ort. €{est_total_rev/total_cycles:,.0f}/vaka", icon="💶")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # 2. KVKK Madde 6 Privacy Toggle and Filter Bar
    fcol1, fcol2, fcol3 = st.columns([1.5, 1.2, 1.3])
    with fcol1:
        mask_toggle = st.toggle(
            "🔒 Hasta İsimlerini Maskele (KVKK Madde 6 Uyarınca)",
            value=True,
            help="Aktifken: 'M*** A*** & C*** A***' olarak özel sağlık verisi korunur. Kapatıldığında yetkili hekimler için tam isimler açılır."
        )
    with fcol2:
        search_query = st.text_input("🔍 İsim, Hasta No veya Ülke Ara:", "", placeholder="Örn: Germany, 1002, Sarah...")
    with fcol3:
        proc_filter = st.selectbox(
            "Klinik İşlem Filtresi:",
            ["Tüm Vakalar (1,382)", "Yalnızca OPU Yapılanlar (795)", "Yalnızca Transfer Yapılanlar (614)", "Cerrahi / TESE Yapılanlar (79)", "Dondurma Kaydı Olanlar", "Çözme Yapılanlar (FET)"]
        )

    # Apply interactive filters to view
    view_df = real_df.copy()
    if search_query:
        sq = search_query.strip().lower()
        view_df = view_df[
            view_df["couple_label"].str.lower().str.contains(sq, na=False) |
            view_df["masked_couple"].str.lower().str.contains(sq, na=False) |
            view_df["country"].str.lower().str.contains(sq, na=False) |
            view_df["hasta_id"].astype(str).str.contains(sq, na=False) |
            view_df["record_id"].str.lower().str.contains(sq, na=False)
        ]

    if proc_filter == "Yalnızca OPU Yapılanlar (795)":
        view_df = view_df[view_df["opu_count"] > 0]
    elif proc_filter == "Yalnızca Transfer Yapılanlar (614)":
        view_df = view_df[view_df["transfer_count"] > 0]
    elif proc_filter == "Cerrahi / TESE Yapılanlar (79)":
        view_df = view_df[view_df["surgery_count"] > 0]
    elif proc_filter == "Dondurma Kaydı Olanlar":
        view_df = view_df[view_df["freeze_records"] > 0]
    elif proc_filter == "Çözme Yapılanlar (FET)":
        view_df = view_df[view_df["thawed"] == "E"]

    # 3. Two Analytical Charts (Country Breakdown & Stay Duration / Express NGS Fit)
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1.1, 1])

    with c1:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>🌍 En Çok Hasta Gelen İlk 15 Ülke Dağılımı (HBYS Verisi)</span>
                <span class="tag">58 Ülke Arasından</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 8px;">
                GEN-ART'ı bizzat Ankara'da ziyaret eden yabancı çiftlerin vatandaşı olduğu ülkeler
            </div>
        """, unsafe_allow_html=True)

        country_counts = real_df["country"].value_counts().head(15).reset_index()
        country_counts.columns = ["Ülke", "Hasta Sayısı"]
        country_counts = country_counts.sort_values(by="Hasta Sayısı", ascending=True)

        fig_country = px.bar(
            country_counts,
            x="Hasta Sayısı",
            y="Ülke",
            orientation="h",
            text="Hasta Sayısı",
            color="Hasta Sayısı",
            color_continuous_scale=[[0, "#15736D"], [1, "#00F0FF"]]
        )
        fig_country.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            margin=dict(l=10, r=20, t=10, b=10),
            height=340,
            coloraxis_showscale=False,
            xaxis=dict(showgrid=True, gridcolor="rgba(24, 174, 187, 0.15)", title=""),
            yaxis=dict(title="", tickfont=dict(size=11))
        )
        fig_country.update_traces(
            texttemplate="%{text}",
            textposition="outside",
            marker=dict(line=dict(width=0))
        )
        st.plotly_chart(fig_country, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>⏱️ Ankara'da Kalış Süresi Dağılımı ve 17 Gün Express NGS Uyumu</span>
                <span class="tag">Klinik Doğrulama</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-bottom: 8px;">
                Hastaların Ankara'da geçirdiği gün sayısı (Ortalama 12.4 Gün, Express NGS zirvesi 15-21 gün)
            </div>
        """, unsafe_allow_html=True)

        # Segment stay durations into meaningful bins
        bins = [0, 7, 14, 21, 100]
        labels = ["1-7 Gün (Kısa / Ön Tetkik)", "8-14 Gün (Hızlı Protokol)", "15-21 Gün (17 Gün Express NGS Zirvesi ⭐)", "22+ Gün (Uzun Takip / Cerrahi)"]
        stay_binned = pd.cut(real_df["stay_days"].clip(lower=1), bins=bins, labels=labels).value_counts().reindex(labels).reset_index()
        stay_binned.columns = ["Kalış Süresi Aralığı", "Vaka Sayısı"]

        fig_stay = px.bar(
            stay_binned,
            x="Kalış Süresi Aralığı",
            y="Vaka Sayısı",
            text="Vaka Sayısı",
            color="Kalış Süresi Aralığı",
            color_discrete_map={
                "1-7 Gün (Kısa / Ön Tetkik)": "#4A6B82",
                "8-14 Gün (Hızlı Protokol)": "#15736D",
                "15-21 Gün (17 Gün Express NGS Zirvesi ⭐)": "#00F0FF",
                "22+ Gün (Uzun Takip / Cerrahi)": "#F5821F"
            }
        )
        fig_stay.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            margin=dict(l=10, r=10, t=10, b=10),
            height=340,
            showlegend=False,
            xaxis=dict(showgrid=False, title="", tickangle=-15, tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor="rgba(24, 174, 187, 0.15)", title="")
        )
        fig_stay.update_traces(
            texttemplate="%{text} Vaka",
            textposition="outside"
        )
        st.plotly_chart(fig_stay, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. Detailed Clinical Table
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>📋 Gerçek Klinik Döngü & Tedavi Kayıtları Listesi</span>
            <span class="tag">Canlı Tablo ({} Vaka)</span>
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
            {}
        </div>
    """.format(
        len(view_df),
        "🔒 <b>KVKK Madde 6 Koruması Aktif:</b> Hasta ve eş isimleri maskelenmiştir (Örn: M*** A***)." if mask_toggle else "🔓 <b>Açık İsim Görünümü:</b> Yetkili hekim doğrulaması için tam hasta isimleri listelenmektedir."
    ), unsafe_allow_html=True)

    table_df = view_df.copy()
    table_df["hasta_adi"] = table_df["masked_couple"] if mask_toggle else table_df["couple_label"]
    table_df["tarih_str"] = table_df["start_date"].dt.strftime("%d.%m.%Y")
    table_df["ciro_str"] = table_df["revenue"].apply(lambda x: f"€{x:,.0f}")
    table_df["kalis_str"] = table_df["stay_days"].apply(lambda x: f"{x} gün")

    display_cols = [
        "record_id", "hasta_adi", "country", "tarih_str", "kalis_str",
        "opu_count", "transfer_count", "surgery_count", "spermiogram_count",
        "active_freeze", "thawed", "clinical_outcome", "ciro_str"
    ]

    col_names = {
        "record_id": "Protokol No",
        "hasta_adi": "Hasta / Çift Adı (KVKK)",
        "country": "Ülke",
        "tarih_str": "İlk Randevu",
        "kalis_str": "Ankara Kalış",
        "opu_count": "OPU (Yumurta)",
        "transfer_count": "Transfer (ET)",
        "surgery_count": "Cerrahi / TESE",
        "spermiogram_count": "Sperm Testi",
        "active_freeze": "Dondurma",
        "thawed": "Çözme",
        "clinical_outcome": "Klinik Durum / Sonuç",
        "ciro_str": "Tahmini Paket (€)"
    }

    st.dataframe(
        table_df[display_cols].rename(columns=col_names),
        use_container_width=True,
        height=450,
        hide_index=True
    )

    # One-Click CSV Export
    csv_bytes = table_df[display_cols].rename(columns=col_names).to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Bu Tabloyu CSV Olarak İndir (Excel Uyumlu UTF-8 BOM)",
        data=csv_bytes,
        file_name="genart_gercek_klinik_hbys_veritabani.csv",
        mime="text/csv",
        use_container_width=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

def render_dropoff_breakdown(leads_df):
    """Visualizes reasons why inquiries dropped out of the funnel"""
    lost_leads = leads_df[leads_df["drop_reason"].notna()]
    total_lost = len(lost_leads)
    
    # Detailed Context & Data Source Notification Box
    st.markdown("""
    <div style="background: rgba(14, 47, 59, 0.7); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 10px; padding: 14px 18px; margin-bottom: 14px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <span style="font-size: 14px; font-weight: 700; color: #00F0FF;">
                ℹ️ Bu Veriler Neyi İfade Eder ve Hangi Süreçte Yaşanır? (CRM Kayıp Metodolojisi)
            </span>
            <span style="font-size: 11px; background: rgba(0, 240, 255, 0.15); color: #00F0FF; padding: 3px 8px; border-radius: 4px; font-weight: 600;">
                Klinik Başvuru Süreci (Lead Funnel) Kayıpları
            </span>
        </div>
        <div style="font-size: 12px; color: #CBD5E1; line-height: 1.65;">
            <b>📌 Süreç Tanımı:</b> Bu analizdeki kayıplar hastaların kendi ülkelerinde durduk yere vazgeçmesi <u>değildir</u>. Uluslararası bir çift GEN-ART ile iletişime geçtiği andan (WhatsApp, Web Formu, Çağrı) Ankara'da tedavi masasına oturana kadar olan <b>CRM İletişim Tünelinde (Closed-Lost)</b> yaşanan engellerdir:<br/>
            • <b>Gecikmiş İletişim / Slow Response:</b> Hastanın ilk mesajına 4 saatten geç yanıt verilmesi sonucu iletişimin kopması (SLA aşımı).<br/>
            • <b>Vazgeçti / Erteledi / Changed Mind:</b> Doktor görüşmesinden sonra hastanın iş izni, ailevi veya döngü ertelemesi sebebiyle tedaviyi ileri tarihe atması.<br/>
            • <b>Tıbbi Uygunsuzluk / Clinical Non-eligibility:</b> Hastanın kendi ülkesinde yaptırıp gönderdiği ön tetkiklerde (yurtdışı gelmeden test.xlsx) over rezervinin tükenmiş olması veya ağır tıbbi engeller nedeniyle hekimin tedaviye onay vermemesi.<br/>
            • <b>Seyahat & Vize Zorluğu / Travel & Visa Barriers:</b> Vize randevusu alamama veya Ankara uçuş/konaklama organize edememe.<br/>
            • <b>Maliyet / Bütçe / Treatment Affordability:</b> Tedavi + seyahat bütçesini yüksek bulma.<br/>
            • <b>Başka Klinik Tercihi / Selected Competitor:</b> İstanbul, Kıbrıs veya yerel bir kliniğe yönelme.<br/>
            <div style="margin-top: 6px; padding: 6px 10px; background: rgba(245, 130, 31, 0.1); border-left: 3px solid #F5821F; border-radius: 4px; font-size: 11px; color: #FF8C1A;">
                💡 <b>Veri Kaynağı:</b> Kliniğinize ait resmi CRM/Excel hasta listeniz henüz yüklenmediği için, bu veriler <i>genart-dashboard.docx</i> şartnamesindeki uluslararası sağlık turizmi CRM benchmark modeline göre çalışmaktadır. Kendi veri dosyanızı yüklediğinizde oranlar anlık olarak kendi gerçek vaka verilerinizle güncellenecektir.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        render_kpi_card("Toplam Kaybedilen Başvuru", f"{total_lost:,}", f"İncelenen {len(leads_df)} vaka içinden", icon="📉")
    with col2:
        maliyet_kaybi = len(lost_leads[lost_leads["drop_reason"].str.contains("Maliyet|Affordability", na=False)])
        maliyet_pct = (maliyet_kaybi / total_lost * 100) if total_lost > 0 else 0
        render_kpi_card("Bütçe / Fiyat Kaynaklı", f"%{maliyet_pct:.1f}", f"{maliyet_kaybi} hasta bütçeyi yüksek buldu", icon="💶")
    with col3:
        sla_kaybi = len(lost_leads[lost_leads["drop_reason"].str.contains("Gecikmiş|Slow", na=False)])
        sla_pct = (sla_kaybi / total_lost * 100) if total_lost > 0 else 0
        render_kpi_card("İletişim & Yanıt Gecikmesi", f"%{sla_pct:.1f}", f"{sla_kaybi} hasta geç yanıttan dolayı koptu", icon="⏱️")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    
    c_pie, c_bar = st.columns([1, 1.3])
    
    with c_pie:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>📊 Kayıp Nedenleri Dağılımı</span>
            </div>
        """, unsafe_allow_html=True)
        
        reason_counts = lost_leads["drop_reason"].value_counts().reset_index()
        reason_counts.columns = ["Neden", "Adet"]
        
        fig = px.pie(
            reason_counts,
            names="Neden",
            values="Adet",
            hole=0.45,
            color_discrete_sequence=["#EF4444", "#F59E0B", "#00B4D8", "#8B5CF6", "#64748B", "#EC4899"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            margin=dict(l=10, r=10, t=20, b=10),
            height=300,
            showlegend=True,
            legend=dict(orientation="h", y=-0.2)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with c_bar:
        st.markdown("""
        <div class="section-card">
            <div class="section-header">
                <span>🌍 Ülkelere Göre Kayıp Sebepleri & Dinamik Pazar Seçimi</span>
            </div>
            <div style="font-size: 11px; color: #94A3B8; margin-bottom: 8px;">
                💡 <b>Pazar Seçim Rasyoneli:</b> Doğrudan Ankara (ESB) uçuş hatları, vize muafiyeti/kolaylığı ve yerel mevzuat kısıtları (Almanya/İtalya genetik kısıtlamaları, İngiltere bekleme süreleri) sebebiyle Türkiye'den en çok IVF talep eden odaklar listelenmiştir.
            </div>
        """, unsafe_allow_html=True)
        
        country_loss = lost_leads.groupby(["country", "drop_reason"]).size().reset_index(name="Kayıp_Adedi")
        all_avail_countries = sorted(lost_leads["country"].unique().tolist())
        top_default = list(leads_df["country"].value_counts().head(6).index)
        
        col_flt1, col_flt2 = st.columns([1, 1.4])
        with col_flt1:
            region_preset = st.selectbox(
                "Bölge / Hızlı Küme:",
                ["🔥 En Çok Başvuru Alan 6 Ülke", "🌐 Tüm Ülkeleri Göster", "🕌 Körfez & Orta Doğu", "🏛️ Avrupa Pazarları", "🏔️ Orta Asya & BDT", "🌍 Kuzey Afrika & Diğer"],
                key="crm_region_preset"
            )
        
        if region_preset == "🔥 En Çok Başvuru Alan 6 Ülke":
            preset_countries = top_default
        elif region_preset == "🌐 Tüm Ülkeleri Göster":
            preset_countries = all_avail_countries
        elif region_preset == "🕌 Körfez & Orta Doğu":
            preset_countries = [c for c in all_avail_countries if c in MARKET_GROUPS.get("Middle East & Gulf", [])]
        elif region_preset == "🏛️ Avrupa Pazarları":
            preset_countries = [c for c in all_avail_countries if c in MARKET_GROUPS.get("Europe", [])]
        elif region_preset == "🏔️ Orta Asya & BDT":
            preset_countries = [c for c in all_avail_countries if c in MARKET_GROUPS.get("Central Asia & CIS", [])]
        elif region_preset == "🌍 Kuzey Afrika & Diğer":
            preset_countries = [c for c in all_avail_countries if c in MARKET_GROUPS.get("North Africa & Other", []) or c in MARKET_GROUPS.get("Balkans", [])]
        else:
            preset_countries = top_default

        with col_flt2:
            selected_chart_countries = st.multiselect(
                "Grafikte İncelenecek Ülkeler:",
                options=all_avail_countries,
                default=preset_countries if preset_countries else top_default,
                key=f"crm_dynamic_country_picker_{region_preset}"
            )
        
        if not selected_chart_countries:
            selected_chart_countries = top_default
            
        country_loss_filtered = country_loss[country_loss["country"].isin(selected_chart_countries)]
        
        fig_bar = px.bar(
            country_loss_filtered,
            x="country",
            y="Kayıp_Adedi",
            color="drop_reason",
            title=f"Kayıp Kök Nedenleri Ayrımı ({len(selected_chart_countries)} Ülke Karşılaştırması)",
            barmode="stack",
            color_discrete_sequence=["#EF4444", "#F59E0B", "#00B4D8", "#8B5CF6", "#64748B", "#EC4899"],
            labels={"country": "Ülke", "Kayıp_Adedi": "Kayıp Başvuru Sayısı", "drop_reason": "Kayıp Nedeni"}
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#CBD5E1", size=11),
            margin=dict(l=10, r=10, t=30, b=10),
            height=320,
            legend=dict(
                orientation="h",
                y=-0.26,
                x=0,
                title="",
                font=dict(size=10)
            )
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

def render_conversion_simulator():
    """Interactive Patient conversion simulator matching docx spec Section 5"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🧮 İnteraktif Hasta Dönüşüm Simülatörü</span>
            <span class="tag">Varsayım Modeli</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.5; margin-bottom: 16px;">
            Örneğin: GEN-ART bir ülkeden 100 başvuru aldığında aşama geçiş oranlarını değiştirerek nihai tedaviye başlayan hasta sayısını ve beklenen ciroyu anlık simüle edebilirsiniz.
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        inquiries = st.number_input("Aylık Başvuru Hacmi", min_value=10, max_value=2000, value=100, step=10)
    with col2:
        r1 = st.slider("1. Başvuru → Nitelikli (%)", 10, 100, 50, step=5) / 100.0
    with col3:
        r2 = st.slider("2. Nitelikli → Konsültasyon (%)", 10, 100, 60, step=5) / 100.0
    with col4:
        r3 = st.slider("3. Konsültasyon → Tedavi (%)", 5, 80, 20, step=1) / 100.0

    # Calculations
    qualified = inquiries * r1
    consulted = qualified * r2
    treatment_starts = consulted * r3
    overall_cvr = (treatment_starts / inquiries) * 100.0
    est_revenue = treatment_starts * 5500.0  # Average package €5,500
    
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    c_res1, c_res2, c_res3, c_res4 = st.columns(4)
    with c_res1:
        render_kpi_card("Nitelikli Başvuru", f"{qualified:.1f}", f"%{r1*100:.0f} Ön Kabul", icon="1️⃣")
    with c_res2:
        render_kpi_card("Gerçekleşen Konsültasyon", f"{consulted:.1f}", f"%{r2*100:.0f} Doktor Randevusu", icon="2️⃣")
    with c_res3:
        render_kpi_card("Beklenen Tedavi Başlangıcı", f"{treatment_starts:.1f}", "Ayda Kesin Başlayan", icon="🧬", is_highlight=True)
    with c_res4:
        render_kpi_card("Toplam Dönüşüm / Ciro", f"%{overall_cvr:.1f}", f"Tahmini Ciro: €{est_revenue:,.0f}", icon="💶", is_highlight=True)

    st.markdown("</div>", unsafe_allow_html=True)

def render_leads_table(leads_df):
    """De-identified register table for international patient leads"""
    st.markdown("""
    <div class="section-card">
        <div class="section-header">
            <span>🛡️ KVKK Uyumlu Anonim Hasta Takip Listesi (CRM)</span>
            <span class="tag">Kişisel Veri İçermez</span>
        </div>
        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 12px;">
            Yönetici kokpiti seviyesinde hasta isimleri veya özel klinik notlar gizlenmiştir. Süreç, koordinatör ve dönüşüm durumu takip edilir.
        </div>
    """, unsafe_allow_html=True)
    
    filter_stage = st.multiselect("Aşama Filtresi:", leads_df["stage"].unique(), default=None)
    
    display_leads = leads_df.copy()
    if filter_stage:
        display_leads = display_leads[display_leads["stage"].isin(filter_stage)]
        
    display_leads["inquiry_date"] = display_leads["inquiry_date"].dt.strftime("%Y-%m-%d %H:%M")
    display_leads["response_time_hrs"] = display_leads["response_time_hrs"].apply(lambda x: f"{x:.1f} saat")
    display_leads["revenue"] = display_leads["revenue"].apply(lambda x: f"€{x:,.0f}" if x > 0 else "-")
    
    cols = ["lead_id"]
    rename_dict = {
        "lead_id": "Kayıt No",
        "inquiry_date": "Başvuru / Randevu Tarihi",
        "country": "Ülke",
        "language": "Dil",
        "channel": "Kanal",
        "coordinator": "Koordinatör",
        "response_time_hrs": "Yanıt Süresi",
        "clinical_segment": "Klinik Segment",
        "stage": "Aşama",
        "drop_reason": "Kayıp / Erteleme Nedeni",
        "revenue": "Ciro (€)"
    }
    if "masked_patient_name" in display_leads.columns:
        display_leads["masked_name_col"] = display_leads["masked_patient_name"].fillna("Aday Çift (Online Form)")
        cols.append("masked_name_col")
        rename_dict["masked_name_col"] = "Hasta / Çift (KVKK m.6)"

    cols.extend([
        "inquiry_date", "country", "language", "channel",
        "coordinator", "response_time_hrs", "clinical_segment", "stage", "drop_reason", "revenue"
    ])

    st.dataframe(
        display_leads[cols].rename(columns=rename_dict),
        use_container_width=True,
        height=400,
        hide_index=True
    )
    st.markdown("</div>", unsafe_allow_html=True)
