import os
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
    
    /* 主標題設計 */
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
    .custom-alert-table tr:hover {
        background-color: #f8fafc;
    }
    
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
    
    /* 按鈕大小設定：固定寬度 125px 符合「矽碳課-碳酸鉀」 */
    .stButton > button {
        width: 125px !important;
        min-width: 125px !important;
        max-width: 125px !important;
        height: 36px !important;
        padding: 2px 6px !important;
        font-size: 13px !important;
        min-height: 36px !important;
        max-height: 36px !important;
        white-space: nowrap !important;
    }
    
    /* 透過 Flexbox 確保按鈕在同一列橫向排列、絕不換行、保有 12px 相等間距 */
    div.row-button-container {
        display: flex !important;
        flex-direction: row !important;
        gap: 12px !important;
        align-items: center !important;
        height: 36px !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
    }
    
    div.row-button-container > div {
        width: auto !important;
        flex: 0 0 auto !important;
    }
    
    .refresh-btn-fixed {
        margin-top: 4px; 
    }
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
    
    .row-spacer {
        height: 4px;
    }
    
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
        margin-bottom: 6px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    </style>
""", unsafe_allow_html=True)

# 3. Google 試算表遠端 CSV 讀取設定
GOOGLE_SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSgSWa6LTNxRQYImmAZkHX2JbsNkuROSpb_4Q3u6VJ05k72wsTjQ3eq8TMRtn3JpMEg59jlqYqoTk0_/pub?gid=729038536&single=true&output=csv"

@st.cache_data(ttl=60)
def load_and_preprocess_data(url):
    try:
        temp_df = pd.read_csv(url, dtype=str)
    except Exception as e:
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
        
    for col in ["單位", "階段", "樣品名稱", "分析項目", "取樣點/規格", "小數位數", "USL", "LSL", "UCL", "LCL"]:
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
        temp_df["_dt"] = pd.to_datetime(temp_df["檢驗日期"], format='mixed', errors='coerce')
    else:
        temp_df["_dt"] = pd.NaT
            
    return temp_df

df = load_and_preprocess_data(GOOGLE_SHEET_CSV_URL)

required_cols = ["單位", "階段", "樣品名稱", "分析項目", "測定值"]
for rc in required_cols:
    if rc != "階段" and rc not in df.columns:
        pass

# ==================== 批號排序函數 ====================
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
            
    import re
    digits = re.findall(r'\d+', s_str)
    if digits:
        try:
            return (0, int(digits[-1]), s_str)
        except ValueError:
            pass
            
    return (1, 0, s_str)

def natural_sort_key(s):
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', str(s))]

# ==================== 狀態回呼與瞬間聯動邏輯 ====================
def on_unit_change():
    st.session_state.pop("selected_stage", None)
    st.session_state.pop("current_product", None)
    st.session_state.pop("current_spec", None)
    st.session_state.pop("current_param", None)

def on_stage_change():
    st.session_state.pop("current_product", None)
    st.session_state.pop("current_spec", None)
    st.session_state.pop("current_param", None)

def on_product_change():
    st.session_state.pop("current_spec", None)
    st.session_state.pop("current_param", None)

def on_spec_change():
    pass

# ==================== 頂部主標題與「更新資料」按鈕同行配置 ====================
header_cols = st.columns([5.5, 1.2])

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
        st.cache_data.clear()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

# ==================== 統一全域絕對對齊的 7 欄網格框架 (Master Grid) ====================
master_grid_weights = [0.7, 3.0, 0.8, 2.5, 0.9, 0.9, 0.6]

# ==================== 1. 製造單位按鈕群組 ====================
fixed_units_list = [
    "電解課",
    "矽碳課-矽膠",
    "矽碳課-碳酸鉀",
    "凡立水課",
    "精密化學課",
    "雙氧水課",
    "公用課"
]

available_units = df["單位"].dropna().unique().tolist() if len(df) > 0 and "單位" in df.columns else []

if "selected_unit" not in st.session_state or st.session_state["selected_unit"] not in fixed_units_list:
    if "電解課" in available_units:
        st.session_state["selected_unit"] = "電解課"
    else:
        st.session_state["selected_unit"] = next((u for u in fixed_units_list if u in available_units), fixed_units_list[0])

selected_unit = st.session_state["selected_unit"]
unit_df = df[df["單位"] == selected_unit] if len(df) > 0 and "單位" in df.columns else pd.DataFrame()

cols_unit = st.columns(master_grid_weights)
with cols_unit[0]:
    st.markdown('<div class="row-label">製造單位</div>', unsafe_allow_html=True)

with cols_unit[1]:
    st.markdown('<div class="row-button-container">', unsafe_allow_html=True)
    for unit in fixed_units_list:
        has_data = unit in available_units
        is_active = (selected_unit == unit)
        if has_data:
            if st.button(unit, key=f"u_{unit}", type="primary" if is_active else "secondary"):
                if st.session_state["selected_unit"] != unit:
                    st.session_state["selected_unit"] = unit
                    on_unit_change()
                    st.rerun()
        else:
            st.button(unit, key=f"u_{unit}", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="row-spacer"></div>', unsafe_allow_html=True)

# ==================== 2. 製程階段按鈕群組 ====================
stages_dict = {
    "原料IQC": "原料",
    "製程IPQC": "製程",
    "成品FQC": "成品",
    "出貨OQC": "出貨"
}
stages_list = list(stages_dict.keys())

if "selected_stage" not in st.session_state or st.session_state["selected_stage"] not in stages_list:
    target_stage = None
    priority_order = ["出貨OQC", "成品FQC", "製程IPQC", "原料IQC"]
    for p_stage in priority_order:
        raw_val = stages_dict[p_stage]
        if "階段" in unit_df.columns and any(unit_df["階段"].str.contains(raw_val, na=False) | (unit_df["階段"] == p_stage)):
            target_stage = p_stage
            break
    if target_stage is None and stages_list:
        target_stage = stages_list[0]
    st.session_state["selected_stage"] = target_stage

selected_stage_label = st.session_state["selected_stage"]
selected_stage_raw = stages_dict[selected_stage_label]

if len(unit_df) > 0 and "階段" in unit_df.columns:
    stage_mask = unit_df["階段"].str.contains(selected_stage_raw, na=False) | (unit_df["階段"] == selected_stage_label)
    stage_df = unit_df[stage_mask]
else:
    stage_df = unit_df

cols_stage = st.columns(master_grid_weights)
with cols_stage[0]:
    st.markdown('<div class="row-label">製程階段</div>', unsafe_allow_html=True)

with cols_stage[1]:
    st.markdown('<div class="row-button-container">', unsafe_allow_html=True)
    for stage_label, raw_name in stages_dict.items():
        has_stage_data = any(unit_df["階段"].str.contains(raw_name, na=False)) if len(unit_df) > 0 and "階段" in unit_df.columns else False
        if has_stage_data:
            is_active = (selected_stage_label == stage_label)
            if st.button(stage_label, key=f"s_{stage_label}", type="primary" if is_active else "secondary"):
                if st.session_state["selected_stage"] != stage_label:
                    st.session_state["selected_stage"] = stage_label
                    on_stage_change()
                    st.rerun()
        else:
            st.button(stage_label, key=f"s_{stage_label}", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="row-spacer"></div>', unsafe_allow_html=True)

# ==================== 3. 樣品名稱與取樣點/規格選單 ====================
products_list = stage_df["樣品名稱"].dropna().unique().tolist() if len(stage_df) > 0 and "樣品名稱" in stage_df.columns else []
products_list = sorted(products_list, key=natural_sort_key)

if "current_product" not in st.session_state or st.session_state["current_product"] not in products_list:
    st.session_state["current_product"] = products_list[0] if products_list else ""

cols_row3 = st.columns(master_grid_weights)

with cols_row3[0]:
    st.markdown('<div class="row-label">樣品名稱</div>', unsafe_allow_html=True)
with cols_row3[1]:
    selected_product = st.selectbox(
        "樣品名稱", 
        products_list if products_list else ["請先選擇製程階段"], 
        key="current_product",
        on_change=on_product_change,
        label_visibility="collapsed"
    )

prod_df = stage_df[(stage_df["樣品名稱"] == selected_product)] if products_list and selected_product != "請先選擇製程階段" else pd.DataFrame()
valid_specs_series = prod_df["取樣點/規格"].dropna() if "取樣點/規格" in prod_df.columns else pd.Series(dtype=str)
raw_specs_list = [str(s).strip() for s in valid_specs_series.unique() if str(s).strip() and str(s).strip().lower() not in ["nan", "none", "nat", ""]]

raw_specs_list = sorted(raw_specs_list, key=natural_sort_key)

if len(raw_specs_list) > 1:
    if "current_spec" not in st.session_state or not isinstance(st.session_state["current_spec"], list):
        st.session_state["current_spec"] = []
    else:
        st.session_state["current_spec"] = [s for s in st.session_state["current_spec"] if s in raw_specs_list]
elif len(raw_specs_list) == 1:
    if "current_spec" not in st.session_state or not isinstance(st.session_state["current_spec"], list):
        st.session_state["current_spec"] = raw_specs_list.copy()
    else:
        st.session_state["current_spec"] = [s for s in st.session_state["current_spec"] if s in raw_specs_list]

is_all_selected = len(raw_specs_list) > 0 and set(st.session_state.get("current_spec", [])) == set(raw_specs_list)
is_none_selected = len(st.session_state.get("current_spec", [])) == 0

with cols_row3[4]:
    if len(raw_specs_list) > 0:
        if st.button("全選", key="btn_select_all", use_container_width=True, disabled=is_all_selected):
            st.session_state["current_spec"] = raw_specs_list.copy()
            st.rerun()

with cols_row3[5]:
    if len(raw_specs_list) > 0:
        if st.button("全部取消", key="btn_deselect_all", use_container_width=True, disabled=is_none_selected):
            st.session_state["current_spec"] = []
            st.rerun()

with cols_row3[2]:
    st.markdown('<div class="row-label">取樣點/規格</div>', unsafe_allow_html=True)

with cols_row3[3]:
    if len(raw_specs_list) > 0:
        selected_specs = st.multiselect(
            "取樣點/規格",
            options=raw_specs_list,
            key="current_spec",
            on_change=on_spec_change,
            label_visibility="collapsed"
        )
        
        selected_specs = [s for s in raw_specs_list if s in selected_specs]
        
        if len(selected_specs) > 0:
            spec_df = prod_df[prod_df["取樣點/規格"].astype(str).str.strip().isin(selected_specs)]
        else:
            spec_df = prod_df.iloc[0:0]
    else:
        selected_specs = []
        spec_df = prod_df
        st.multiselect(
            "取樣點/規格",
            options=["無取樣點/規格資料"],
            default=["無取樣點/規格資料"],
            disabled=True,
            key="sel_spec_disabled",
            label_visibility="collapsed"
        )

st.markdown('<div class="row-spacer"></div>', unsafe_allow_html=True)

# ==================== 4. 分析項目下拉選單 ====================
cols_param = st.columns(master_grid_weights)
with cols_param[0]:
    st.markdown('<div class="row-label">分析項目</div>', unsafe_allow_html=True)

with cols_param[1]:
    if len(raw_specs_list) == 0 or len(selected_specs) > 0:
        params_list = spec_df["分析項目"].dropna().unique().tolist() if len(spec_df) > 0 and "分析項目" in spec_df.columns else []
        params_list = sorted(params_list, key=natural_sort_key)

        if "current_param" not in st.session_state or st.session_state["current_param"] not in params_list:
            default_p = next((p for p in params_list if "濃度" in p), None)
            if default_p:
                st.session_state["current_param"] = default_p
            else:
                st.session_state["current_param"] = params_list[0] if params_list else ""

        selected_param = st.selectbox(
            "分析項目", 
            params_list if params_list else ["請先選擇樣品名稱"], 
            key="current_param", 
            label_visibility="collapsed"
        )
        final_df = spec_df[(spec_df["分析項目"] == selected_param)] if len(spec_df) > 0 and params_list else pd.DataFrame()
    else:
        st.selectbox(
            "分析項目", 
            ["請先選擇取樣點/規格"], 
            disabled=True, 
            key="param_disabled", 
            label_visibility="collapsed"
        )
        final_df = pd.DataFrame()
        selected_param = None

st.markdown("<div style='height: 4px;'></div>", unsafe_allow_html=True)

# ==================== 5. 檢驗日期區間選擇 ====================
today = date.today()
current_year = today.year

if today.month <= 6:
    default_start = date(current_year - 1, 1, 1)
else:
    default_start = date(current_year, 1, 1)

default_end = today

if "start_date" not in st.session_state:
    st.session_state["start_date"] = default_start
if "end_date" not in st.session_state:
    st.session_state["end_date"] = default_end

if st.session_state["start_date"] > st.session_state["end_date"]:
    st.session_state["start_date"] = st.session_state["end_date"]

is_fanlishui_batch_mode = (selected_unit == "凡立水課" and selected_stage_label in ["製程IPQC", "成品FQC", "出貨OQC"])
has_valid_dates = not is_fanlishui_batch_mode and "檢驗日期" in final_df.columns and final_df["_dt"].notna().any()

if has_valid_dates:
    cols_val5 = st.columns([0.7, 0.35, 1.3, 0.45, 1.3, 4.2])
    with cols_val5[0]:
        st.markdown('<div class="row-label">檢驗日期</div>', unsafe_allow_html=True)
    with cols_val5[1]:
        st.markdown('<div class="inline-sub-label">開始</div>', unsafe_allow_html=True)
    with cols_val5[2]:
        start_date = st.date_input(
            "起始日期", 
            value=st.session_state["start_date"], 
            max_value=st.session_state["end_date"], 
            key="start_date_input", 
            label_visibility="collapsed"
        )
        st.session_state["start_date"] = start_date

    with cols_val5[3]:
        st.markdown('<div class="inline-sub-label">結束</div>', unsafe_allow_html=True)
    with cols_val5[4]:
        end_date = st.date_input(
            "結束日期", 
            value=st.session_state["end_date"], 
            min_value=st.session_state["start_date"], 
            max_value=today, 
            key="end_date_input", 
            label_visibility="collapsed"
        )
        st.session_state["end_date"] = end_date

filtered_df = final_df.copy()
if has_valid_dates and len(filtered_df) > 0:
    try:
        date_mask = (filtered_df["_dt"].dt.date >= start_date) & (filtered_df["_dt"].dt.date <= end_date)
        filtered_df = filtered_df[date_mask | filtered_df["_dt"].isna()]
    except Exception:
        pass

st.markdown("<hr style='margin: 12px 0; border-color: #cbd5e1;'>", unsafe_allow_html=True)

# ==================== 數據小數點位數讀取與圖表渲染 ====================
if len(raw_specs_list) > 0 and len(selected_specs) == 0:
    st.warning("尚未選擇取樣點/規格")
elif len(filtered_df) > 0 and "測定值" in filtered_df.columns:
    clean_data = filtered_df.dropna(subset=["測定值"]).copy()
    
    decimal_places = 2
    has_custom_dec = False
    
    if "小數位數" in clean_data.columns:
        valid_dec_series = clean_data["小數位數"].dropna()
        if not valid_dec_series.empty:
            try:
                dec_val = int(float(valid_dec_series.iloc[0]))
                decimal_places = max(0, dec_val)
                has_custom_dec = True
            except ValueError:
                pass
                
    if not has_custom_dec:
        if "測定值_str" in clean_data.columns:
            max_dec = 0
            has_decimal = False
            for val_str in clean_data["測定值_str"].dropna():
                if '.' in val_str:
                    has_decimal = True
                    dec_part = val_str.split('.')[1]
                    dec_clean = "".join([c for c in dec_part if c.isdigit()])
                    max_dec = max(max_dec, len(dec_clean))
            if has_decimal:
                decimal_places = max_dec
            else:
                decimal_places = 0
    
    fmt_str = f"{{:.{decimal_places}f}}"
    plotly_fmt = f".{decimal_places}f"

    active_batch_col = None
    for candidate in ["批號", "批次", "檢驗批號"]:
        if candidate in clean_data.columns and clean_data[candidate].dropna().astype(str).str.strip().ne("").any():
            active_batch_col = candidate
            break

    use_date_axis = has_valid_dates and not is_fanlishui_batch_mode and clean_data["_dt"].notna().any()

    if use_date_axis:
        clean_data = clean_data.dropna(subset=["_dt"]).copy()
        clean_data = clean_data.sort_values(by="_dt", ascending=True).reset_index(drop=True)
        xaxis_title_text = "日期"
        unique_batches = []
    else:
        if active_batch_col is not None:
            clean_data[active_batch_col] = clean_data[active_batch_col].astype(str).str.strip()
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
    values = clean_data["測定值"]
    mean_val = values.mean()
    std_val = values.std(ddof=1) if len(values) > 1 else 0.0
    n = len(values)

    usl = float(clean_data["USL"].dropna().iloc[0]) if "USL" in clean_data.columns and len(clean_data["USL"].dropna()) > 0 else None
    lsl = float(clean_data["LSL"].dropna().iloc[0]) if "LSL" in clean_data.columns and len(clean_data["LSL"].dropna()) > 0 else None
    ucl = float(clean_data["UCL"].dropna().iloc[0]) if "UCL" in clean_data.columns and len(clean_data["UCL"].dropna()) > 0 else None
    lcl = float(clean_data["LCL"].dropna().iloc[0]) if "LCL" in clean_data.columns and len(clean_data["LCL"].dropna()) > 0 else None

    cpu = (usl - mean_val) / (3 * std_val) if usl is not None and std_val > 0 else 0
    cpl = (mean_val - lsl) / (3 * std_val) if lsl is not None and std_val > 0 else 0
    
    if usl is not None and lsl is not None:
        cpk = min(cpu, cpl)
    elif usl is not None:
        cpk = cpu
    elif lsl is not None:
        cpk = cpl
    else:
        cpk = 0.0

    def check_anomaly(val):
        spec_violate = (usl is not None and val > usl) or (lsl is not None and val < lsl)
        control_violate = (ucl is not None and val > ucl) or (lcl is not None and val < lcl)
        
        if spec_violate:
            return "超出規格範圍"
        elif control_violate:
            return "超出管制範圍"
        return "正常"

    clean_data["異常狀況"] = values.apply(check_anomaly)

    if use_date_axis:
        date_str_range = f"{start_date.strftime('%Y/%m/%d')}-{end_date.strftime('%Y/%m/%d')}"
    else:
        date_str_range = "全批號區間"

    summary_title_html = f"""
    <div class="highlight-title-box">
        {selected_unit} ➔ {selected_stage_label} ➔ <span style='color: #dc2626;'>{selected_product}</span>{spec_display_part if 'spec_display_part' in locals() else ""} ➔ <span style='color: #dc2626;'>{selected_param}</span> ➔ {date_str_range} 統計摘要
    </div>
    """
    st.markdown(summary_title_html, unsafe_allow_html=True)
    st.markdown("<div style='margin: 4px 0;'></div>", unsafe_allow_html=True)
    
    def render_custom_metric(label, value, bg_color, border_color, label_color, unique_key):
        st.markdown(f"""
            <div key="{unique_key}" style="
                background-color: {bg_color};
                border: 1.5px solid {border_color};
                padding: 4px 8px;
                border-radius: 6px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                height: 52px;
                display: flex;
                flex-direction: column;
                justify-content: center;
            ">
                <div style="color: {label_color}; font-size: 10px; font-weight: 600; line-height: 1.2;">{label}</div>
                <div style="color: #000000; font-size: 14px; font-weight: 700; line-height: 1.3;">{value}</div>
            </div>
        """, unsafe_allow_html=True)

    m1, m2, m3, m4, m5, m6, m7, m8 = st.columns(8)
    with m1:
        render_custom_metric("有效樣本數 (n)", f"{n:,}", "#ffffff", "#cbd5e1", "#000000", "m1")
    with m2:
        render_custom_metric("平均值 (Mean)", fmt_str.format(mean_val), "#f0fdf4", "#10b981", "#047857", "m2")
    with m3:
        render_custom_metric("標準差 (Std)", fmt_str.format(std_val) if std_val > 0 else ("0." + "0" * decimal_places), "#ffffff", "#cbd5e1", "#000000", "m3")
    with m4:
        render_custom_metric("製程能力 Cpk", f"{cpk:.3f}" if (usl is not None or lsl is not None) else "N/A", "#ffffff", "#cbd5e1", "#000000", "m4")
    with m5:
        render_custom_metric("管制下限 (LCL)", fmt_str.format(lcl) if lcl is not None else "N/A", "#fff7ed", "#f97316", "#c2410c", "m5")
    with m6:
        render_custom_metric("管制上限 (UCL)", fmt_str.format(ucl) if ucl is not None else "N/A", "#fff7ed", "#f97316", "#c2410c", "m6")
    with m7:
        render_custom_metric("規格下限 (LSL)", fmt_str.format(lsl) if lsl is not None else "N/A", "#fef2f2", "#ef4444", "#b91c1c", "m7")
    with m8:
        render_custom_metric("規格上限 (USL)", fmt_str.format(usl) if usl is not None else "N/A", "#fef2f2", "#ef4444", "#b91c1c", "m8")
    
    st.markdown("<div style='margin: 12px 0;'></div>", unsafe_allow_html=True)

    chart_title_html = f"""
    <div class="highlight-title-box">
        {selected_unit} ➔ {selected_stage_label} ➔ <span style='color: #dc2626;'>{selected_product}</span>{spec_display_part if 'spec_display_part' in locals() else ""} ➔ <span style='color: #dc2626;'>{selected_param}</span> 管制圖
    </div>
    """
    st.markdown(chart_title_html, unsafe_allow_html=True)

    fig = go.Figure()
    
    if len(selected_specs) > 1 and "取樣點/規格" in clean_data.columns:
        color_palette = [
            '#0f172a', '#0d9488', '#d97706', '#db2777', '#7c3aed',
            '#0284c7', '#65a30d', '#9333ea', '#4f46e5', '#ca8a04'
        ]
        
        for idx, sub_spec in enumerate(selected_specs):
            sub_df = clean_data[clean_data["取樣點/規格"].astype(str).str.strip() == str(sub_spec)].copy()
            sub_df = sub_df.dropna(subset=["測定值"])
            if len(sub_df) == 0:
                continue
                
            sub_color = color_palette[idx % len(color_palette)]
            
            if use_date_axis:
                sub_df = sub_df.sort_values(by="_dt", ascending=True)
                plot_x, plot_y, marker_colors_sub, marker_symbols_sub, marker_sizes_sub = [], [], [], [], []
                
                for i in range(len(sub_df)):
                    curr_dt = sub_df["_dt"].iloc[i]
                    curr_val = sub_df["測定值"].iloc[i]
                    if pd.isna(curr_dt):
                        continue
                    
                    if i > 0:
                        prev_dt = sub_df["_dt"].iloc[i - 1]
                        if pd.notna(prev_dt) and (curr_dt - prev_dt).days > 1:
                            plot_x.append(prev_dt + timedelta(days=1))
                            plot_y.append(None)
                            marker_colors_sub.append('#00000000')
                            marker_symbols_sub.append('circle')
                            marker_sizes_sub.append(0)
                    
                    is_spec = (usl is not None and curr_val > usl) or (lsl is not None and curr_val < lsl)
                    is_ctrl = (ucl is not None and curr_val > ucl) or (lcl is not None and curr_val < lcl)
                    
                    if is_spec:
                        m_col, m_sym, m_sz = '#dc2626', 'x', 10
                    elif is_ctrl:
                        m_col, m_sym, m_sz = '#f97316', 'circle', 8
                    else:
                        m_col, m_sym, m_sz = sub_color, 'circle', 6
                        
                    plot_x.append(curr_dt)
                    plot_y.append(curr_val)
                    marker_colors_sub.append(m_col)
                    marker_symbols_sub.append(m_sym)
                    marker_sizes_sub.append(m_sz)
            else:
                if active_batch_col is not None:
                    plot_x = sub_df[active_batch_col].astype(str).tolist()
                else:
                    plot_x = sub_df.index.astype(str).tolist()
                
                plot_y = sub_df["測定值"].tolist()
                marker_colors_sub, marker_symbols_sub, marker_sizes_sub = [], [], []
                for curr_val in plot_y:
                    is_spec = (usl is not None and curr_val > usl) or (lsl is not None and curr_val < lsl)
                    is_ctrl = (ucl is not None and curr_val > ucl) or (lcl is not None and curr_val < lcl)
                    if is_spec:
                        marker_colors_sub.append('#dc2626'); marker_symbols_sub.append('x'); marker_sizes_sub.append(10)
                    elif is_ctrl:
                        marker_colors_sub.append('#f97316'); marker_symbols_sub.append('circle'); marker_sizes_sub.append(8)
                    else:
                        marker_colors_sub.append(sub_color); marker_symbols_sub.append('circle'); marker_sizes_sub.append(6)
            
            fig.add_trace(go.Scatter(
                x=plot_x, y=plot_y,
                mode='lines+markers',
                name=f"{sub_spec}",
                hovertemplate="%{fullSeries.name}: %{y:" + plotly_fmt + "}<extra></extra>",
                line=dict(color=sub_color, width=2.5),
                marker=dict(size=marker_sizes_sub, color=marker_colors_sub, symbol=marker_symbols_sub),
                connectgaps=False
            ))
    else:
        if use_date_axis:
            clean_data = clean_data.sort_values(by="_dt", ascending=True)
            plot_x, plot_y = [], []
            marker_colors_list, marker_symbols_list, marker_sizes_list = [], [], []
            
            for i in range(len(clean_data)):
                curr_dt = clean_data["_dt"].iloc[i]
                curr_val = clean_data["測定值"].iloc[i]
                if pd.isna(curr_dt):
                    continue
                if i > 0:
                    prev_dt = clean_data["_dt"].iloc[i - 1]
                    if pd.notna(prev_dt) and (curr_dt - prev_dt).days > 1:
                        plot_x.append(prev_dt + timedelta(days=1))
                        plot_y.append(None)
                        marker_colors_list.append('#00000000')
                        marker_symbols_list.append('circle')
                        marker_sizes_list.append(0)
                
                is_spec = (usl is not None and curr_val > usl) or (lsl is not None and curr_val < lsl)
                is_ctrl = (ucl is not None and curr_val > ucl) or (lcl is not None and curr_val < lcl)
                
                if is_spec:
                    m_col, m_sym, m_sz = '#dc2626', 'x', 10
                elif is_ctrl:
                    m_col, m_sym, m_sz = '#f97316', 'circle', 8
                else:
                    m_col, m_sym, m_sz = '#2563eb', 'circle', 6
                    
                plot_x.append(curr_dt)
                plot_y.append(curr_val)
                marker_colors_list.append(m_col)
                marker_symbols_list.append(m_sym)
                marker_sizes_list.append(m_sz)
        else:
            if active_batch_col is not None:
                plot_x = clean_data[active_batch_col].astype(str).tolist()
            else:
                plot_x = clean_data.index.astype(str).tolist()
            
            plot_y = clean_data["測定值"].tolist()
            marker_colors_list, marker_symbols_list, marker_sizes_list = [], [], []
            for curr_val in plot_y:
                is_spec = (usl is not None and curr_val > usl) or (lsl is not None and curr_val < lsl)
                is_ctrl = (ucl is not None and curr_val > ucl) or (lcl is not None and curr_val < lcl)
                if is_spec:
                    marker_colors_list.append('#dc2626'); marker_symbols_list.append('x'); marker_sizes_list.append(10)
                elif is_ctrl:
                    marker_colors_list.append('#f97316'); marker_symbols_list.append('circle'); marker_sizes_list.append(8)
                else:
                    marker_colors_list.append('#2563eb'); marker_symbols_list.append('circle'); marker_sizes_list.append(6)

        fig.add_trace(go.Scatter(
            x=plot_x, y=plot_y,
            mode='lines+markers',
            name=selected_param,
            hovertemplate="%{fullSeries.name}: %{y:" + plotly_fmt + "}<extra></extra>",
            line=dict(color='#2563eb', width=2),
            marker=dict(size=marker_sizes_list, color=marker_colors_list, symbol=marker_symbols_list),
            connectgaps=False
        ))
        
        fig.add_hline(
            y=mean_val, line_dash="solid", line_color="#10b981", 
            annotation_text=f"CL: {fmt_str.format(mean_val)}", 
            annotation_font_color="#10b981",
            annotation_position="bottom right"
        )
    
    if ucl is not None:
        fig.add_hline(
            y=ucl, line_dash="dot", line_color="#f97316", 
            annotation_text=f"UCL: {fmt_str.format(ucl)}", 
            annotation_font_color="#f97316",
            annotation_position="top left"
        )
    
    if lcl is not None:
        fig.add_hline(
            y=lcl, line_dash="dot", line_color="#f97316", 
            annotation_text=f"LCL: {fmt_str.format(lcl)}", 
            annotation_font_color="#f97316",
            annotation_position="bottom left"
        )
        
    if usl is not None:
        fig.add_hline(
            y=usl, line_dash="dash", line_color="#ef4444", 
            annotation_text=f"USL: {fmt_str.format(usl)}", 
            annotation_font_color="#ef4444",
            annotation_position="top right"
        )
        
    if lsl is not None:
        fig.add_hline(
            y=lsl, line_dash="dash", line_color="#ef4444", 
            annotation_text=f"LSL: {fmt_str.format(lsl)}", 
            annotation_font_color="#ef4444",
            annotation_position="bottom right"
        )

    fig.update_layout(
        title=dict(text="", font=dict(color="#000000", size=1)),
        xaxis_title=dict(text=xaxis_title_text, font=dict(color="#000000", size=12)),
        yaxis_title=dict(text=selected_param, font=dict(color="#000000", size=12)),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#000000", family="sans-serif"),
        hovermode="x unified",
        hoverlabel=dict(
            align="left",
            namelength=0
        ),
        margin=dict(l=60, r=40, t=50, b=80),
        legend=dict(
            y=0.5,
            yanchor="middle",
            bordercolor="#000000",
            borderwidth=1
        ),
        xaxis=dict(
            type='date' if use_date_axis else 'category',
            categoryorder='array' if not use_date_axis else None,
            categoryarray=unique_batches if not use_date_axis else None,
            tickformat='%Y-%m-%d' if use_date_axis else None,
            tickfont=dict(color="#000000", size=10),
            title_font=dict(color="#000000"),
            tickangle=-45,
            nticks=30,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            spikethickness=1,
            spikecolor="black",
            spikedash="dash"
        ),
        yaxis=dict(
            tickfont=dict(color="#000000"),
            title_font=dict(color="#000000"),
            title=dict(text=selected_param, font=dict(color="#000000", size=12)),
            tickformat=plotly_fmt,
            showline=True,
            linewidth=1,
            linecolor='black',
            mirror=True,
            showspikes=True,
            spikemode="across",
            spikesnap="cursor",
            spikethickness=1,
            spikecolor="black",
            spikedash="dash"
        )
    )
    st.plotly_chart(fig, use_container_width=True, key="spc_main_chart")

    abnormal_df = clean_data[clean_data["異常狀況"] != "正常"].copy()
    
    if len(abnormal_df) > 0:
        spec_count = len(abnormal_df[abnormal_df["異常狀況"] == "超出規格範圍"])
        control_count = len(abnormal_df[abnormal_df["異常狀況"] == "超出管制範圍"])
        
        st.markdown(f'<div class="highlight-title-box" style="background-color: #fee2e2; border-color: #fca5a5; color: #991b1b;">⚠️ 異常警示清單 (共 {len(abnormal_df)} 筆違規點：超出規格範圍 {spec_count} 筆，超出管制範圍 {control_count} 筆)</div>', unsafe_allow_html=True)
        
        col_name_mapping = {
            "異常狀況": "異常狀況",
            active_batch_col: active_batch_col,
            "檢驗日期": "檢驗日期",
            "測定值": "測定值",
            "USL": "規格上限 (USL)",
            "LSL": "規格下限 (LSL)",
            "UCL": "管制上限 (UCL)",
            "LCL": "管制下限 (LCL)"
        }
        
        display_cols = [c for c in ["異常狀況", active_batch_col, "檢驗日期", "測定值", "USL", "LSL", "UCL", "LCL"] if c in abnormal_df.columns or c == "異常狀況"]
        
        table_html = '<table class="custom-alert-table"><thead><tr>'
        for col in display_cols:
            header_label = col_name_mapping.get(col, col)
            table_html += f'<th>{header_label}</th>'
        table_html += '</tr></thead><tbody>'
        
        for _, row in abnormal_df[display_cols].iterrows():
            table_html += '<tr>'
            for col in display_cols:
                val = row[col]
                if pd.isna(val):
                    val_str = ""
                elif col == "異常狀況":
                    if "規格" in str(val):
                        val_str = "❌ 超出規格範圍"
                    else:
                        val_str = "⚠️ 超出管制範圍"
                elif isinstance(val, float):
                    val_str = f"{val:.{decimal_places}f}"
                else:
                    val_str = str(val)
                table_html += f'<td>{val_str}</td>'
            table_html += '</tr>'
        table_html += '</tbody></table>'
        
        st.markdown(table_html, unsafe_allow_html=True)
    else:
        st.success("✅ 目前篩選範圍內的數據皆在管制與規格範圍內，無異常點。")

    with st.expander("點此查看該項目的完整歷史數據明細"):
        st.dataframe(clean_data.drop(columns=["_dt", "_x_val", "測定值_str", "_x_num_idx"], errors="ignore"), use_container_width=True, key="history_data_table")
        
elif len(raw_specs_list) > 0 and len(selected_specs) > 0:
    st.warning("該篩選條件下沒有對應的數據。")
