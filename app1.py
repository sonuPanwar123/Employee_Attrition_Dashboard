import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# ELECTRONICS / TECH THEME (CUSTOM CSS)
# ==========================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

/* ---------- Global App Background ---------- */
.stApp {
    background: radial-gradient(circle at 10% 0%, #0f1b2b 0%, #060c14 45%, #04080d 100%);
    color: #d9f2ff;
    font-family: 'Rajdhani', sans-serif;
}

/* ---------- Circuit grid overlay ---------- */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0, 229, 255, 0.045) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 229, 255, 0.045) 1px, transparent 1px);
    background-size: 34px 34px;
    pointer-events: none;
    z-index: 0;
}

/* ---------- Titles ---------- */
h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #00e5ff !important;
    text-shadow: 0 0 10px rgba(0, 229, 255, 0.55), 0 0 24px rgba(0, 229, 255, 0.25);
    letter-spacing: 1px;
}

h1 {
    border-bottom: 2px solid rgba(0, 229, 255, 0.35);
    padding-bottom: 14px;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a1622 0%, #060d16 100%);
    border-right: 1px solid rgba(0, 229, 255, 0.25);
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #39ff14 !important;
    text-shadow: 0 0 8px rgba(57, 255, 20, 0.5);
}

/* ---------- Metric Cards ---------- */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, rgba(0,229,255,0.08), rgba(0,229,255,0.02));
    border: 1px solid rgba(0, 229, 255, 0.35);
    border-radius: 13px;
    padding: 12px 10px;
    box-shadow: 0 0 18px rgba(0, 229, 255, 0.12), inset 0 0 12px rgba(0,229,255,0.04);
    transition: all 0.25s ease-in-out;
}

div[data-testid="stMetric"]:hover {
    border-color: #39ff14;
    box-shadow: 0 0 22px rgba(57, 255, 20, 0.35);
    transform: translateY(-3px);
}

div[data-testid="stMetricLabel"] {
    color: #7fd9ff !important;
    font-family: 'Rajdhani', sans-serif;
    font-weight: 400;
    letter-spacing: 0.5px;
}

div[data-testid="stMetricValue"] {

    font-family: 'Orbitron', sans-serif !important;

    font-size: 20px !important;

    color: #ffffff !important;

    text-shadow: 0 0 10px rgba(0, 229, 255, 0.6);

}

/* ---------- Buttons ---------- */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(90deg, #00e5ff, #39ff14) !important;
    color: #04141f !important;
    font-family: 'Orbitron', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 0 16px rgba(0, 229, 255, 0.45);
    transition: 0.2s ease-in-out;
}

.stButton > button:hover, .stFormSubmitButton > button:hover {
    box-shadow: 0 0 26px rgba(57, 255, 20, 0.75);
    transform: scale(1.02);
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: rgba(0, 229, 255, 0.04);
    border-radius: 10px;
    padding: 6px;
    border: 1px solid rgba(0,229,255,0.2);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7fd9ff;
    font-family: 'Orbitron', sans-serif;
    font-size: 13px;
    border-radius: 8px;
    padding: 8px 16px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(0,229,255,0.25), rgba(57,255,20,0.15)) !important;
    color: #ffffff !important;
    box-shadow: 0 0 12px rgba(0,229,255,0.4);
}

/* ---------- Dataframe ---------- */
div[data-testid="stDataFrame"] {
    border: 1px solid rgba(0, 229, 255, 0.3);
    border-radius: 10px;
    box-shadow: 0 0 14px rgba(0, 229, 255, 0.08);
}

/* ---------- Divider glow ---------- */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, #00e5ff, transparent);
    box-shadow: 0 0 8px rgba(0,229,255,0.6);
}

/* ---------- Multiselect / inputs ---------- */
div[data-baseweb="select"] > div {
    background-color: rgba(0, 229, 255, 0.06) !important;
    border: 1px solid rgba(0, 229, 255, 0.35) !important;
    border-radius: 8px !important;
}

