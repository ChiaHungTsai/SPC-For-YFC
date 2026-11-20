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
    with cols_stage[i + 1]:
        if has_stage_data:
            is_active = (selected_stage_label == stage_label)
            if st.button(stage_label, key=f"s_{stage_label}", use_container_width=True, type="primary" if is_active else "secondary"):
                if st.session_state["selected_stage"] != stage_label:
                    st.session_state["selected_stage"] = stage_label
                    on_stage_change()
                    st.rerun()
        else:
            st.button(stage_label, key=f"s_{stage_label}", use_container_width=True, disabled=True)

st.markdown('<div class="row-spacer"></div>', unsafe_allow_html=True)

is_fanlishui_special = (selected_unit == "凡立水課" and selected_stage_label in ["製程IPQC", "成品FQC"])
is_multi_limit_exempt_unit_stage = (
    (selected_unit == "凡立水課" and selected_stage_label in ["製程IPQC", "成品FQC"]) or
    (selected_unit == "雙氧水課" and selected_stage_label == "成品FQC")
)
product_label_text = "樣品種類" if is_fanlishui_special else "樣品名稱"
spec_label_text = "樣品名稱" if is_fanlishui_special else "取樣點/規格"

# ==================== 3. 樣品名稱與取樣點/規格選單 ====================
products_list = stage_df["樣品名稱"].dropna().unique().tolist() if len(stage_df) > 0 and "樣品名稱" in stage_df.columns else []
products_list = sorted(products_list, key=natural_sort_key)

if "current_product" not in st.session_state or st.session_state["current_product"] not in products_list:
    st.session_state["current_product"] = products_list[0] if products_list else ""

cols_row3 = st.columns(master_grid_weights)
with cols_row3[0]:
    st.markdown(f'<div class="row-label">{product_label_text}</div>', unsafe_allow_html=True)
with cols_row3[1]:
    selected_product = st.selectbox(
        product_label_text, 
        options=products_list if products_list else ["請先選擇製程階段"], 
        key="current_product",
        on_change=on_product_change,
        label_visibility="collapsed"
    )

prod_df = stage_df[(stage_df["樣品名稱"] == selected_product)] if products_list and selected_product != "請先選擇製程階段" else pd.DataFrame()
valid_specs_series = prod_df["取樣點/規格"].dropna() if "取樣點/規格" in prod_df.columns else pd.Series(dtype=str)
raw_specs_list = sorted([str(s).strip() for s in valid_specs_series.unique() if str(s).strip() and str(s).strip().lower() not in ["nan", "none", "nat", ""]], key=natural_sort_key)

if "current_spec" not in st.session_state or st.session_state["current_spec"] == "__AUTO_SELECT__":
    if len(raw_specs_list) == 0:
        st.session_state["current_spec"] = []
    elif is_multi_limit_exempt_unit_stage and len(raw_specs_list) > 1:
        st.session_state["current_spec"] = [raw_specs_list[0]]
    else:
        st.session_state["current_spec"] = raw_specs_list.copy()
elif not isinstance(st.session_state["current_spec"], list):
    st.session_state["current_spec"] = raw_specs_list.copy() if len(raw_specs_list) > 0 else []
else:
    st.session_state["current_spec"] = [s for s in st.session_state["current_spec"] if s in raw_specs_list]

if st.session_state.get("trigger_action") == "select_all":
    st.session_state["current_spec"] = raw_specs_list.copy()
    st.session_state.pop("trigger_action", None)
elif st.session_state.get("trigger_action") == "deselect_all":
    st.session_state["current_spec"] = []
    st.session_state.pop("trigger_action", None)

is_all_selected = len(raw_specs_list) > 0 and set(st.session_state["current_spec"]) == set(raw_specs_list)
is_none_selected = len(st.session_state["current_spec"]) == 0

with cols_row3[2]:
    st.markdown(f'<div class="row-label-right">{spec_label_text}</div>', unsafe_allow_html=True)
