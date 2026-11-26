"""
Module 9: Genetic Tests Catalog & International Oncology/Genetics Market Analysis (B2B Partner Discovery)
Features:
- Integrated Genetic & Cancer Test Catalog (Curated from Mikrogen Lab www.mikrogenlab.com)
- Dynamic Excel File Upload for custom clinic test lists
- Country-level B2B Market Analysis: Institutions, Clinics, Labs, Universities, Oncologists & Geneticists
- Complete contact records: Name, Title, Phone/WhatsApp, Email, LinkedIn Profile, Website, and Market Collaboration Info
- Add New Partner Form & One-Click Excel/CSV Export
- International Biological Sample Logistics Guide (IATA 650 & Cold Chain)
"""

import streamlit as st
import pandas as pd
import io
from data.genetics_data import DEFAULT_GENETIC_TESTS, DEFAULT_B2B_PARTNERS
from utils.components import render_kpi_card

def render_html(html_str):
    """Renders HTML safely by stripping all leading whitespace from each line and removing blank lines to prevent markdown code block formatting"""
    lines = [line.strip() for line in html_str.strip().split("\n") if line.strip()]
    cleaned = "\n".join(lines)
    st.markdown(cleaned, unsafe_allow_html=True)

def init_genetics_session_state():
    """Initializes session state for genetic tests and partner pipeline"""
    if "genetic_tests_db" not in st.session_state:
        st.session_state["genetic_tests_db"] = DEFAULT_GENETIC_TESTS.copy()
    if "b2b_partners_db" not in st.session_state:
        st.session_state["b2b_partners_db"] = DEFAULT_B2B_PARTNERS.copy()

def render_genetics_oncology():
    """Main renderer for Genetic & Oncology Market Analysis Module"""
    init_genetics_session_state()

    render_html("""
    <div style="margin-bottom: 16px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
            <div>
                <h2 style="color: #FFFFFF; font-size: 22px; font-weight: 800; margin: 0; display: flex; align-items: center; gap: 8px;">
                    🧬 Genetik & Kanser Testleri Kataloğu ve B2B Pazar Zekası
                </h2>
                <div style="font-size: 13px; color: #94A3B8; margin-top: 4px;">
                    Mikrogen Lab entegre genetik test panelleri, hedef ülkelerde kurum/klinik/üniversite/doktor pazar analizi ve B2B numune sevkiyat ağı
                </div>
            </div>
            <div style="display: flex; gap: 8px; align-items: center;">
                <span class="badge-auth">Mikrogen Lab Entegre</span>
                <span style="font-size: 11px; background: rgba(0, 240, 255, 0.15); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.35); padding: 5px 12px; border-radius: 20px; font-weight: 700;">
                    B2B Onkoloji İş Birlikleri
                </span>
            </div>
        </div>
    </div>
    """)

    # High-level Metrics Header
    tests_db = st.session_state["genetic_tests_db"]
    partners_db = st.session_state["b2b_partners_db"]

    tot_tests = len(tests_db)
    tot_partners = len(partners_db)
    tot_countries = len(set(p["country"] for p in partners_db))
    active_partners = len([p for p in partners_db if "Aktif" in p.get("status", "") or "Sözleşme" in p.get("status", "")])
    custom_sla = st.session_state.get("custom_sample_sla", None)
    sla_val = custom_sla if custom_sla else "Veri Girilmedi"
    sla_sub = "Kurumsal Teslim SLA Onaylı" if custom_sla else "Numune Teslim Bilgisi Bekleniyor"
    active_sub = "Aktif Sözleşmeli Sevkiyat Ağı" if active_partners > 0 else "Henüz Sözleşme / Veri Girilmedi"

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_kpi_card("Katalogdaki Genetik Panel", f"{tot_tests} Test", "Herediter & Somatik Onkoloji", icon="🔬")
    with k2:
        render_kpi_card("Potansiyel B2B Araştırma Havuzu", f"{tot_partners} Merkez", f"{tot_countries} Odak Ülkede Referans Tarama", icon="🏥", is_highlight=True)
    with k3:
        render_kpi_card("Aktif & Sözleşmeli Partner", f"{active_partners} Kurum", active_sub, icon="🤝")
    with k4:
        render_kpi_card("Numune Teslim & Kargo SLA", sla_val, sla_sub, icon="📦")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    render_html("""
    <div style="background: rgba(14, 47, 59, 0.7); border: 1px solid rgba(245, 130, 31, 0.35); border-radius: 8px; padding: 10px 16px; margin-bottom: 14px; font-size: 12px; color: #CBD5E1; line-height: 1.55;">
        ℹ️ <b>Veri Kaynağı & Durum Bilgisi:</b> GEN-ART'a ait <b>resmi sözleşmeli kurum (`0 Kurum`)</b> ve <b>numune teslimat süreleri (SLA)</b> henüz sisteme girilmediği için aktif anlaşma sayısı <b>0</b> ve numune teslim süresi <b>'Veri Girilmedi'</b> olarak gösterilmektedir. Aşağıdaki 22 kurum kaydı yalnızca hedef ülkelerdeki (Bakü, Erbil, Amman, Taşkent vb.) potansiyel onkoloji hastaneleri ve tıp fakültelerini listeleyen bir <b>B2B İş Geliştirme (Pipeline) Araştırma Rehberidir</b>. Kendi sözleşmeli partnerlerinizi ve kargo SLA bilgilerinizi <i>'3. Yeni Partner / Doktor Ekle &amp; Numune Lojistiği'</i> sekmesinden sisteme işleyebilirsiniz.
    </div>
    """)

    # 3 Main Tabs
    tab_tests, tab_market, tab_new_partner = st.tabs([
        "🔬 1. Genetik & Kanser Test Kataloğu (Mikrogen & Excel Entegre)",
        "🌐 2. Ülke Bazlı Kurum, Lab, Üniversite & Doktor Rehberi (Market Analysis)",
        "➕ 3. Yeni Partner / Doktor Ekle & Numune Lojistiği"
    ])

    # =========================================================================
    # TAB 1: GENETIC & CANCER TEST CATALOG
    # =========================================================================
    with tab_tests:
        render_tests_catalog_tab()

    # =========================================================================
    # TAB 2: B2B MARKET ANALYSIS & PARTNER DIRECTORY
    # =========================================================================
    with tab_market:
        render_market_directory_tab()

    # =========================================================================
    # TAB 3: ADD PARTNER FORM & SAMPLE LOGISTICS
    # =========================================================================
    with tab_new_partner:
        render_add_partner_and_logistics_tab()

