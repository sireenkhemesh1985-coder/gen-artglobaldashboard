"""
Reusable modern UI components for GEN-ART Global Patient Intelligence
Dark Navy (#070D1E) and Turquoise (#00F0FF) aesthetic with crisp typography and responsive sizing.
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import base64
import os
from config import THEME_COLORS

def get_base64_logo():
    """Reads assets/logo.png and returns base64 data URI"""
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
            return f"data:image/png;base64,{encoded}"
        except Exception:
            return None
    return None

def inject_custom_css():
    """Injects high-end dark navy & neon turquoise custom styles into Streamlit"""
    css = f"""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

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
        flex-wrap: wrap;
        gap: 16px;
        padding: 14px 20px;
        background: rgba(14, 26, 56, 0.7);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 14px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }}

    .brand-container {{
        display: flex;
        align-items: center;
        gap: 14px;
        min-width: 0;
    }}

    .brand-logo-img {{
        height: 48px;
        width: auto;
        object-fit: contain;
    }}

    .brand-title {{
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        white-space: nowrap;
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
        padding: 5px 12px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        white-space: nowrap;
    }}

    /* KPI Cards - Responsive & Fitted Size */
    .kpi-card {{
        background: linear-gradient(135deg, rgba(19, 35, 71, 0.85) 0%, rgba(14, 26, 56, 0.65) 100%);
        border: 1px solid rgba(30, 58, 110, 0.8);
        border-radius: 12px;
        padding: 12px 12px;
        position: relative;
        overflow: hidden;
        min-width: 0;
        box-sizing: border-box;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }}

    .kpi-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(0, 240, 255, 0.4);
        box-shadow: 0 6px 20px rgba(0, 240, 255, 0.12);
    }}

    .kpi-title {{
        font-size: 10px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: {THEME_COLORS["text_secondary"]};
        margin-bottom: 4px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .kpi-value {{
        font-size: 19px;
        font-weight: 800;
        color: #FFFFFF;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.2;
    }}

    .kpi-subtext {{
        font-size: 10.5px;
        color: {THEME_COLORS["text_muted"]};
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: block;
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
        padding: 18px;
        margin-bottom: 18px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    }}

    .section-header {{
        font-size: 15px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid rgba(30, 58, 110, 0.4);
        padding-bottom: 8px;
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
        padding: 5px 12px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        color: #10B981;
        font-size: 11px;
        font-weight: 600;
        white-space: nowrap;
    }}

    /* Tabs tweak */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
        background-color: rgba(14, 26, 56, 0.8);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid rgba(30, 58, 110, 0.5);
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        color: {THEME_COLORS["text_secondary"]};
        font-weight: 600;
        padding: 6px 14px;
        font-size: 13px;
    }}

    .stTabs [aria-selected="true"] {{
        background-color: rgba(0, 240, 255, 0.15) !important;
        color: {THEME_COLORS["turquoise"]} !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_top_navbar(date_label="2026 YTD"):
    """Renders the executive top header with official logo and verification indicators"""
    logo_src = get_base64_logo()
    logo_tag = f'<img src="{logo_src}" class="brand-logo-img" alt="GEN-ART">' if logo_src else '🧬'
    
    st.markdown(f"""
    <div class="header-bar">
        <div class="brand-container">
            {logo_tag}
            <div>
                <div class="brand-title">
                    <span>GEN-ART</span> <span class="glow">| Global Patient Intelligence</span>
                </div>
                <div style="font-size: 11px; color: #94A3B8; margin-top: 2px;">
                    AI-Powered International Patient Acquisition, Market Intelligence & Conversion Management
                </div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
            <div class="badge-auth">
                🛡️ Sağlık Turizmi Yetki: ST-0625
            </div>
            <div class="audit-stamp">
                ✓ Doğrulanmış Veri · {date_label}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_card(title, value, subtext, icon="📊", is_highlight=False):
    """Renders a single KPI card with robust non-wrapping typography"""
    border_color = "rgba(0, 240, 255, 0.45)" if is_highlight else "rgba(30, 58, 110, 0.8)"
    bg_glow = "radial-gradient(circle at top right, rgba(0, 240, 255, 0.15), transparent 70%)" if is_highlight else "none"
    val_color = '#00F0FF' if is_highlight else '#FFFFFF'
    
    html = f"""
    <div class="kpi-card" style="border-color: {border_color}; background-image: {bg_glow};">
        <div class="kpi-title" title="{title}">
            <span>{title}</span>
            <span style="font-size: 13px;">{icon}</span>
        </div>
        <div class="kpi-value" style="color: {val_color};" title="{value}">
            {value}
        </div>
        <div class="kpi-subtext" title="{subtext}">
            {subtext}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def build_funnel_figure(funnel_data):
    """Builds a robust Plotly Express funnel chart that runs flawlessly across all versions"""
    df = pd.DataFrame(funnel_data)
    
    try:
        fig = px.funnel(
            df,
            x="value",
            y="stage",
            color="stage",
            color_discrete_sequence=["#00B4D8", "#0096C7", "#0077B6", "#023E8A", "#10B981"]
        )
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            showlegend=False,
            font=dict(family="Plus Jakarta Sans", color="#CBD5E1", size=12)
        )
        return fig
    except Exception:
        # Resilient fallback to horizontal bar chart
        fig = px.bar(
            df,
            x="value",
            y="stage",
            orientation="h",
            color="stage",
            color_discrete_sequence=["#00B4D8", "#0096C7", "#0077B6", "#023E8A", "#10B981"]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            showlegend=False
        )
        return fig
