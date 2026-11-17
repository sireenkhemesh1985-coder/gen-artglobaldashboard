"""
Reusable modern UI components for GEN-ART Global Patient Intelligence
Dark Navy (#070D1E) and Turquoise (#00F0FF) aesthetic with crisp typography and subtle glows.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from config import THEME_COLORS

def inject_custom_css():
    """Injects high-end dark navy & neon turquoise custom styles into Streamlit"""
    css = f"""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* Main background */
    .stApp {{
        background: radial-gradient(circle at 15% 10%, #0c1836 0%, #070D1E 65%, #040813 100%);
        color: {THEME_COLORS["text_primary"]};
    }}

    /* Header & Navbar */
    .header-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 24px;
        background: rgba(14, 26, 56, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 14px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }}

    .brand-title {{
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .brand-title span.glow {{
        color: {THEME_COLORS["turquoise"]};
        text-shadow: 0 0 15px rgba(0, 240, 255, 0.5);
    }}

    .badge-auth {{
        background: rgba(0, 240, 255, 0.1);
        border: 1px solid {THEME_COLORS["turquoise"]};
        color: {THEME_COLORS["turquoise"]};
        font-size: 11px;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }}

    /* KPI Cards */
    .kpi-card {{
        background: linear-gradient(135deg, rgba(19, 35, 71, 0.8) 0%, rgba(14, 26, 56, 0.6) 100%);
        border: 1px solid rgba(30, 58, 110, 0.8);
        border-radius: 12px;
        padding: 16px 18px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }}

    .kpi-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(0, 240, 255, 0.4);
        box-shadow: 0 8px 24px rgba(0, 240, 255, 0.12);
    }}

    .kpi-title {{
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: {THEME_COLORS["text_secondary"]};
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }}

    .kpi-value {{
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }}

    .kpi-subtext {{
        font-size: 11px;
        color: {THEME_COLORS["text_muted"]};
        display: flex;
        align-items: center;
        gap: 4px;
    }}

    .kpi-subtext span.positive {{
        color: {THEME_COLORS["success"]};
        font-weight: 600;
    }}

    .kpi-subtext span.highlight {{
        color: {THEME_COLORS["turquoise"]};
        font-weight: 600;
    }}

    /* Section Cards */
    .section-card {{
        background: rgba(14, 26, 56, 0.65);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(30, 58, 110, 0.6);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    }}

    .section-header {{
        font-size: 16px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid rgba(30, 58, 110, 0.4);
        padding-bottom: 10px;
    }}

    .section-header span.tag {{
        font-size: 10px;
        background: rgba(0, 240, 255, 0.15);
        color: {THEME_COLORS["turquoise"]};
        padding: 2px 8px;
        border-radius: 6px;
        font-weight: 600;
    }}

    /* Data verification badge */
    .audit-stamp {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 10px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 6px;
        color: #10B981;
        font-size: 11px;
        font-weight: 600;
    }}

    /* Streamlit components tweaks */
    div[data-testid="stMetricValue"] {{
        color: #00F0FF !important;
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: rgba(14, 26, 56, 0.8);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(30, 58, 110, 0.5);
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        color: {THEME_COLORS["text_secondary"]};
        font-weight: 600;
        padding: 8px 16px;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: rgba(0, 240, 255, 0.15) !important;
        color: {THEME_COLORS["turquoise"]} !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
    }}
    
    /* Table styles */
    .dataframe {{
        background-color: transparent !important;
        color: #E2E8F0 !important;
        font-size: 13px !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_top_navbar(date_label="2026 YTD"):
    """Renders the executive top header with brand and verification indicators"""
    st.markdown(f"""
    <div class="header-bar">
        <div>
            <div class="brand-title">
                🧬 <span>GEN-ART</span> <span class="glow">| Global Patient Intelligence</span>
            </div>
            <div style="font-size: 12px; color: #94A3B8; margin-top: 4px;">
                AI-Powered International Patient Acquisition, Market Intelligence & Conversion Management
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <div class="badge-auth">
                🛡️ Sağlık Turizmi Yetki Belgesi: ST-0625
            </div>
            <div class="audit-stamp">
                ✓ Doğrulanmış Veri · {date_label}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_card(title, value, subtext, icon="📊", is_highlight=False):
    """Renders a single KPI card with the specified metrics"""
    border_color = "rgba(0, 240, 255, 0.4)" if is_highlight else "rgba(30, 58, 110, 0.8)"
    bg_glow = "radial-gradient(circle at top right, rgba(0, 240, 255, 0.12), transparent 70%)" if is_highlight else "none"
    
    html = f"""
    <div class="kpi-card" style="border-color: {border_color}; background-image: {bg_glow};">
        <div class="kpi-title">
            <span>{title}</span>
            <span style="font-size: 16px;">{icon}</span>
        </div>
        <div class="kpi-value" style="color: {'#00F0FF' if is_highlight else '#FFFFFF'};">
            {value}
        </div>
        <div class="kpi-subtext">
            {subtext}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def build_funnel_figure(funnel_data):
    """Builds a high-contrast dark navy & turquoise Plotly funnel chart"""
    stages = [item["stage"] for item in funnel_data]
    values = [item["value"] for item in funnel_data]
    percentages = [f"{item['rate']:.1f}%" for item in funnel_data]
    
    fig = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textinfo="value+percent previous",
        textposition="inside",
        textfont=dict(family="Plus Jakarta Sans", size=13, color="#FFFFFF"),
        marker=dict(
            color=["#00B4D8", "#0096C7", "#0077B6", "#023E8A", "#10B981"],
            line=dict(width=1, color="rgba(0, 240, 255, 0.5)")
        ),
        connector=dict(line=dict(color="rgba(0, 240, 255, 0.3)", width=1, dash="dot"))
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=10, b=10),
        height=320,
        font=dict(family="Plus Jakarta Sans", color="#CBD5E1")
    )
    return fig