/* ---------- Alert / warning boxes ---------- */
div[data-testid="stAlert"] {
    background: rgba(255, 60, 60, 0.08);
    border: 1px solid rgba(255, 60, 60, 0.4);
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# Plotly template matching the neon electronics theme
PLOTLY_TEMPLATE = "plotly_dark"
NEON_COLORS = ["#00e5ff", "#39ff14", "#ff2ec4", "#ffb800", "#7f5bff"]


def style_fig(fig):
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Rajdhani, sans-serif", color="#d9f2ff", size=13),
        title_font=dict(family="Orbitron, sans-serif", color="#00e5ff", size=16),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(t=60, b=40, l=20, r=20),
    )
    fig.update_xaxes(gridcolor="rgba(0,229,255,0.08)", zerolinecolor="rgba(0,229,255,0.15)")
    fig.update_yaxes(gridcolor="rgba(0,229,255,0.08)", zerolinecolor="rgba(0,229,255,0.15)")
    return fig


# ==========================================
# TITLE
# ==========================================

st.title("🔌 Employee Attrition Analysis Dashboard")

st.markdown(
    "<p style='color:#7fd9ff; font-size:17px; margin-top:-10px;'>"
    "Real-time analytics console to track and predict employee attrition risk ⚡"
    "</p>",
    unsafe_allow_html=True
)


# ==========================================
# LOAD DATASET
# ==========================================

DEFAULT_PATH = "WA_Fn-UseC_-HR-Employee-Attrition.csv"

st.sidebar.markdown("### 📁 Data Source")

uploaded_file = st.sidebar.file_uploader(
    "Upload HR Attrition CSV",
    type=["csv"],
    help="If not uploaded, the app tries to load from the default local path."
)

@st.cache_data
def load_data(path_or_buffer):
    return pd.read_csv(path_or_buffer)

df = None

if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    try:
        df = load_data(DEFAULT_PATH)
    except FileNotFoundError:
        st.error(
            "⚠️ Default dataset not found at the local path.\n\n"
            "Please upload the `WA_Fn-UseC_-HR-Employee-Attrition.csv` file "
            "using the sidebar uploader to continue."
        )
        st.stop()

st.sidebar.success(f"✅ Loaded {len(df)} employee records")


# ==========================================
# FILTER OPTIONS
# ==========================================

department_options = list(df["Department"].unique())
job_role_options = list(df["JobRole"].unique())
gender_options = list(df["Gender"].unique())
overtime_options = list(df["OverTime"].unique())

age_min, age_max = int(df["Age"].min()), int(df["Age"].max())
income_min, income_max = int(df["MonthlyIncome"].min()), int(df["MonthlyIncome"].max())


# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