def render_tests_catalog_tab():
    """Renders genetic test catalog with Mikrogen Lab data and Excel upload feature"""
    render_html("""
    <div class="section-card">
        <div class="section-header">
            <span>🔬 Genetik ve Kanser Testleri Portföyü</span>
            <span class="tag">Mikrogen Lab & Özel Excel Entegrasyonu</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
            Aşağıdaki testler <b>Mikrogen Genetik Hastalıklar Tanı Merkezi (mikrogenlab.com)</b> altyapısı ve uluslararası onkoloji kılavuzları (NCCN, ESMO) doğrultusunda yapılandırılmıştır. Kendi klinik test listenizi Excel (.xlsx) olarak yükleyerek kataloğu anında güncelleyebilirsiniz.
        </div>
    </div>
    """)

    # Excel File Uploader Component
    with st.expander("📥 Kendi Genetik Test Listenizi Yükleyin (Excel .xlsx Entegrasyonu)", expanded=False):
        render_html("""
        <div style="font-size: 12px; color: #94A3B8; margin-bottom: 8px;">
            Kliniğinize ait genetik ve kanser testleri Excel dosyanızı (.xlsx veya .xls) seçiniz. Dosya yüklendiğinde içerisindeki test adları, genler, yöntem ve materyaller otomatik olarak sisteme aktarılacaktır:
        </div>
        """)
        uploaded_file = st.file_uploader("Excel Dosyası Seçin:", type=["xlsx", "xls"], key="genetic_excel_uploader")

        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_excel(uploaded_file)
                st.success(f"✓ '{uploaded_file.name}' başarıyla yüklendi! Toplam {len(uploaded_df)} satır veri tespit edildi.")
                
                with st.expander("📄 Yüklenen Excel Dosyası Önizlemesi", expanded=True):
                    st.dataframe(uploaded_df, use_container_width=True)
                    
                # Option to incorporate into tests
                if st.button("🔄 Yüklenen Excel Testlerini Sisteme Dahil Et", type="primary"):
                    st.session_state["uploaded_custom_tests_df"] = uploaded_df
                    st.success("Yüklenen testler başarıyla entegre edildi!")
            except Exception as e:
                st.error(f"Excel okunurken bir hata oluştu: {str(e)}")

    # Category and Search Filters
    tests_list = st.session_state["genetic_tests_db"]
    all_categories = ["Tüm Kategoriler"] + sorted(list(set(t["category"] for t in tests_list)))

    f_col1, f_col2 = st.columns([1.2, 2])
    with f_col1:
        sel_cat = st.selectbox("Test Kategorisi Filtrele:", all_categories, index=0)
    with f_col2:
        search_query = st.text_input("Test Adı, Gen (örn. BRCA1, EGFR, 93 Gen) veya Endikasyon Ara:", "")

    # Filtered tests
    filtered_tests = tests_list
    if sel_cat != "Tüm Kategoriler":
        filtered_tests = [t for t in filtered_tests if t["category"] == sel_cat]
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_tests = [
            t for t in filtered_tests 
            if q in t["name"].lower() or q in t["key_genes"].lower() or q in t["indication"].lower() or q in t["method"].lower()
        ]

    render_html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 12px 0 8px 0;">
        <span style="font-size: 13px; font-weight: 700; color: #00F0FF;">
            Listelenen Test Sayısı: {len(filtered_tests)}
        </span>
        <a href="https://www.mikrogenlab.com" target="_blank" style="font-size: 12px; color: #F5821F; text-decoration: none; font-weight: 600;">
            🌐 Mikrogen Lab Resmi Web Sitesini Ziyaret Et ↗
        </a>
    </div>
    """)

    # Display as rich cards or data table
    view_type = st.radio("Görünüm Modu:", ["🗂️ Detaylı Test Kartları", "📊 Karşılaştırmalı Tablo"], horizontal=True)

    if view_type == "🗂️ Detaylı Test Kartları":
        # Render cards in 2-column grid
        col_left, col_right = st.columns(2)
        for idx, t in enumerate(filtered_tests):
            target_col = col_left if idx % 2 == 0 else col_right
            with target_col:
                is_cancer = "Kanser" in t["category"] or "Tümör" in t["category"]
                cat_badge_color = "#F5821F" if is_cancer else "#00F0FF"
                cat_badge_bg = "rgba(245, 130, 31, 0.15)" if is_cancer else "rgba(0, 240, 255, 0.15)"

                render_html(f"""
                <div style="background: rgba(14, 47, 59, 0.7); border: 1px solid rgba(24, 174, 187, 0.35); border-radius: 12px; padding: 16px; margin-bottom: 14px; box-shadow: 0 4px 18px rgba(0,0,0,0.25);">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <span style="font-size: 11px; font-weight: 700; color: {cat_badge_color}; background: {cat_badge_bg}; border: 1px solid {cat_badge_color}; padding: 3px 8px; border-radius: 4px;">
                            {t['category']}
                        </span>
                        <span style="font-size: 13px; font-weight: 800; color: #10B981; background: rgba(16, 185, 129, 0.15); padding: 3px 8px; border-radius: 6px;">
                            B2B: €{t['b2b_price_eur']}
                        </span>
                    </div>
                    <div style="font-size: 16px; font-weight: 700; color: #FFFFFF; margin-bottom: 6px;">
                        {t['name']}
                    </div>
                    <div style="font-size: 12px; color: #94A3B8; margin-bottom: 10px;">
                        🔬 <b>Yöntem:</b> {t['method']} &nbsp;|&nbsp; ⏱️ <b>Süre:</b> {t['turnaround_days']}
                    </div>
                    <div style="background: rgba(9, 34, 43, 0.8); padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #00F0FF; font-size: 11.5px; line-height: 1.5; color: #CBD5E1;">
                        <b>🧬 Öne Çıkan Genler ({t['genes_count']} Gen):</b><br/>
                        <span style="color: #00F0FF;">{t['key_genes']}</span>
                    </div>
                    <div style="font-size: 12px; color: #A5C4CF; line-height: 1.5; margin-bottom: 8px;">
                        <b>🎯 Klinik Endikasyon:</b> {t['indication']}
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #64748B; border-top: 1px solid rgba(24, 174, 187, 0.2); padding-top: 8px; margin-top: 8px;">
                        <span>🧪 <b>Materyal:</b> {t['sample_type']}</span>
                        <span>👨‍⚕️ <b>Hedef:</b> {t['target_specialty']}</span>
                    </div>
                </div>
                """)
    else:
        # Table view
        table_df = pd.DataFrame(filtered_tests)
        st.dataframe(
            table_df[[
                "name", "category", "genes_count", "method", "turnaround_days", 
                "sample_type", "b2b_price_eur", "target_specialty"
            ]].rename(columns={
                "name": "Test Paneli Adı",
                "category": "Kategori",
                "genes_count": "Gen Sayısı",
                "method": "Yöntem",
                "turnaround_days": "Sonuçlanma",
                "sample_type": "Numune Türü",
                "b2b_price_eur": "B2B Fiyat (€)",
                "target_specialty": "Hedef Branş"
            }),
            use_container_width=True,
            hide_index=True
        )

def render_market_directory_tab():
    """Renders verified cross-border partner directory with institutions, doctors, contacts, and outreach data"""
    render_html("""
    <div class="section-card">
        <div class="section-header">
            <span>🌐 Ülke Bazlı Kurum, Klinik, Lab, Üniversite & Doktor Portföyü</span>
            <span class="tag">B2B Partner Pipeline & Kontak Bilgileri</span>
        </div>
        <div style="font-size: 13px; color: #CBD5E1; line-height: 1.6;">
            GEN-ART Ankara akredite genetik laboratuvarı ile çalışmak üzere hedeflenen ve temas kurulan <b>uluslararası onkoloji merkezleri, üniversite tıp fakülteleri, özel klinikler ve hekimler</b>.
        </div>
    </div>
    """)

    render_html("""
    <div style="background: rgba(14, 47, 59, 0.7); border: 1px solid rgba(0, 240, 255, 0.3); border-radius: 8px; padding: 10px 16px; margin-bottom: 14px; font-size: 12px; color: #CBD5E1; line-height: 1.55;">
        🤝 <b>B2B İletişim & Strateji Rehberi:</b> Buradaki kurum ve hekimlerle sözleşme modelleri (Outsource NGS/PGT, Hekimden Hekime Yönlendirme, IATA 650 Numune Lojistiği ve Hazır E-posta/LinkedIn Şablonları) için <b>'4. Dijital Pazarlama & Keşif'</b> altındaki <b>'🏥 B2B: Kurumlar, Hastaneler, Klinikler & Doktorlar Stratejisi'</b> sekmesini inceleyebilirsiniz.
    </div>
    """)

    partners = st.session_state["b2b_partners_db"]

    # Quick summary metrics for countries
    country_counts = pd.Series([p["country"] for p in partners]).value_counts()
    
    # Filter Row
    col_u, col_t, col_s, col_q = st.columns([1.1, 1.2, 1.1, 1.4])
    with col_u:
        country_options = ["Tüm Ülkeler"] + sorted(list(set(p["country"] for p in partners)))
        sel_country = st.selectbox("Hedef Ülke:", country_options, index=0)
    with col_t:
        type_options = ["Tüm Kurum Tipleri"] + sorted(list(set(p["institution_type"] for p in partners)))
        sel_type = st.selectbox("Kurum Tipi:", type_options, index=0)
    with col_s:
        status_options = ["Tüm Durumlar"] + sorted(list(set(p["status"] for p in partners)))
        sel_status = st.selectbox("İş Birliği Durumu:", status_options, index=0)
    with col_q:
        search_kw = st.text_input("Kurum, Doktor veya Uzmanlık Ara:", placeholder="Örn: Charité, Eldar, Meme, Onkolog...")

    # Filter logic
    filtered_partners = partners
    if sel_country != "Tüm Ülkeler":
        filtered_partners = [p for p in filtered_partners if p["country"] == sel_country]
    if sel_type != "Tüm Kurum Tipleri":
        filtered_partners = [p for p in filtered_partners if p["institution_type"] == sel_type]
    if sel_status != "Tüm Durumlar":
        filtered_partners = [p for p in filtered_partners if p["status"] == sel_status]
    if search_kw.strip():
        kw = search_kw.strip().lower()
        filtered_partners = [
            p for p in filtered_partners
            if kw in p["institution_name"].lower() or kw in p["contact_name"].lower() or kw in p["city"].lower() or kw in p["specialty"].lower() or kw in p.get("market_info", "").lower()
        ]

    # Action Toolbar: Count + Download Excel/CSV
    render_html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 10px 0 14px 0;">
        <span style="font-size: 13px; font-weight: 700; color: #00F0FF;">
            🔍 Eşleşen Partner & Hekim Sayısı: {len(filtered_partners)} / {len(partners)}
        </span>
    </div>
    """)

    # Data Display Mode: Cards vs Detailed Table
    partner_view = st.radio("Liste Görünüm Formatı:", ["🏢 B2B İletişim Kartları", "📋 Detaylı Kontak Tablosu (Excel Formatı)"], horizontal=True)

    if partner_view == "🏢 B2B İletişim Kartları":
        for p in filtered_partners:
            # Status badge color
            st_color = "#10B981" if "Aktif" in p['status'] else ("#00F0FF" if "Sözleşme" in p['status'] or "Teklifi" in p['status'] else "#F5821F")
            
            render_html(f"""
            <div style="background: rgba(14, 47, 59, 0.7); border: 1px solid rgba(24, 174, 187, 0.35); border-radius: 12px; padding: 18px; margin-bottom: 14px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 8px; border-bottom: 1px solid rgba(24, 174, 187, 0.25); padding-bottom: 10px; margin-bottom: 12px;">
                    <div>
                        <div style="font-size: 17px; font-weight: 800; color: #FFFFFF;">
                            {p['institution_name']}
                        </div>
                        <div style="font-size: 12px; color: #94A3B8; margin-top: 3px;">
                            📍 <b>{p['city']}, {p['country']}</b> &nbsp;|&nbsp; 🏛️ <i>{p['institution_type']}</i>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 11px; font-weight: 700; color: {st_color}; background: rgba(0,0,0,0.3); border: 1px solid {st_color}; padding: 4px 10px; border-radius: 6px;">
                            {p['status']}
                        </span>
                    </div>
                </div>

                <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 16px; margin-bottom: 12px;">
                    <div style="background: rgba(9, 34, 43, 0.7); padding: 12px; border-radius: 8px; border-left: 3px solid #00F0FF;">
                        <div style="font-size: 13.5px; font-weight: 700; color: #00F0FF; margin-bottom: 4px;">
                            👨‍⚕️ {p['contact_name']}
                        </div>
                        <div style="font-size: 12px; color: #CBD5E1; margin-bottom: 8px;">
                            <b>Unvan:</b> {p['title']} &nbsp;|&nbsp; <b>Branş:</b> {p['specialty']}
                        </div>
                        <div style="font-size: 12px; color: #E2E8F0; line-height: 1.6;">
                            📞 <b>Telefon / WhatsApp:</b> <a href="tel:{p['phone']}" style="color: #10B981; text-decoration: none; font-weight: 600;">{p['phone']}</a><br/>
                            ✉️ <b>E-posta:</b> <a href="mailto:{p['email']}" style="color: #00F0FF; text-decoration: none;">{p['email']}</a><br/>
                            🌐 <b>Web:</b> <a href="{p['website']}" target="_blank" style="color: #F5821F; text-decoration: none;">{p['website']} ↗</a><br/>
                            💼 <b>LinkedIn:</b> <a href="{p['linkedin_url']}" target="_blank" style="color: #38BDF8; text-decoration: none;">Profili İncele ↗</a>
                        </div>
                    </div>

                    <div style="background: rgba(9, 34, 43, 0.7); padding: 12px; border-radius: 8px; border-left: 3px solid #F5821F;">
                        <div style="font-size: 12.5px; font-weight: 700; color: #F5821F; margin-bottom: 6px;">
                            💡 Pazar Durumu & Neden GEN-ART ile Çalışmalı?
                        </div>
                        <div style="font-size: 12px; color: #CBD5E1; line-height: 1.55;">
                            {p['market_info']}
                        </div>
                        <div style="font-size: 11px; color: #94A3B8; margin-top: 8px; border-top: 1px dashed rgba(24, 174, 187, 0.25); padding-top: 6px;">
                            ✈️ <b>Numune Lojistiği:</b> {p['sample_logistics']}
                        </div>
                    </div>
                </div>
            </div>
            """)
    else:
        # Full Data Table with Export capability
        export_df = pd.DataFrame(filtered_partners)
        st.dataframe(
            export_df[[
                "country", "city", "institution_name", "institution_type",
                "contact_name", "title", "phone", "email", "website", "linkedin_url", "status"
            ]].rename(columns={
                "country": "Ülke", "city": "Şehir", "institution_name": "Kurum Adı",
                "institution_type": "Kurum Tipi", "contact_name": "İsim", "title": "Unvan",
                "phone": "Telefon / WhatsApp", "email": "E-posta", "website": "Website",
                "linkedin_url": "LinkedIn", "status": "Pipeline Durumu"
            }),
            use_container_width=True,
            hide_index=True
        )

    # Export Buttons
    c_exp1, c_exp2 = st.columns([1, 4])
    with c_exp1:
        csv_data = pd.DataFrame(filtered_partners).to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 CSV Olarak İndir",
            data=csv_data,
            file_name=f"GENART_Onkoloji_B2B_Rehber_{sel_country}.csv",
            mime="text/csv",
            use_container_width=True
        )