with cols_row3[3]:
    if len(raw_specs_list) > 0:
        selected_specs = st.multiselect(
            spec_label_text,
            options=raw_specs_list,
            key="current_spec",
            placeholder="請選擇（可多選）...",
            on_change=on_spec_change,
            label_visibility="collapsed"
        )
        selected_specs = [s for s in raw_specs_list if s in selected_specs]
        spec_df = prod_df[prod_df["取樣點/規格"].astype(str).str.strip().isin(selected_specs)] if len(selected_specs) > 0 else prod_df.iloc[0:0]
    else:
        selected_specs = []
        spec_df = prod_df
        st.multiselect(spec_label_text, options=["無資料"], default=["無資料"], disabled=True, key="sel_spec_disabled", label_visibility="collapsed")

with cols_row3[4]:
    if len(raw_specs_list) > 0:
        b_cols = st.columns(2)
        with b_cols[0]:
            if st.button("全選", key="btn_select_all", use_container_width=True, disabled=is_all_selected):
                st.session_state["trigger_action"] = "select_all"
                st.rerun()
        with b_cols[1]:
            if st.button("全部取消", key="btn_deselect_all", use_container_width=True, disabled=is_none_selected):
                st.session_state["trigger_action"] = "deselect_all"
                st.rerun()

st.markdown('<div class="row-spacer"></div>', unsafe_allow_html=True)

# ==================== 4. 分析項目下拉選單 ====================
cols_param = st.columns(master_grid_weights)
with cols_param[0]:
    st.markdown('<div class="row-label">分析項目</div>', unsafe_allow_html=True)
with cols_param[1]:
    if len(raw_specs_list) == 0 or len(selected_specs) > 0:
        params_list = sorted(spec_df["分析項目"].dropna().unique().tolist(), key=natural_sort_key) if len(spec_df) > 0 and "分析項目" in spec_df.columns else []
        if "current_param" not in st.session_state or st.session_state["current_param"] not in params_list:
            default_p = next((next((p for p in params_list if kw in p.lower()), None) for kw in ["純度", "固含量", "na2o", "nacl", "kcl", "s.s."] if any(kw in p.lower() for p in params_list)), None)
            st.session_state["current_param"] = default_p if default_p else (params_list[0] if params_list else "")

        selected_param = st.selectbox("分析項目", params_list if params_list else ["請先選擇樣品名稱"], key="current_param", label_visibility="collapsed")
        final_df = spec_df[(spec_df["分析項目"] == selected_param)] if len(spec_df) > 0 and params_list else pd.DataFrame()
    else:
        st.selectbox("分析項目", ["請先選擇取樣點/規格"], disabled=True, key="param_disabled", label_visibility="collapsed")
        final_df = pd.DataFrame()
        selected_param = None

st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

# ==================== 5. 檢驗日期區間 / 檢驗年份多選 ====================
today = date.today()
default_start = date(today.year - 1, 1, 1) if today.month <= 6 else date(today.year, 1, 1)
default_end = today

if "date_reset_version" not in st.session_state:
    st.session_state["date_reset_version"] = 0
if "user_start_date" not in st.session_state:
    st.session_state["user_start_date"] = default_start
if "user_end_date" not in st.session_state:
    st.session_state["user_end_date"] = default_end
if st.session_state["user_start_date"] > st.session_state["user_end_date"]:
    st.session_state["user_start_date"] = st.session_state["user_end_date"]

is_forced_batch_mode = (
    (selected_unit == "凡立水課" and selected_stage_label in ["製程IPQC", "成品FQC", "出貨OQC"]) or
    (selected_unit == "雙氧水課" and selected_stage_label == "成品FQC") or
    (selected_unit == "矽碳課-矽膠" and selected_stage_label == "出貨OQC") or
    (selected_unit == "精密化學課" and selected_stage_label == "出貨OQC")
)

available_years = (
    sorted(final_df["_year"].dropna().astype(str).str.strip().unique().tolist(), key=natural_sort_key)
    if len(final_df) > 0 and "_year" in final_df.columns
    else []
)

has_valid_dates = not is_forced_batch_mode and "檢驗日期" in final_df.columns and final_df["_dt"].notna().any()
show_year_selector = is_forced_batch_mode and len(available_years) > 0

