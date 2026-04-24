import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="HR Analytics Dashboard", layout="wide")

st.title("📊 Employee Analytics Dashboard")

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
    # 🔥 DEFAULT FILE (IMPORTANT)
    try:
        df = pd.read_csv("HR.csv")
        st.success("Using default dataset: HR.csv")
    except:
        st.error("❌ HR.csv not found. Please upload dataset.")
        st.stop()

# -----------------------------
# PREVIEW
# -----------------------------
st.subheader("📄 Data Preview")
st.dataframe(df.head())

# -----------------------------
# CLEANING
# -----------------------------
df = df.drop_duplicates()
df = df.dropna()

# -----------------------------
# SIDEBAR FILTERS
# -----------------------------
st.sidebar.header("🔍 Filters")

if "sales" in df.columns:
    dept = st.sidebar.selectbox("Department", ["All"] + list(df["sales"].unique()))
    if dept != "All":
        df = df[df["sales"] == dept]

if "salary" in df.columns:
    sal = st.sidebar.selectbox("Salary Level", ["All"] + list(df["salary"].unique()))
    if sal != "All":
        df = df[df["salary"] == sal]

# -----------------------------
# KPIs
# -----------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Employees", len(df))

if "satisfaction_level" in df.columns:
    col2.metric("Avg Satisfaction", round(df["satisfaction_level"].mean(), 2))

if "left" in df.columns:
    col3.metric("Attrition Rate", f"{round(df['left'].mean()*100,2)} %")

# -----------------------------
# VISUALIZATIONS
# -----------------------------

# Satisfaction Distribution
if "satisfaction_level" in df.columns:
    st.subheader("😊 Satisfaction Level Distribution")
    fig1 = px.histogram(df, x="satisfaction_level")
    st.plotly_chart(fig1, use_container_width=True)

# Projects vs Hours
if "number_project" in df.columns:
    st.subheader("📈 Projects vs Working Hours")
    fig2 = px.scatter(df, x="number_project", y="average_montly_hours", color="left")
    st.plotly_chart(fig2, use_container_width=True)

# Salary Distribution
if "salary" in df.columns:
    st.subheader("💰 Salary Distribution")
    fig3 = px.pie(df, names="salary")
    st.plotly_chart(fig3, use_container_width=True)

# Department Distribution
if "sales" in df.columns:
    st.subheader("🏢 Department Distribution")
    fig4 = px.bar(df["sales"].value_counts())
    st.plotly_chart(fig4, use_container_width=True)

# Attrition Analysis
if "left" in df.columns:
    st.subheader("🚪 Attrition Analysis")
    fig5 = px.box(df, x="left", y="satisfaction_level")
    st.plotly_chart(fig5, use_container_width=True)

# -----------------------------
# DOWNLOAD
# -----------------------------
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Cleaned Data", csv, "cleaned_data.csv")