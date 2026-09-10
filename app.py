import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Employee Attrition Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==========================================
# TITLE
# ==========================================

st.title("📊 Employee Attrition Analysis Dashboard")

st.write(
    "Analyze employee attrition and identify employees at risk of leaving."
)


# ==========================================
# LOAD DATASET
# ==========================================

df = pd.read_csv(
    r"D:\electronics\Agentic AI\WA_Fn-UseC_-HR-Employee-Attrition.csv"
)


# ==========================================
# FILTER OPTIONS
# ==========================================

department_options = list(df["Department"].unique())

job_role_options = list(df["JobRole"].unique())

gender_options = list(df["Gender"].unique())

overtime_options = list(df["OverTime"].unique())


# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if "department_filter" not in st.session_state:
    st.session_state.department_filter = department_options

if "job_role_filter" not in st.session_state:
    st.session_state.job_role_filter = job_role_options

if "gender_filter" not in st.session_state:
    st.session_state.gender_filter = gender_options

if "overtime_filter" not in st.session_state:
    st.session_state.overtime_filter = overtime_options


# ==========================================
# APPLIED FILTERS INITIALIZATION
# ==========================================

if "applied_department" not in st.session_state:
    st.session_state.applied_department = department_options

if "applied_job_role" not in st.session_state:
    st.session_state.applied_job_role = job_role_options

if "applied_gender" not in st.session_state:
    st.session_state.applied_gender = gender_options

if "applied_overtime" not in st.session_state:
    st.session_state.applied_overtime = overtime_options


# ==========================================
# RESET FILTER FUNCTION
# ==========================================

def reset_filters():

    # Reset Form Widget Values

    st.session_state.department_filter = department_options

    st.session_state.job_role_filter = job_role_options

    st.session_state.gender_filter = gender_options

    st.session_state.overtime_filter = overtime_options


    # Reset Applied Filters

    st.session_state.applied_department = department_options

    st.session_state.applied_job_role = job_role_options

    st.session_state.applied_gender = gender_options

    st.session_state.applied_overtime = overtime_options


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("🔍 Filter Employees")


# ==========================================
# FILTER FORM
# ==========================================

with st.sidebar.form("filter_form"):


    # Department

    st.multiselect(
        "Select Department",
        options=department_options,
        key="department_filter"
    )


    # Job Role

    st.multiselect(
        "Select Job Role",
        options=job_role_options,
        key="job_role_filter"
    )


    # Gender

    st.multiselect(
        "Select Gender",
        options=gender_options,
        key="gender_filter"
    )


    # OverTime

    st.multiselect(
        "Select OverTime",
        options=overtime_options,
        key="overtime_filter"
    )


    # Apply Button

    apply_filter = st.form_submit_button(
        "✅ Apply Filters",
        use_container_width=True
    )


# ==========================================
# APPLY FILTERS
# ==========================================

if apply_filter:

    st.session_state.applied_department = (
        st.session_state.department_filter
    )

    st.session_state.applied_job_role = (
        st.session_state.job_role_filter
    )

    st.session_state.applied_gender = (
        st.session_state.gender_filter
    )

    st.session_state.applied_overtime = (
        st.session_state.overtime_filter
    )

    st.rerun()


# ==========================================
# RESET BUTTON
# ==========================================

st.sidebar.button(
    "🔄 Reset Filters",
    use_container_width=True,
    on_click=reset_filters
)


# ==========================================
# APPLY FILTERS TO DATASET
# ==========================================

filtered_df = df[

    (df["Department"].isin(
        st.session_state.applied_department
    ))

    &

    (df["JobRole"].isin(
        st.session_state.applied_job_role
    ))

    &

    (df["Gender"].isin(
        st.session_state.applied_gender
    ))

    &

    (df["OverTime"].isin(
        st.session_state.applied_overtime
    ))

]


# ==========================================
# EMPLOYEE OVERVIEW METRICS
# ==========================================

st.subheader("📊 Employee Overview")


# Total Employees

total_employees = len(filtered_df)


# Employees Left

employees_left = len(

    filtered_df[
        filtered_df["Attrition"] == "Yes"
    ]

)


# Calculate Values

if total_employees > 0:

    attrition_rate = (
        employees_left / total_employees
    ) * 100


    average_income = filtered_df[
        "MonthlyIncome"
    ].mean()


else:

    attrition_rate = 0

    average_income = 0


# ==========================================
# METRIC COLUMNS
# ==========================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Total Employees",
        total_employees
    )


with col2:

    st.metric(
        "Employees Left",
        employees_left
    )


with col3:

    st.metric(
        "Attrition Rate",
        f"{attrition_rate:.2f}%"
    )


with col4:

    st.metric(
        "Average Monthly Income",
        f"₹ {average_income:.0f}"
    )


# ==========================================
# DATASET PREVIEW
# ==========================================

st.subheader("👥 Employee Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)


# ==========================================
# CHECK DATA AVAILABLE
# ==========================================

if len(filtered_df) > 0:


    # ==========================================
    # CHART 1
    # DEPARTMENT-WISE ATTRITION
    # ==========================================

    st.subheader("📊 Department-wise Attrition")


    department_attrition = pd.crosstab(
        filtered_df["Department"],
        filtered_df["Attrition"]
    ).reset_index()


    department_melted = department_attrition.melt(
        id_vars="Department",
        var_name="Attrition",
        value_name="Employees"
    )


    fig1 = px.bar(
        department_melted,
        x="Department",
        y="Employees",
        color="Attrition",
        barmode="group",
        title="Attrition by Department"
    )


    st.plotly_chart(
        fig1,
        use_container_width=True
    )


    # ==========================================
    # CHART 2
    # JOB ROLE-WISE ATTRITION
    # ==========================================

    st.subheader("💼 Job Role-wise Attrition")


    job_attrition = pd.crosstab(
        filtered_df["JobRole"],
        filtered_df["Attrition"]
    ).reset_index()


    job_attrition_melted = job_attrition.melt(
        id_vars="JobRole",
        var_name="Attrition",
        value_name="Employees"
    )


    fig2 = px.bar(
        job_attrition_melted,
        x="JobRole",
        y="Employees",
        color="Attrition",
        barmode="group",
        title="Attrition by Job Role"
    )


    fig2.update_layout(
        xaxis_tickangle=-45
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )


    # ==========================================
    # CHART 3
    # OVERTIME VS ATTRITION
    # ==========================================

    st.subheader("⏰ OverTime vs Attrition")


    overtime_attrition = pd.crosstab(
        filtered_df["OverTime"],
        filtered_df["Attrition"]
    ).reset_index()


    overtime_melted = overtime_attrition.melt(
        id_vars="OverTime",
        var_name="Attrition",
        value_name="Employees"
    )


    fig3 = px.bar(
        overtime_melted,
        x="OverTime",
        y="Employees",
        color="Attrition",
        barmode="group",
        title="OverTime vs Attrition"
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )


    # ==========================================
    # CHART 4
    # MONTHLY INCOME VS ATTRITION
    # ==========================================

    st.subheader("💰 Monthly Income vs Attrition")


    fig4 = px.box(
        filtered_df,
        x="Attrition",
        y="MonthlyIncome",
        title="Monthly Income Distribution by Attrition"
    )


    st.plotly_chart(
        fig4,
        use_container_width=True
    )


else:

    st.warning(
        "⚠️ No data available for selected filters."
    )