if has_valid_dates:
    cols_val5 = st.columns([0.7, 0.25, 1.3, 0.45, 1.3, 0.9, 3.2])
    with cols_val5[0]:
        st.markdown('<div class="row-label">檢驗日期</div>', unsafe_allow_html=True)
    with cols_val5[1]:
        st.markdown('<div class="inline-sub-label">開始</div>', unsafe_allow_html=True)
    with cols_val5[2]:
        start_date = st.date_input("起始日期", value=st.session_state["user_start_date"], key=f"start_date_widget_{st.session_state['date_reset_version']}", label_visibility="collapsed")
        st.session_state["user_start_date"] = start_date
    with cols_val5[3]:
        st.markdown('<div class="inline-sub-label">結束</div>', unsafe_allow_html=True)
    with cols_val5[4]:
        end_date = st.date_input("結束日期", value=st.session_state["user_end_date"], min_value=st.session_state["user_start_date"], max_value=today, key=f"end_date_widget_{st.session_state['date_reset_version']}", label_visibility="collapsed")
        st.session_state["user_end_date"] = end_date
    with cols_val5[5]:
        if st.button("恢復預設", key="btn_reset_dates", use_container_width=True):
            st.session_state["user_start_date"] = default_start
            st.session_state["user_end_date"] = default_end
            st.session_state["date_reset_version"] += 1
            st.rerun()
elif show_year_selector:
    if "current_years" not in st.session_state or st.session_state["current_years"] == "__AUTO_SELECT_YEARS__":
        st.session_state["current_years"] = available_years.copy()
    elif not isinstance(st.session_state["current_years"], list):
        st.session_state["current_years"] = available_years.copy()
    else:
        st.session_state["current_years"] = [y for y in st.session_state["current_years"] if y in available_years]

    cols_val5 = st.columns([0.65, 3.6, 5.85])
    with cols_val5[0]:
        st.markdown('<div class="row-label">檢驗年份</div>', unsafe_allow_html=True)
    with cols_val5[1]:
        selected_years = st.multiselect(
            "檢驗年份",
            options=available_years,
            key="current_years",
            placeholder="請選擇年份（可多選）...",
            label_visibility="collapsed"
        )
        selected_years = [y for y in available_years if y in selected_years]
else:
    selected_years = []

filtered_df = final_df.copy()
if has_valid_dates and len(filtered_df) > 0:
    try:
        date_mask = (filtered_df["_dt"].dt.date >= st.session_state["user_start_date"]) & (filtered_df["_dt"].dt.date <= st.session_state["user_end_date"])
        filtered_df = filtered_df[date_mask | filtered_df["_dt"].isna()]
    except Exception:
        pass
elif show_year_selector and len(filtered_df) > 0:
    if len(selected_years) > 0:
        year_mask = filtered_df["_year"].astype(str).str.strip().isin(selected_years)
        filtered_df = filtered_df[year_mask | filtered_df["_year"].isna()]
    else:
        filtered_df = filtered_df.iloc[0:0]

st.markdown("<hr style='margin: 12px 0; border-color: #cbd5e1;'>", unsafe_allow_html=True)

# ==================== 跨取樣點規格界限 (USL/LSL/UCL/LCL) 一致性檢核函數（全歷史區間 final_df） ====================
def format_locator_hint(rows_df):
    if len(rows_df) == 0:
        return ""
    b_col = next((c for c in ["批號", "批次", "檢驗批號"] if c in rows_df.columns and rows_df[c].dropna().astype(str).str.strip().ne("").any()), None)
    loc_items = []
    for _, r in rows_df.head(3).iterrows():
        b_val = str(r[b_col]).strip() if b_col and pd.notna(r[b_col]) and str(r[b_col]).strip() != "" else ""
        d_val = str(r["檢驗日期"]).strip() if "檢驗日期" in rows_df.columns and pd.notna(r["檢驗日期"]) and str(r["檢驗日期"]).strip() != "" else ""
        if b_val and d_val:
            loc_items.append(f"{d_val}({b_val})")
        elif b_val or d_val:
            loc_items.append(b_val or d_val)
    if not loc_items:
        return ""
    suffix = f"...等共{len(rows_df)}筆" if len(rows_df) > 3 else ""
    return f" [例: {', '.join(loc_items)}{suffix}]"

