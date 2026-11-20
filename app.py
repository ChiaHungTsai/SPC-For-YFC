import os
import re
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import date, timedelta

# 1. 網頁基本設定 (寬螢幕、隱藏側邊欄)
st.set_page_config(page_title="義芳化學品保科 - SPC 統計製程管制儀表板", layout="wide", initial_sidebar_state="collapsed")

# 2. 自訂 CSS
st.markdown("""
    <style>
    [data-testid="stSidebar"] {display: none;}
    .main { background-color: #f8fafc; color: #1e293b; }
    .block-container {
        max-width: 100% !important;
        padding-top: 3.5rem !important;
        padding-bottom: 1.5rem !important;
        padding-right: 20px !important;
        padding-left: 20px !important;
    }
    .main-header-container {
        background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
        padding: 14px 20px;
        border-radius: 8px;
        color: #ffffff;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .main-header-title {
        font-size: 20px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #ffffff;
        margin: 0;
        line-height: 1.3;
    }
    .main-header-subtitle {
        font-size: 11px;
        color: #93c5fd;
        margin-top: 3px;
        letter-spacing: 0.5px;
        line-height: 1.2;
    }
    div[data-baseweb="popover"] {
        width: max-content !important;
        min-width: 280px !important;
    }
    div[data-baseweb="popover"] div[role="listbox"] {
        max-height: 350px !important;
        overflow-y: auto !important;
    }
    div[data-baseweb="popover"] div[role="listbox"] div {
        white-space: normal !important;
        word-break: break-all !important;
        height: auto !important;
    }
    .custom-alert-table {
        width: 100%;
        border-collapse: collapse;
        background-color: #ffffff;
        font-size: 14px;
        color: #1e293b;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border-radius: 6px;
        overflow: hidden;
        margin-bottom: 12px;
        table-layout: fixed;
    }
    .custom-alert-table th, .custom-alert-table td {
        text-align: center !important;
        padding: 10px 8px;
        border-bottom: 1px solid #e2e8f0;
        white-space: nowrap !important;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .custom-alert-table th {
        background-color: #f1f5f9;
        color: #334155;
        font-weight: 700;
        border-bottom: 2px solid #cbd5e1;
    }
    .custom-alert-table tr:hover { background-color: #f8fafc; }
    .row-label {
        font-size: 16px;
        font-weight: 700;
        color: #1e3a8a;
        display: flex;
        align-items: center;
        justify-content: flex-start;
        height: 36px;
        padding-left: 2px;
        white-space: nowrap;
    }
    .row-label-right {
        font-size: 16px;
        font-weight: 700;
        color: #1e3a8a;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        height: 36px;
        padding-right: 8px;
        white-space: nowrap;
    }
    .inline-sub-label {
        font-size: 14px;
        font-weight: 600;
        color: #000000;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        height: 36px;
        padding-right: 8px;
        white-space: nowrap;
    }
    .stButton > button {
        width: 100% !important;
        height: 36px !important;
        padding: 2px 6px !important;
        font-size: 13px !important;
        min-height: 36px !important;
        max-height: 36px !important;
        white-space: nowrap !important;
    }
    div[data-testid="column"] .stButton > button {
        width: 70pt !important;
        min-width: 70pt !important;
        max-width: 70pt !important;
    }
    .refresh-btn-fixed { margin-top: 4px; }
    .refresh-btn-fixed button {
        width: 120px !important;
        max-width: 120px !important;
        height: 52px !important;
        min-height: 52px !important;
        max-height: 52px !important;
        padding: 2px 6px !important;
        font-size: 13px !important;
        white-space: nowrap !important;
    }
    .stButton > button:disabled {
        background: repeating-linear-gradient(45deg, #cbd5e1, #cbd5e1 6px, #94a3b8 6px, #94a3b8 12px) !important;
        color: #334155 !important;
        border: 2px solid #475569 !important;
        cursor: not-allowed !important;
        opacity: 0.95 !important;
        font-weight: 700 !important;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #dbeafe !important;
        color: #1e40af !important;
        border: 1.5px solid #3b82f6 !important;
        font-weight: 700 !important;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #bfdbfe !important;
        border-color: #2563eb !important;
        color: #1e3a8a !important;
    }
    div[data-baseweb="select"] > div {
        min-height: 36px !important;
        height: auto !important;
    }
    div[data-baseweb="input"] > div {
        min-height: 36px !important;
        height: 36px !important;
    }
    .stDateInput input {
        height: 36px !important;
        padding: 0px 8px !important;
        font-size: 13px !important;
        width: 100% !important;
    }
    .row-spacer { height: 4px; }
    .highlight-title-box {
        display: inline-block;
        width: fit-content;
        background-color: #fef08a;
        border: 1px solid #fde047;
        border-radius: 6px;
        padding: 6px 14px;
        font-size: 16px;
        font-weight: 700;
        color: #713f12;
        margin-bottom: 4px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .missing-spec-hint {
        font-size: 13px;
        color: #475569;
        margin: 0px 0px 6px 2px;
        line-height: 1.4;
    }
    .limit-conflict-alert {
        background-color: #fff1f2;
        border-left: 4px solid #e11d48;
        border-top: 1px solid #fecdd3;
        border-right: 1px solid #fecdd3;
        border-bottom: 1px solid #fecdd3;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 13.5px;
        color: #881337;
        margin: 2px 0px 8px 0px;
        line-height: 1.5;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Google 試算表遠端 CSV 讀取設定（含斷線備援機制）
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgSWa6LTNxRQYImmAZkHX2JbsNkuROSpb_4Q3u6VJ05k72wsTjQ3eq8TMRtn3JpMEg59jlqYqoTk0_/pub?gid=729038536&single=true&output=csv"

@st.cache_data(ttl=60)
def fetch_raw_csv(url):
    return pd.read_csv(url, dtype=str)

def load_and_preprocess_data(url):
    try:
        temp_df = fetch_raw_csv(url).copy()
        st.session_state["backup_df"] = temp_df.copy()
    except Exception as e:
        if "backup_df" in st.session_state and isinstance(st.session_state["backup_df"], pd.DataFrame) and len(st.session_state["backup_df"]) > 0:
            st.toast(f"⚠️ 遠端試算表連線瞬斷，暫時沿用先前快取資料：{e}", icon="⚠️")
            temp_df = st.session_state["backup_df"].copy()
        else:
            st.error(f"讀取 Google 試算表失敗，請檢查網路連線或共用權限設定。錯誤訊息: {e}")
            st.stop()
        
    temp_df.columns = [c.strip() for c in temp_df.columns]
    
    prod_col = None
    for candidate in ["樣品名稱", "成品名稱", "產品名稱"]:
        if candidate in temp_df.columns:
            prod_col = candidate
            break
            
    if prod_col and prod_col != "樣品名稱":
        temp_df = temp_df.rename(columns={prod_col: "樣品名稱"})
        
    for col in ["單位", "階段", "樣品名稱", "分析項目", "取樣點/規格", "小數位數", "USL", "LSL", "UCL", "LCL", "檢驗日期"]:
        if col in temp_df.columns:
            temp_df[col] = temp_df[col].astype(str).str.strip()
            temp_df.loc[temp_df[col].isin(["nan", "NaN", "None", "NAT", "nat", ""]), col] = np.nan
            
    if "測定值" in temp_df.columns:
        temp_df["測定值_str"] = temp_df["測定值"].astype(str).str.strip()
        temp_df["測定值"] = pd.to_numeric(temp_df["測定值"], errors='coerce')
        
    for limit_col in ["USL", "LSL", "UCL", "LCL"]:
        if limit_col in temp_df.columns:
            temp_df[limit_col] = pd.to_numeric(temp_df[limit_col], errors='coerce')
            
    if "檢驗日期" in temp_df.columns:
        raw_date_str = temp_df["檢驗日期"].astype(str).str.strip()
        is_pure_year = raw_date_str.str.match(r"^(19|20)\d{2}$", na=False)
        parsed_dt = pd.to_datetime(raw_date_str.where(~is_pure_year, np.nan), format='mixed', errors='coerce')
        temp_df["_dt"] = parsed_dt

        def extract_year_val(row):
            s_val = str(row["檢驗日期"]).strip() if pd.notna(row["檢驗日期"]) else ""
            m4 = re.search(r"\b((?:19|20)\d{2})\b", s_val)
            if m4:
                return m4.group(1)
            if pd.notna(row["_dt"]):
                return str(row["_dt"].year)
            return np.nan

        temp_df["_year"] = temp_df.apply(extract_year_val, axis=1)
    else:
        temp_df["_dt"] = pd.NaT
        temp_df["_year"] = np.nan
            
    return temp_df

df = load_and_preprocess_data(GOOGLE_SHEET_CSV_URL)

# ==================== 原始標準批號排序函數 ====================
def batch_sort_key(s):
    s_str = str(s).strip()
    i = len(s_str) - 1
    while i >= 0 and not s_str[i].isdigit():
        i -= 1
    digits_collected = []
    while i >= 0 and len(digits_collected) < 3 and s_str[i].isdigit():
        digits_collected.append(s_str[i])
        i -= 1
    if len(digits_collected) > 0:
        digits_collected.reverse()
        num_str = "".join(digits_collected)
        try:
            return (0, int(num_str), s_str)
        except ValueError:
            pass
    digits = re.findall(r'\d+', s_str)
    if digits:
        try:
            return (0, int(digits[-1]), s_str)
        except ValueError:
            pass
    return (1, 0, s_str)

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]

# ==================== 狀態回呼與瞬間聯動邏輯 ====================
def on_unit_change():
    st.session_state.pop("selected_stage", None)
    st.session_state.pop("current_product", None)
    st.session_state["current_spec"] = "__AUTO_SELECT__"
    st.session_state.pop("current_param", None)
    st.session_state["current_years"] = "__AUTO_SELECT_YEARS__"

def on_stage_change():
    st.session_state.pop("current_product", None)
    st.session_state["current_spec"] = "__AUTO_SELECT__"
    st.session_state.pop("current_param", None)
    st.session_state["current_years"] = "__AUTO_SELECT_YEARS__"

def on_product_change():
    st.session_state["current_spec"] = "__AUTO_SELECT__"
    st.session_state.pop("current_param", None)
    st.session_state["current_years"] = "__AUTO_SELECT_YEARS__"

def on_spec_change():
    pass

# ==================== 頂部主標題與「更新資料」按鈕同行配置 ====================
header_cols = st.columns([6.5, 0.9])
with header_cols[0]:
    st.markdown("""
        <div class="main-header-container">
            <div class="main-header-title">義芳化學 ｜ 品保科分析數據儀表板</div>
            <div class="main-header-subtitle">YEE FONG CHEMICAL & INDUSTRIAL CO., LTD.</div>
        </div>
    """, unsafe_allow_html=True)

with header_cols[1]:
    st.markdown('<div class="refresh-btn-fixed">', unsafe_allow_html=True)
    if st.button("🔄 更新資料", use_container_width=False):
        fetch_raw_csv.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# ==================== 網格比例設定 ====================
master_grid_weights = [0.95, 3.0, 1.4, 3.6, 2.4, 1.4]
button_row_weights = [0.7, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 2.0]

# ==================== 1. 製造單位按鈕群組 ====================
fixed_units_list = ["電解課", "矽碳課-矽膠", "矽碳課-碳酸鉀", "凡立水課", "精密化學課", "雙氧水課", "公用課"]
available_units = df["單位"].dropna().unique().tolist() if len(df) > 0 and "單位" in df.columns else []

if "selected_unit" not in st.session_state or st.session_state["selected_unit"] not in fixed_units_list:
    if "電解課" in available_units:
        st.session_state["selected_unit"] = "電解課"
    else:
        st.session_state["selected_unit"] = next((u for u in fixed_units_list if u in available_units), fixed_units_list[0])

selected_unit = st.session_state["selected_unit"]
unit_df = df[df["單位"] == selected_unit] if len(df) > 0 and "單位" in df.columns else pd.DataFrame()

cols_unit = st.columns(button_row_weights)
with cols_unit[0]:
    st.markdown('<div class="row-label">製造單位</div>', unsafe_allow_html=True)

for i, unit in enumerate(fixed_units_list):
    with cols_unit[i + 1]:
        has_data = unit in available_units
        is_active = (selected_unit == unit)
        if has_data:
            if st.button(unit, key=f"u_{unit}", use_container_width=True, type="primary" if is_active else "secondary"):
                if st.session_state["selected_unit"] != unit:
                    st.session_state["selected_unit"] = unit
                    on_unit_change()
                    st.rerun()
        else:
            st.button(unit, key=f"u_{unit}", use_container_width=True, disabled=True)

st.markdown('<div class="row-spacer"></div>', unsafe_allow_html=True)

# ==================== 2. 製程階段按鈕群組 ====================
stages_dict = {"原料IQC": "原料", "製程IPQC": "製程", "成品FQC": "成品", "出貨OQC": "出貨"}
stages_list = list(stages_dict.keys())

if "selected_stage" not in st.session_state or st.session_state["selected_stage"] not in stages_list:
    target_stage = None
    for p_stage in ["出貨OQC", "成品FQC", "製程IPQC", "原料IQC"]:
        raw_val = stages_dict[p_stage]
        if "階段" in unit_df.columns and any(unit_df["階段"].str.contains(raw_val, na=False) | (unit_df["階段"] == p_stage)):
            target_stage = p_stage
            break
    st.session_state["selected_stage"] = target_stage if target_stage else stages_list[0]

selected_stage_label = st.session_state["selected_stage"]
selected_stage_raw = stages_dict[selected_stage_label]

if len(unit_df) > 0 and "階段" in unit_df.columns:
    stage_mask = unit_df["階段"].str.contains(selected_stage_raw, na=False) | (unit_df["階段"] == selected_stage_label)
    stage_df = unit_df[stage_mask]
else:
    stage_df = unit_df

cols_stage = st.columns(button_row_weights)
with cols_stage[0]:
    st.markdown('<div class="row-label">製程階段</div>', unsafe_allow_html=True)

for i, (stage_label, raw_name) in enumerate(stages_dict.items()):
    has_stage_data = any(unit_df["階段"].str.contains(raw_name, na=False)) if len(unit_df) > 0 and "階段" in unit_df.columns else False
    with cols_stage[i + 1