def render_add_partner_and_logistics_tab():
    """Form to add new partner leads and biological sample shipment guidelines"""
    col_form, col_guide = st.columns([1.2, 1])

    with col_form:
        render_html("""
        <div class="section-card">
            <div class="section-header">
                <span>➕ Yeni B2B Kurum / Doktor Kaydı Ekle</span>
                <span class="tag">CRM & İş Geliştirme</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8;">
                Yurtdışı temas kurulan onkolog, genetik laboratuvarı veya üniversite hastanesi yetkilisini sisteme ekleyin:
            </div>
        </div>
        """)

        with st.form("new_b2b_partner_form", clear_on_submit=True):
            f_inst_name = st.text_input("Kurum / Klinik / Lab / Üniversite Adı:*", placeholder="Örn: Baku German Oncology Clinic")
            
            f_c1, f_c2 = st.columns(2)
            with f_c1:
                f_country = st.selectbox("Ülke:*", ["Azerbaijan", "Iraq", "Jordan", "Uzbekistan", "Kazakhstan", "Germany", "United Kingdom", "UAE", "Saudi Arabia", "Georgia", "Serbia", "Bosnia", "Libya", "Egypt", "Diğer"])
            with f_c2:
                f_city = st.text_input("Şehir:*", placeholder="Örn: Bakü, Taşkent, Erbil...")

            f_type = st.selectbox("Kurum Tipi:", [
                "Özel Onkoloji Kliniği", "Kanser Araştırma Enstitüsü", "Genetik Tanı Laboratuvarı",
                "Üniversite Tıp Fakültesi", "Özel Referans Hastanesi", "IVF & Genetik Merkezi"
            ])

            f_c3, f_c4 = st.columns(2)
            with f_c3:
                f_contact_name = st.text_input("İlgili Doktor / Yetkili Adı:*", placeholder="Örn: Prof. Dr. Ahmet Yılmaz")
            with f_c4:
                f_title = st.text_input("Unvanı:*", placeholder="Örn: Tıbbi Onkoloji Şefi")

            f_specialty = st.text_input("Uzmanlık / İlgi Alanı:", placeholder="Örn: Meme Kanseri, Moleküler Genetik, NGS")

            f_c5, f_c6 = st.columns(2)
            with f_c5:
                f_phone = st.text_input("Telefon / WhatsApp:*", placeholder="+994 50 123 4567")
            with f_c6:
                f_email = st.text_input("E-posta Adresi:*", placeholder="doktor@klinik.az")

            f_c7, f_c8 = st.columns(2)
            with f_c7:
                f_linkedin = st.text_input("LinkedIn Profili:", placeholder="https://linkedin.com/in/...")
            with f_c8:
                f_website = st.text_input("Kurumsal Web Sitesi:", placeholder="https://klinik.az")

            f_market_info = st.text_area("Pazar ve İş Birliği Notu (Info):", placeholder="Neden bizimle çalışmalı? Yerel lab kapasitesi, numune gönderme potansiyeli...")
            
            f_status = st.selectbox("Pipeline Başlangıç Aşaması:", [
                "Hedef / İletişime Geçilecek", "İlk Yazışma Yapıldı", "Fiyat Teklifi Gönderildi",
                "Numune Sözleşmesi Aşaması", "Aktif Numune Gönderen Partner"
            ])

            submit_btn = st.form_submit_button("💾 Partner Kaydını Sisteme Ekle", type="primary", use_container_width=True)

            if submit_btn:
                if not f_inst_name.strip() or not f_contact_name.strip() or not f_phone.strip():
                    st.error("Lütfen Kurum Adı, İsim ve Telefon alanlarını doldurunuz.")
                else:
                    new_entry = {
                        "id": f"PARTNER-{len(st.session_state['b2b_partners_db']) + 1:03d}",
                        "country": f_country,
                        "city": f_city,
                        "institution_name": f_inst_name,
                        "institution_type": f_type,
                        "contact_name": f_contact_name,
                        "title": f_title,
                        "specialty": f_specialty,
                        "phone": f_phone,
                        "email": f_email,
                        "linkedin_url": f_linkedin if f_linkedin else "https://linkedin.com",
                        "website": f_website if f_website else "https://google.com",
                        "market_info": f_market_info,
                        "status": f_status,
                        "sample_logistics": f"{f_city} - Ankara ESB / Kargo",
                        "priority": "Yüksek"
                    }
                    st.session_state["b2b_partners_db"].insert(0, new_entry)
                    st.success(f"✓ '{f_inst_name}' ve '{f_contact_name}' başarıyla eklendi!")

    with col_guide:
        render_html("""
        <div class="section-card">
            <div class="section-header">
                <span>📦 Biyolojik Numune Lojistiği & SLA Tanımlama</span>
                <span class="tag">Referans Kılavuz (Henüz Veri Girilmedi)</span>
            </div>
            <div style="font-size: 12.5px; color: #CBD5E1; line-height: 1.65;">
                Kurumunuza ve çalıştığınız medikal kargo/gümrük firmalarına ait <b>kesin numune teslimat süreleri henüz girilmemiştir</b>. Aşağıdaki teknik standartlar yalnızca uluslararası UN 3373 referans bilgisidir:
                <br/><br/>
                <div style="background: rgba(9, 34, 43, 0.75); padding: 10px; border-radius: 8px; margin-bottom: 10px; border-left: 3px solid #00F0FF;">
                    <b>1. UN 3373 Teknik Numune Standartları:</b><br/>
                    • <b>Periferik Kan (Germline / WES / Meme-Kolon NGS):</b> 2x3 ml K2-EDTA tüpü (Soğuk zincir).<br/>
                    • <b>Likit Biyopsi (ctDNA):</b> Streck BCT tüpü.<br/>
                    • <b>Tümör Dokusu (FFPE):</b> Parafin blok veya kesit lam.
                </div>
                <div style="background: rgba(9, 34, 43, 0.75); padding: 10px; border-radius: 8px; border-left: 3px solid #F5821F;">
                    <b>2. Kurumsal Teslim Süresi (SLA) & Gümrük Bilgisi:</b><br/>
                    • Teslimat süreleri ve anlaşmalı hava kargo / medikal kurye protokolünüz aşağıdan tanımlandığında üstteki gösterge kartı otomatik olarak güncellenir.
                </div>
            </div>
        </div>
        """)
        with st.form("sample_sla_form"):
            sla_input = st.text_input("Kesin Numune Teslim SLA Sürenizi Girin:", value=st.session_state.get("custom_sample_sla", ""), placeholder="Örn: 24-48 Saat (DHL Medical Express)")
            if st.form_submit_button("💾 Numune Teslim Süresini Kaydet", use_container_width=True):
                if sla_input.strip():
                    st.session_state["custom_sample_sla"] = sla_input.strip()
                    st.success(f"✓ Numune teslim süresi '{sla_input.strip()}' olarak güncellendi!")
                    st.rerun()