def check_spec_limits_consistency(df_to_check, unit, stage_label, is_multi_exempt):
    if is_multi_exempt or len(df_to_check) == 0:
        return [], set()
    has_spec_col = "取樣點/規格" in df_to_check.columns and df_to_check["取樣點/規格"].dropna().astype(str).str.strip().ne("").any()
    conflicts = []
    conflicting_cols = set()

    for limit_col, limit_label in [("USL", "規格上限 USL"), ("LSL", "規格下限 LSL"), ("UCL", "管制上限 UCL"), ("LCL", "管制下限 LCL")]:
        if limit_col not in df_to_check.columns:
            continue
        if has_spec_col:
            sub_specs = df_to_check["取樣點/規格"].dropna().astype(str).str.strip().unique()
            spec_val_map = {}
            distinct_signatures = set()
            for sp in sorted(sub_specs, key=natural_sort_key):
                sp_rows = df_to_check[df_to_check["取樣點/規格"].astype(str).str.strip() == sp]
                non_na_vals = sp_rows[limit_col].dropna().unique()
                has_na = sp_rows[limit_col].isna().any()
                if len(non_na_vals) == 0:
                    val_signature = ("EMPTY",)
                    display_v = "未填(空白)"
                elif len(non_na_vals) == 1 and not has_na:
                    val_signature = ("VAL", float(non_na_vals[0]))
                    display_v = f"{float(non_na_vals[0]):g}"
                elif len(non_na_vals) == 1 and has_na:
                    val_signature = ("MIXED_NA", float(non_na_vals[0]))
                    na_rows = sp_rows[sp_rows[limit_col].isna()]
                    display_v = f"{float(non_na_vals[0]):g} (含部分空白列{format_locator_hint(na_rows)})"
                else:
                    val_signature = ("MULTI", tuple(sorted([float(x) for x in non_na_vals])))
                    val_counts = sp_rows[limit_col].dropna().value_counts()
                    minority_val = val_counts.index[-1]
                    min_rows = sp_rows[sp_rows[limit_col] == minority_val]
                    vals_str = " / ".join([f"{float(x):g}" for x in non_na_vals])
                    display_v = f"{vals_str} (同規格內數值不一致，少數值 {float(minority_val):g}{format_locator_hint(min_rows)})"
                spec_val_map[sp] = display_v
                distinct_signatures.add(val_signature)
            if len(distinct_signatures) > 1 or any(sig[0] in ["MIXED_NA", "MULTI"] for sig in distinct_signatures):
                detail_parts = [f"<b>{sp}</b>: {v}" for sp, v in spec_val_map.items()]
                conflicts.append(f"• <b>{limit_label}</b> 設定不一致 ➔ " + " ｜ ".join(detail_parts))
                conflicting_cols.add(limit_col)
        else:
            non_na_vals = df_to_check[limit_col].dropna().unique()
            has_na = df_to_check[limit_col].isna().any()
            if len(non_na_vals) > 1:
                val_counts = df_to_check[limit_col].dropna().value_counts()
                minority_val = val_counts.index[-1]
                min_rows = df_to_check[df_to_check[limit_col] == minority_val]
                vals_str = " / ".join([f"{float(x):g}" for x in non_na_vals])
                conflicts.append(f"• <b>{limit_label}</b> 出現多種不同數值 ➔ {vals_str} (少數值 {float(minority_val):g}{format_locator_hint(min_rows)})")
                conflicting_cols.add(limit_col)
            elif len(non_na_vals) == 1 and has_na:
                na_rows = df_to_check[df_to_check[limit_col].isna()]
                conflicts.append(f"• <b>{limit_label}</b> 部分資料列漏填 ➔ {float(non_na_vals[0]):g} (含部分空白列{format_locator_hint(na_rows)})")
                conflicting_cols.add(limit_col)
    return conflicts, conflicting_cols