defaults = {
    "department_filter": department_options,
    "job_role_filter": job_role_options,
    "gender_filter": gender_options,
    "overtime_filter": overtime_options,
    "age_filter": (age_min, age_max),
    "income_filter": (income_min, income_max),
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

applied_defaults = {f"applied_{k}": v for k, v in defaults.items()}

for key, val in applied_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ==========================================
# RESET FILTER FUNCTION
# ==========================================

def reset_filters():
    for key, val in defaults.items():
        st.session_state[key] = val
    for key, val in applied_defaults.items():
        st.session_state[key] = val


# ==========================================
# SIDEBAR FILTER FORM
# ==========================================

st.sidebar.header("🎛️ Filter Console")

with st.sidebar.form("filter_form"):

    st.multiselect("🏢 Department", options=department_options, key="department_filter")
    st.multiselect("💼 Job Role", options=job_role_options, key="job_role_filter")
    st.multiselect("🧑 Gender", options=gender_options, key="gender_filter")
    st.multiselect("⏰ OverTime", options=overtime_options, key="overtime_filter")

    st.slider("🎂 Age Range", min_value=age_min, max_value=age_max, key="age_filter")
    st.slider("💰 Monthly Income Range", min_value=income_min, max_value=income_max, key="income_filter")

    apply_filter = st.form_submit_button("⚡ Apply Filters", use_container_width=True)


if apply_filter:
    for key in defaults:
        st.session_state[f"applied_{key}"] = st.session_state[key]
    st.rerun()

st.sidebar.button("🔄 Reset Filters", use_container_width=True, on_click=reset_filters)


# ==========================================
# APPLY FILTERS TO DATASET
# ==========================================

filtered_df = df[
    (df["Department"].isin(st.session_state.applied_department_filter))
    & (df["JobRole"].isin(st.session_state.applied_job_role_filter))
    & (df["Gender"].isin(st.session_state.applied_gender_filter))
    & (df["OverTime"].isin(st.session_state.applied_overtime_filter))
    & (df["Age"].between(*st.session_state.applied_age_filter))
    & (df["MonthlyIncome"].between(*st.session_state.applied_income_filter))
]


# ==========================================
# EMPLOYEE OVERVIEW METRICS
# ==========================================

st.subheader("📊 Live Overview")

total_employees = len(filtered_df)
employees_left = len(filtered_df[filtered_df["Attrition"] == "Yes"])

if total_employees > 0:
    attrition_rate = (employees_left / total_employees) * 100
    average_income = filtered_df["MonthlyIncome"].mean()
    avg_age = filtered_df["Age"].mean()
    avg_tenure = filtered_df["YearsAtCompany"].mean() if "YearsAtCompany" in filtered_df.columns else None
else:
    attrition_rate = 0
    average_income = 0
    avg_age = 0
    avg_tenure = 0

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("👥 Total Employees", total_employees)

with col2:
    st.metric("🚪 Employees Left", employees_left)

with col3:
    st.metric("📉 Attrition Rate", f"{attrition_rate:.2f}%")

with col4:
    st.metric("💵 Avg Monthly Income", f"₹ {average_income:.0f}")

with col5:
    if avg_tenure is not None:
        st.metric("🕒 Avg Tenure (yrs)", f"{avg_tenure:.1f}")
    else:
        st.metric("🎂 Avg Age", f"{avg_age:.1f}")

st.markdown("<hr>", unsafe_allow_html=True)


# ==========================================
# TABS FOR INTERACTIVITY
# ==========================================

if total_employees > 0:

    tab_overview, tab_dept, tab_role, tab_factors, tab_data = st.tabs(
        ["⚡ Risk Gauge", "🏢 Department", "💼 Job Role", "🔍 Key Factors", "📋 Raw Data"]
    )

    # ---------- TAB 1: RISK GAUGE ----------
    with tab_overview:

        colg1, colg2 = st.columns([1, 1])

        with colg1:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=attrition_rate,
                title={"text": "Attrition Risk Level (%)", "font": {"family": "Orbitron", "color": "#00e5ff"}},
                number={"suffix": "%", "font": {"color": "#ffffff"}},
                gauge={
                    "axis": {"range": [0, 50], "tickcolor": "#00e5ff"},
                    "bar": {"color": "#39ff14"},
                    "bgcolor": "rgba(0,0,0,0)",
                    "borderwidth": 1,
                    "bordercolor": "#00e5ff",
                    "steps": [
                        {"range": [0, 15], "color": "rgba(57,255,20,0.25)"},
                        {"range": [15, 30], "color": "rgba(255,184,0,0.25)"},
                        {"range": [30, 50], "color": "rgba(255,46,196,0.25)"},
                    ],
                }
            ))
            gauge = style_fig(gauge)
            st.plotly_chart(gauge, use_container_width=True)

        with colg2:
            gender_attr = pd.crosstab(filtered_df["Gender"], filtered_df["Attrition"])
            fig_pie = px.pie(
                gender_attr.reset_index().melt(id_vars="Gender", var_name="Attrition", value_name="Count"),
                names="Gender",
                values="Count",
                color_discrete_sequence=NEON_COLORS,
                title="Employee Split by Gender",
                hole=0.55
            )
            fig_pie = style_fig(fig_pie)
            st.plotly_chart(fig_pie, use_container_width=True)

    # ---------- TAB 2: DEPARTMENT ----------
    with tab_dept:
        department_attrition = pd.crosstab(filtered_df["Department"], filtered_df["Attrition"]).reset_index()
        department_melted = department_attrition.melt(id_vars="Department", var_name="Attrition", value_name="Employees")

        fig1 = px.bar(
            department_melted, x="Department", y="Employees", color="Attrition",
            barmode="group", title="Attrition by Department",
            color_discrete_sequence=NEON_COLORS
        )
        st.plotly_chart(style_fig(fig1), use_container_width=True)

        fig_box_dept = px.box(
            filtered_df, x="Department", y="MonthlyIncome", color="Attrition",
            title="Income Distribution by Department", color_discrete_sequence=NEON_COLORS
        )
        st.plotly_chart(style_fig(fig_box_dept), use_container_width=True)

    # ---------- TAB 3: JOB ROLE ----------
    with tab_role:
        job_attrition = pd.crosstab(filtered_df["JobRole"], filtered_df["Attrition"]).reset_index()
        job_attrition_melted = job_attrition.melt(id_vars="JobRole", var_name="Attrition", value_name="Employees")

        fig2 = px.bar(
            job_attrition_melted, x="JobRole", y="Employees", color="Attrition",
            barmode="group", title="Attrition by Job Role", color_discrete_sequence=NEON_COLORS
        )
        fig2.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(style_fig(fig2), use_container_width=True)

        overtime_attrition = pd.crosstab(filtered_df["OverTime"], filtered_df["Attrition"]).reset_index()
        overtime_melted = overtime_attrition.melt(id_vars="OverTime", var_name="Attrition", value_name="Employees")

        fig3 = px.bar(
            overtime_melted, x="OverTime", y="Employees", color="Attrition",
            barmode="group", title="OverTime vs Attrition", color_discrete_sequence=NEON_COLORS
        )
        st.plotly_chart(style_fig(fig3), use_container_width=True)

    # ---------- TAB 4: KEY FACTORS ----------
    with tab_factors:
        fig4 = px.box(
            filtered_df, x="Attrition", y="MonthlyIncome",
            title="Monthly Income vs Attrition", color="Attrition",
            color_discrete_sequence=NEON_COLORS
        )
        st.plotly_chart(style_fig(fig4), use_container_width=True)

        col_a, col_b = st.columns(2)

        with col_a:
            if "JobSatisfaction" in filtered_df.columns:
                sat = pd.crosstab(filtered_df["JobSatisfaction"], filtered_df["Attrition"]).reset_index()
                sat_melted = sat.melt(id_vars="JobSatisfaction", var_name="Attrition", value_name="Employees")
                fig5 = px.bar(
                    sat_melted, x="JobSatisfaction", y="Employees", color="Attrition",
                    barmode="group", title="Job Satisfaction vs Attrition",
                    color_discrete_sequence=NEON_COLORS
                )
                st.plotly_chart(style_fig(fig5), use_container_width=True)

        with col_b:
            if "YearsAtCompany" in filtered_df.columns:
                fig6 = px.histogram(
                    filtered_df, x="YearsAtCompany", color="Attrition",
                    barmode="overlay", title="Tenure Distribution vs Attrition",
                    color_discrete_sequence=NEON_COLORS, nbins=20
                )
                st.plotly_chart(style_fig(fig6), use_container_width=True)

    # ---------- TAB 5: RAW DATA ----------
    with tab_data:
        st.dataframe(filtered_df, use_container_width=True)

        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download Filtered Data (CSV)",
            data=csv_data,
            file_name="filtered_attrition_data.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    st.warning("⚠️ No data available for selected filters. Try widening your filter console settings.")