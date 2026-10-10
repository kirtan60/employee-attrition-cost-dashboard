import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Employee Attrition & Cost Dashboard", layout="wide")
st.title("📊 Employee Attrition & Workforce Cost Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
file = st.file_uploader("Upload Dataset (CSV or Excel)", type=["csv", "xlsx"])

if file is not None:
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)
else:
    try:
        df = pd.read_csv("HR.csv")
        st.success("Using default dataset: HR.csv")
    except FileNotFoundError:
        st.error("HR.csv not found. Please upload a dataset.")
        st.stop()

# 'sales' in this dataset is actually the department
df = df.rename(columns={"sales": "department"})

# -----------------------------
# CLEANING (with transparency)
# -----------------------------
before = len(df)
df = df.drop_duplicates().dropna()
st.info(
    f"Cleaning removed {before - len(df):,} duplicate/missing rows "
    f"({before:,} → {len(df):,})."
)

if "left" in df.columns:
    df["status"] = df["left"].map({0: "Stayed", 1: "Left"})

# -----------------------------
# PREVIEW
# -----------------------------
st.subheader("📄 Data Preview")
st.dataframe(df.head())

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

if "department" in df.columns:
    dept = st.sidebar.selectbox("Department", ["All"] + sorted(df["department"].unique()))
    if dept != "All":
        df = df[df["department"] == dept]

if "salary" in df.columns:
    sal = st.sidebar.selectbox("Salary Level", ["All"] + sorted(df["salary"].unique()))
    if sal != "All":
        df = df[df["salary"] == sal]

# -----------------------------
# COST ASSUMPTIONS (editable)
# -----------------------------
st.sidebar.header("💰 Cost Assumptions")
st.sidebar.caption("The dataset has salary levels only, so annual pay per level is assumed.")
low_pay = st.sidebar.number_input("Annual salary - Low (₹)", value=300000, step=50000)
med_pay = st.sidebar.number_input("Annual salary - Medium (₹)", value=600000, step=50000)
high_pay = st.sidebar.number_input("Annual salary - High (₹)", value=1200000, step=50000)
replace_pct = st.sidebar.slider("Replacement cost (% of annual salary)", 10, 150, 50)

# -----------------------------
# EMPTY FILTER CHECK
# -----------------------------
if df.empty:
    st.warning("No data for this filter combination.")
    st.stop()

# -----------------------------
# COST CALCULATION
# -----------------------------
has_cost = "salary" in df.columns and "left" in df.columns
if has_cost:
    pay_map = {"low": low_pay, "medium": med_pay, "high": high_pay}
    df["assumed_annual_salary"] = df["salary"].map(pay_map)
    df["attrition_cost"] = df["assumed_annual_salary"] * (replace_pct / 100) * df["left"]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📊 Key Metrics")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Employees", f"{len(df):,}")

if "satisfaction_level" in df.columns:
    c2.metric("Avg Satisfaction", round(df["satisfaction_level"].mean(), 2))
if "left" in df.columns:
    c3.metric("Attrition Rate", f"{df['left'].mean() * 100:.1f} %")
if has_cost:
    c4.metric("Est. Attrition Cost", f"₹{df['attrition_cost'].sum():,.0f}")

# -----------------------------
# KEY INSIGHTS
# -----------------------------
st.subheader("🔎 Key Insights")
if "left" in df.columns:
    col_a, col_b = st.columns(2)

    if "salary" in df.columns:
        by_salary = (
            df.groupby("salary")["left"].mean().mul(100).round(1)
            .reset_index(name="attrition_pct")
            .sort_values("attrition_pct", ascending=False)
        )
        col_a.write("**Attrition % by salary level**")
        col_a.dataframe(by_salary, hide_index=True)

    if "department" in df.columns:
        by_dept = (
            df.groupby("department")["left"].mean().mul(100).round(1)
            .reset_index(name="attrition_pct")
            .sort_values("attrition_pct", ascending=False)
        )
        col_b.write("**Attrition % by department**")
        col_b.dataframe(by_dept, hide_index=True)

if has_cost and "department" in df.columns:
    cost_dept = (
        df.groupby("department")["attrition_cost"].sum()
        .reset_index().sort_values("attrition_cost", ascending=False)
    )
    st.subheader("💸 Estimated Attrition Cost by Department")
    fig_cost = px.bar(
        cost_dept, x="department", y="attrition_cost",
        labels={"attrition_cost": "Estimated cost (₹)", "department": "Department"},
    )
    st.plotly_chart(fig_cost, use_container_width=True)

# -----------------------------
# VISUALIZATIONS
# -----------------------------
if "satisfaction_level" in df.columns:
    st.subheader("😊 Satisfaction Level Distribution")
    fig1 = px.histogram(
        df, x="satisfaction_level", color="status" if "status" in df.columns else None,
        barmode="overlay", opacity=0.7,
        labels={"satisfaction_level": "Satisfaction level"},
    )
    st.plotly_chart(fig1, use_container_width=True)

if "number_project" in df.columns and "average_montly_hours" in df.columns:
    st.subheader("📈 Number of Projects vs Monthly Hours")
    fig2 = px.box(
        df, x="number_project", y="average_montly_hours",
        color="status" if "status" in df.columns else None,
        labels={"number_project": "Number of projects",
                "average_montly_hours": "Average monthly hours"},
    )
    st.plotly_chart(fig2, use_container_width=True)

if "salary" in df.columns:
    st.subheader("💰 Salary Level Distribution")
    fig3 = px.pie(df, names="salary")
    st.plotly_chart(fig3, use_container_width=True)

if "department" in df.columns:
    st.subheader("🏢 Employees by Department")
    dept_counts = df["department"].value_counts().rename_axis("department").reset_index(name="employees")
    fig4 = px.bar(dept_counts, x="department", y="employees",
                  labels={"department": "Department", "employees": "Employees"})
    st.plotly_chart(fig4, use_container_width=True)

if "status" in df.columns and "satisfaction_level" in df.columns:
    st.subheader("🚪 Satisfaction: Stayed vs Left")
    fig5 = px.box(df, x="status", y="satisfaction_level", color="status",
                  labels={"satisfaction_level": "Satisfaction level", "status": "Status"})
    st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# DOWNLOAD
# -----------------------------
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Cleaned Data", csv, "cleaned_data.csv", mime="text/csv")