# ==================== 數據小數點位數讀取與圖表渲染 ====================
if len(raw_specs_list) > 0 and len(selected_specs) == 0:
    st.warning("尚未選擇項目")
elif show_year_selector and len(selected_years) == 0:
    st.warning("尚未選擇檢驗年份")
elif len(filtered_df) > 0 and "測定值" in filtered_df.columns:
    clean_data = filtered_df.dropna(subset=["測定值"]).copy()
    decimal_places = 2
    has_custom_dec = False
    if "小數位數" in clean_data.columns:
        valid_dec_series = clean_data["小數位數"].dropna()
        if not valid_dec_series.empty:
            try:
                decimal_places = max(0, int(float(valid_dec_series.iloc[0])))
                has_custom_dec = True
            except ValueError:
                pass
    if not has_custom_dec and "測定值_str" in clean_data.columns:
        max_dec = 0
        has_decimal = False
        for val_str in clean_data["測定值_str"].dropna():
            if '.' in val_str:
                has_decimal = True
                dec_clean = "".join([c for c in val_str.split('.')[1] if c.isdigit()])
                max_dec = max(max_dec, len(dec_clean))
        decimal_places = max_dec if has_decimal else 0
    
    fmt_str = f"{{:.{decimal_places}f}}"
    plotly_fmt = f".{decimal_places}f"

    active_batch_col = next((c for c in ["批號", "批次", "檢驗批號"] if c in clean_data.columns and clean_data[c].dropna().astype(str).str.strip().ne("").any()), None)
    use_date_axis = has_valid_dates and not is_forced_batch_mode and clean_data["_dt"].notna().any()

    if use_date_axis:
        clean_data = clean_data.dropna(subset=["_dt"]).sort_values(by="_dt", ascending=True).reset_index(drop=True)
        xaxis_title_text = "日期"
        unique_batches = []
    else:
        if active_batch_col is not None:
            clean_data[active_batch_col] = clean_data[active_batch_col].astype(str).str.strip()
            if "_year" in clean_data.columns and clean_data["_year"].notna().any():
                def batch_with_year_sort_key(row):
                    y_str = str(row["_year"]).strip() if pd.notna(row["_year"]) else ""
                    y_num = int(y_str) if re.fullmatch(r"\d{4}", y_str) else 9999
                    b_key = batch_sort_key(row[active_batch_col])
                    return (y_num, b_key[0], b_key[1], b_key[2])

                clean_data["_sort_tuple"] = clean_data.apply(batch_with_year_sort_key, axis=1)
                clean_data = clean_data.sort_values(by="_sort_tuple").reset_index(drop=True)
                unique_batches = clean_data[active_batch_col].dropna().unique().tolist()
                clean_data = clean_data.drop(columns=["_sort_tuple"])
            else:
                unique_batches = sorted(clean_data[active_batch_col].dropna().unique().tolist(), key=batch_sort_key)
                clean_data[active_batch_col] = pd.Categorical(clean_data[active_batch_col], categories=unique_batches, ordered=True)
                clean_data = clean_data.sort_values(by=active_batch_col).reset_index(drop=True)
            xaxis_title_text = active_batch_col
        else:
            clean_data = clean_data.reset_index(drop=True)
            unique_batches = []
            xaxis_title_text = "序號"
else:
    clean_data = pd.DataFrame()
    decimal_places = 2
    fmt_str = "{:.2f}"
    plotly_fmt = ".2f"
    xaxis_title_text = "日期"
    use_date_axis = False
    active_batch_col = None
    unique_batches = []

if (len(raw_specs_list) == 0 or len(selected_specs) > 0) and len(clean_data) > 0:
    if selected_specs and "取樣點/規格" in clean_data.columns:
        present_specs_set = set(clean_data["取樣點/規格"].dropna().astype(str).str.strip().unique())
        active_specs = [s for s in selected_specs if str(s).strip() in present_specs_set]
        missing_specs = [s for s in selected_specs if str(s).strip() not in present_specs_set]
    else:
