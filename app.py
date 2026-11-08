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
    
    /* 統一將一二三列按鈕寬度設為 75px，確保高度與對齊一致 */
    .uniform-btn-row .stButton > button,
    div[data-testid="column"] .stButton > button {
        width: 75px !important;
        min-width: 75px !important;
        max-width: 75px !important;
        height: 36px !important;
        min-height: 36px !important;
        max-height: 36px !important;
        padding: 2px 2px !important;
        font-size: 11px !important;
        white-space: nowrap !important;
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
    
    /* 縮小列與列之間的間距 */
    .row-spacer {
        height: 2px !important;
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

# ==================== 統一全域絕對對齊的 7 欄網格框架 (Master Grid & Button Row) ====================
master_grid_weights = [0.7, 3.0, 0.8, 2.5, 0.9, 0.9, 0.6]
button_row_weights = [0.7, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 2.0]

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
