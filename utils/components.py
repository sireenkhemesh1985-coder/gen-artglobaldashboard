"""
Reusable modern UI components for GEN-ART Global Patient Intelligence
Color Identity: Official Gen-Art Logo Palette (Teal #15736D, Cyan #18AEBB, Orange #F5821F)
Styling: Glassmorphism & Neon Glow Buttons, 100% Full-Width Responsive Layout
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
    """Injects Gen-Art logo-aligned colors, glassmorphic surfaces, and neon glowing buttons"""
    css = f"""
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    /* FIT THE PAGE - 100% Full Width Edge-to-Edge Container */
    .main .block-container,
    [data-testid="stAppViewBlockContainer"],
    [data-testid="stMainBlockContainer"],
    div.block-container {{
        max-width: 100% !important;
        width: 100% !important;
        padding-top: 1.2rem !important;
        padding-right: 2rem !important;
        padding-left: 2rem !important;
        padding-bottom: 2.5rem !important;
    }}

    [data-testid="stAppViewContainer"] > .main {{
        max-width: 100% !important;
        width: 100% !important;
    }}

    /* Main background - Gen-Art Deep Teal Night */
    .stApp {{
        background: radial-gradient(circle at 18% 12%, #0e333d 0%, #05161c 65%, #020a0e 100%) !important;
        color: #F8FAFC;
    }}

    /* Sidebar Background - Cohesive Deep Petrol */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #071f27 0%, #04141a 100%) !important;
        border-right: 1px solid rgba(24, 174, 187, 0.25) !important;
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4) !important;
    }}

    /* Header & Navbar - Glass Bar with Dual Neon Accents (Cyan & Orange) */
    .header-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
        width: 100%;
        padding: 16px 24px;
        background: rgba(9, 34, 43, 0.72) !important;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(24, 174, 187, 0.35);
        border-radius: 14px;
        margin-bottom: 22px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(0, 240, 255, 0.2);
        box-sizing: border-box;
    }}

    .brand-container {{
        display: flex;
        align-items: center;
        gap: 18px;
        min-width: 0;
    }}

    .brand-logo-img {{
        height: 52px;
        width: auto;
        object-fit: contain;
        filter: drop-shadow(0 0 12px rgba(24, 174, 187, 0.45));
    }}

    .brand-title {{
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        white-space: nowrap;
    }}

    .brand-title span.glow {{
        color: #00F0FF;
        text-shadow: 0 0 16px rgba(0, 240, 255, 0.6);
    }}

    .brand-title span.orange-glow {{
        color: #F5821F;
        text-shadow: 0 0 14px rgba(245, 130, 31, 0.6);
    }}

    /* Badges - Glass & Neon */
    .badge-auth {{
        background: rgba(245, 130, 31, 0.12) !important;
        border: 1.5px solid #F5821F !important;
        color: #FFA34D !important;
        font-size: 11px;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        white-space: nowrap;
        box-shadow: 0 0 14px rgba(245, 130, 31, 0.35), inset 0 0 8px rgba(245, 130, 31, 0.15);
    }}

    .audit-stamp {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        background: rgba(24, 174, 187, 0.14) !important;
        border: 1.5px solid #18AEBB !important;
        border-radius: 20px;
        color: #00F0FF !important;
        font-size: 11px;
        font-weight: 700;
        white-space: nowrap;
        box-shadow: 0 0 14px rgba(24, 174, 187, 0.35), inset 0 0 8px rgba(0, 240, 255, 0.15);
    }}

    /* ============================================================== */
    /* GLASS & NEON BUTTONS (Ultra-Modern Glassmorphic Neon Controls) */
    /* ============================================================== */
    .stButton > button,
    .stDownloadButton > button,
    div[data-testid="stDownloadButton"] > button,
    button[kind="primary"],
    button[kind="secondary"] {{
        background: linear-gradient(135deg, rgba(24, 174, 187, 0.18) 0%, rgba(245, 130, 31, 0.14) 100%) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1.5px solid rgba(0, 240, 255, 0.6) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 13.5px !important;
        letter-spacing: 0.5px !important;
        padding: 10px 22px !important;
        box-shadow: 0 0 16px rgba(0, 240, 255, 0.35), inset 0 0 12px rgba(0, 240, 255, 0.15) !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.7) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    div[data-testid="stDownloadButton"] > button:hover {{
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.28) 0%, rgba(245, 130, 31, 0.22) 100%) !important;
        border-color: #00F0FF !important;
        box-shadow: 0 0 28px rgba(0, 240, 255, 0.75), 0 0 45px rgba(245, 130, 31, 0.35), inset 0 0 18px rgba(0, 240, 255, 0.35) !important;
        transform: translateY(-2px) scale(1.02) !important;
        color: #FFFFFF !important;
        text-shadow: 0 0 14px rgba(0, 240, 255, 1) !important;
    }}

    .stButton > button:active,
    .stDownloadButton > button:active {{
        transform: translateY(0) scale(0.99) !important;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.5) !important;
    }}

    /* ============================================================== */
    /* LUXURY GLASS BUTTONS FOR SIDEBAR MODULE NAVIGATION            */
    /* ============================================================== */
    [data-testid="stSidebar"] div.stButton {{
        margin-bottom: 7px !important;
    }}

    [data-testid="stSidebar"] div.stButton > button {{
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        width: 100% !important;
        padding: 10px 14px !important;
        min-height: 44px !important;
        border-radius: 11px !important;
        font-size: 13px !important;
        letter-spacing: 0.25px !important;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        position: relative !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }}

    [data-testid="stSidebar"] div.stButton > button p {{
        text-align: left !important;
        width: 100% !important;
        margin: 0 !important;
        font-size: 12.5px !important;
        letter-spacing: 0.2px !important;
        line-height: 1.35 !important;
    }}

    /* INACTIVE MODULE GLASS BUTTON (Frosted Dark Teal Glass) */
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"],
    [data-testid="stSidebar"] div.stButton > button[kind="secondary"] {{
        background: linear-gradient(135deg, rgba(14, 47, 59, 0.65) 0%, rgba(7, 24, 31, 0.8) 100%) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(24, 174, 187, 0.3) !important;
        color: #CBD5E1 !important;
        font-weight: 500 !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        text-shadow: none !important;
    }}

    /* HOVER STATE ON INACTIVE MODULE */
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"]:hover,
    [data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover {{
        background: linear-gradient(135deg, rgba(24, 174, 187, 0.28) 0%, rgba(245, 130, 31, 0.18) 100%) !important;
        border-color: rgba(0, 240, 255, 0.85) !important;
        color: #FFFFFF !important;
        transform: translateX(5px) scale(1.01) !important;
        box-shadow: 0 0 22px rgba(0, 240, 255, 0.45), inset 0 0 10px rgba(0, 240, 255, 0.18) !important;
    }}

    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"]:hover p,
    [data-testid="stSidebar"] div.stButton > button[kind="secondary"]:hover p {{
        color: #FFFFFF !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.7) !important;
    }}

    /* ACTIVE MODULE GLASS BUTTON (Glowing Neon Cyan + Orange Left Indicator) */
    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"],
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.24) 0%, rgba(245, 130, 31, 0.22) 100%) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1.5px solid #00F0FF !important;
        border-left: 5px solid #F5821F !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        transform: translateX(3px) !important;
        box-shadow: 0 0 26px rgba(0, 240, 255, 0.55), 0 0 16px rgba(245, 130, 31, 0.35), inset 0 0 14px rgba(0, 240, 255, 0.22) !important;
    }}

    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"] p,
    [data-testid="stSidebar"] div.stButton > button[kind="primary"] p {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 0 0 12px rgba(0, 240, 255, 0.9) !important;
    }}

    [data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"]:hover,
    [data-testid="stSidebar"] div.stButton > button[kind="primary"]:hover {{
        border-color: #00F0FF !important;
        box-shadow: 0 0 32px rgba(0, 240, 255, 0.75), inset 0 0 18px rgba(0, 240, 255, 0.3) !important;
        transform: translateX(4px) !important;
    }}

    /* ============================================================== */
    /* ULTRA-MODERN GLASS NAVIGATION BUTTONS FOR SIDEBAR MODULES     */
    /* ============================================================== */
    [data-testid="stSidebar"] div[data-testid="stRadio"] {{
        margin-bottom: 16px !important;
    }}

    [data-testid="stSidebar"] div[data-testid="stRadio"] > div[role="radiogroup"] {{
        display: flex !important;
        flex-direction: column !important;
        gap: 8px !important;
        width: 100% !important;
    }}

    /* Convert each radio option into a luxury Glass Button */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"],
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label {{
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        padding: 11px 16px !important;
        margin: 0 !important;
        background: linear-gradient(135deg, rgba(14, 47, 59, 0.62) 0%, rgba(7, 24, 31, 0.75) 100%) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        border: 1px solid rgba(24, 174, 187, 0.3) !important;
        border-radius: 11px !important;
        cursor: pointer !important;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
        box-sizing: border-box !important;
    }}

    /* Remove the native HTML radio circle & dot */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child,
    [data-testid="stSidebar"] div[data-testid="stRadio"] input[type="radio"] {{
        display: none !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        position: absolute !important;
    }}

    /* Option Text Inside Glass Button */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label div[data-testid="stMarkdownContainer"] p {{
        font-size: 12.5px !important;
        font-weight: 500 !important;
        color: #CBD5E1 !important;
        letter-spacing: 0.25px !important;
        margin: 0 !important;
        line-height: 1.4 !important;
        transition: all 0.22s ease !important;
    }}

    /* Hover State on Glass Navigation Button */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:hover,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {{
        background: linear-gradient(135deg, rgba(24, 174, 187, 0.28) 0%, rgba(245, 130, 31, 0.18) 100%) !important;
        border-color: rgba(0, 240, 255, 0.8) !important;
        transform: translateX(5px) scale(1.01) !important;
        box-shadow: 0 0 22px rgba(0, 240, 255, 0.45), inset 0 0 12px rgba(0, 240, 255, 0.18) !important;
    }}

    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:hover div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:hover div[data-testid="stMarkdownContainer"] p {{
        color: #FFFFFF !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.7) !important;
    }}

    /* ACTIVE / SELECTED GLASS BUTTON (Glowing Neon Cyan + Orange Left Indicator) */
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked),
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"],
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"][data-checked="true"],
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {{
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.22) 0%, rgba(245, 130, 31, 0.22) 100%) !important;
        border: 1.5px solid #00F0FF !important;
        border-left: 5px solid #F5821F !important;
        box-shadow: 0 0 26px rgba(0, 240, 255, 0.55), 0 0 16px rgba(245, 130, 31, 0.35), inset 0 0 14px rgba(0, 240, 255, 0.22) !important;
        transform: translateX(3px) !important;
    }}

    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] label[data-baseweb="radio"][aria-checked="true"] div[data-testid="stMarkdownContainer"] p,
    [data-testid="stSidebar"] div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) div[data-testid="stMarkdownContainer"] p {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        text-shadow: 0 0 12px rgba(0, 240, 255, 0.9) !important;
    }}

    /* HORIZONTAL GLASS RADIO BUTTONS ACROSS ALL MODULES */
    div[data-testid="stRadio"] > div[role="radiogroup"][aria-orientation="horizontal"] {{
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        background: rgba(9, 34, 43, 0.55) !important;
        padding: 6px 10px !important;
        border-radius: 12px !important;
        border: 1px solid rgba(24, 174, 187, 0.3) !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"][aria-orientation="horizontal"] label[data-baseweb="radio"] {{
        background: rgba(14, 47, 59, 0.6) !important;
        border: 1px solid rgba(24, 174, 187, 0.28) !important;
        border-radius: 8px !important;
        padding: 6px 16px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"][aria-orientation="horizontal"] label[data-baseweb="radio"] > div:first-child {{
        display: none !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"][aria-orientation="horizontal"] label[data-baseweb="radio"]:hover {{
        border-color: #00F0FF !important;
        box-shadow: 0 0 14px rgba(0, 240, 255, 0.35) !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"][aria-orientation="horizontal"] label[data-baseweb="radio"]:has(input:checked) {{
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.22) 0%, rgba(245, 130, 31, 0.2) 100%) !important;
        border-color: #00F0FF !important;
        box-shadow: 0 0 18px rgba(0, 240, 255, 0.5) !important;
    }}

    /* Sidebar Filter Inputs Glass Styling */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background: rgba(14, 47, 59, 0.75) !important;
        border: 1px solid rgba(24, 174, 187, 0.35) !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.25) !important;
        transition: all 0.2s ease !important;
    }}

    [data-testid="stSidebar"] div[data-baseweb="select"] > div:hover,
    [data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {{
        border-color: #00F0FF !important;
        box-shadow: 0 0 16px rgba(0, 240, 255, 0.35) !important;
    }}

    /* GLASS & NEON TABS */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 10px !important;
        background: rgba(9, 34, 43, 0.65) !important;
        backdrop-filter: blur(14px) !important;
        -webkit-backdrop-filter: blur(14px) !important;
        padding: 8px 10px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(24, 174, 187, 0.3) !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 9px !important;
        color: #A5C4CF !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        font-size: 13.5px !important;
        transition: all 0.25s ease !important;
        background: transparent !important;
        border: 1px solid transparent !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, rgba(24, 174, 187, 0.28) 0%, rgba(245, 130, 31, 0.16) 100%) !important;
        color: #00F0FF !important;
        border: 1px solid rgba(0, 240, 255, 0.6) !important;
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.5), inset 0 0 10px rgba(0, 240, 255, 0.2) !important;
        text-shadow: 0 0 8px rgba(0, 240, 255, 0.7) !important;
    }}

    /* KPI Cards - Gen-Art Teal Glass with Neon Accents */
    .kpi-card {{
        background: linear-gradient(135deg, rgba(14, 47, 59, 0.85) 0%, rgba(8, 28, 36, 0.7) 100%) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(24, 174, 187, 0.4) !important;
        border-radius: 12px;
        padding: 14px 16px;
        position: relative;
        overflow: hidden;
        min-width: 0;
        width: 100%;
        box-sizing: border-box;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.08);
    }}

    .kpi-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(0, 240, 255, 0.65) !important;
        box-shadow: 0 6px 24px rgba(0, 240, 255, 0.25), 0 0 35px rgba(245, 130, 31, 0.15) !important;
    }}

    .kpi-title {{
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #A5C4CF;
        margin-bottom: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    .kpi-value {{
        font-size: 24px;
        font-weight: 800;
        color: #FFFFFF;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        line-height: 1.2;
    }}

    .kpi-subtext {{
        font-size: 11px;
        color: #7AA2B1;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        display: block;
    }}

    .kpi-subtext span.positive {{
        color: #10B981;
        font-weight: 600;
    }}

    .kpi-subtext span.highlight {{
        color: #00F0FF;
        font-weight: 700;
    }}

    .kpi-subtext span.orange {{
        color: #F5821F;
        font-weight: 700;
    }}

    /* Section Cards - Glassmorphic Surface */
    .section-card {{
        background: rgba(9, 34, 43, 0.68) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(24, 174, 187, 0.35) !important;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 6px 28px rgba(0, 0, 0, 0.3) !important;
        box-sizing: border-box;
        width: 100%;
    }}

    .section-header {{
        font-size: 16px;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 8px;
        border-bottom: 1px solid rgba(24, 174, 187, 0.3);
        padding-bottom: 10px;
    }}

    .section-header span.tag {{
        font-size: 10.5px;
        background: rgba(0, 240, 255, 0.16);
        border: 1px solid rgba(0, 240, 255, 0.35);
        color: #00F0FF;
        padding: 3px 10px;
        border-radius: 6px;
        font-weight: 600;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }}

    /* Form Controls & Inputs - Glass Style */
    div[data-baseweb="select"] > div {{
        background: rgba(14, 47, 59, 0.75) !important;
        border: 1px solid rgba(24, 174, 187, 0.35) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_top_navbar(date_label="2026 YTD"):
    """Renders the executive top header with official logo, Teal & Orange brand harmony"""
    logo_src = get_base64_logo()
    logo_tag = f'<img src="{logo_src}" class="brand-logo-img" alt="GEN-ART">' if logo_src else '🧬'
    
    st.markdown(f"""
    <div class="header-bar">
        <div class="brand-container">
            {logo_tag}
            <div>
                <div class="brand-title">
                    <span>GEN-ART</span> <span class="glow">| Global Patient</span> <span class="orange-glow">Intelligence</span>
                </div>
                <div style="font-size: 11.5px; color: #A5C4CF; margin-top: 2px;">
                    AI-Powered International Patient Acquisition, Market Intelligence & Conversion Management
                </div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
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
    """Renders a single KPI card with robust non-wrapping typography and auto-scaled font"""
    border_color = "rgba(0, 240, 255, 0.55)" if is_highlight else "rgba(24, 174, 187, 0.35)"
    bg_glow = "radial-gradient(circle at top right, rgba(0, 240, 255, 0.2), transparent 70%)" if is_highlight else "none"
    val_color = '#00F0FF' if is_highlight else '#FFFFFF'
    
    val_str = str(value)
    if len(val_str) > 20:
        f_size = "16px"
    elif len(val_str) > 13:
        f_size = "18.5px"
    else:
        f_size = "23px"
    
    html = f"""
    <div class="kpi-card" style="border-color: {border_color}; background-image: {bg_glow};">
        <div class="kpi-title" title="{title}">
            <span>{title}</span>
            <span style="font-size: 14px;">{icon}</span>
        </div>
        <div class="kpi-value" style="color: {val_color}; font-size: {f_size};" title="{value}">
            {value}
        </div>
        <div class="kpi-subtext" title="{subtext}">
            {subtext}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def build_funnel_figure(funnel_data):
    """Builds a Plotly Express funnel chart oriented naturally with Gen-Art colors"""
    df = pd.DataFrame(funnel_data)
    
    # Official Gen-Art Brand sequence: Cyan #18AEBB, Deep Teal #15736D, Neon Cyan #00F0FF, Amber #F5821F, Emerald #10B981
    genart_palette = ["#18AEBB", "#15736D", "#00F0FF", "#F5821F", "#10B981"]
    
    try:
        fig = px.funnel(
            df,
            x="value",
            y="stage",
            color="stage",
            color_discrete_sequence=genart_palette
        )
        
        # Natural funnel orientation: top starts at step 1, bottom narrows to step 5
        fig.update_yaxes(autorange="reversed")
        
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=340,
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
            color_discrete_sequence=genart_palette
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            height=340,
            showlegend=False
        )
        return fig
