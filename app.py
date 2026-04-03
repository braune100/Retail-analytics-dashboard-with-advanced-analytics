import streamlit as st
import pandas as pd

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Coffee Dashboard", layout="wide")

# ---------------------------
# LOAD DATA
# ---------------------------
df = pd.read_csv("cafe_sales.csv")

# Clean columns
df.columns = df.columns.str.strip().str.lower()

# Convert date & time
df['date'] = pd.to_datetime(df['date'])
df['time'] = pd.to_datetime(df['time'])

# Feature engineering
df['hour'] = df['time'].dt.hour
df['revenue'] = df['quantity'] * df['price']

# ---------------------------
# SIDEBAR (FILTERS)
# ---------------------------
st.sidebar.header("Filters")

start_date = st.sidebar.date_input("Start Date", df['date'].min())
end_date = st.sidebar.date_input("End Date", df['date'].max())

margin = st.sidebar.slider("Profit Margin (%)", 0, 100, 30)

# Filter data
filtered_df = df[
    (df['date'] >= pd.to_datetime(start_date)) &
    (df['date'] <= pd.to_datetime(end_date))
].copy()

# Profit calculation
filtered_df['profit'] = filtered_df['revenue'] * (margin / 100)

# ---------------------------
# KPIs
# ---------------------------
total_revenue = filtered_df['revenue'].sum()
total_profit = filtered_df['profit'].sum()

top_product = filtered_df.groupby('product')['quantity'].sum().idxmax()

hourly_sales = filtered_df.groupby('hour')['revenue'].sum()
busiest_hour = hourly_sales.idxmax()

# ---------------------------
# TITLE
# ---------------------------
st.title("☕ Coffee Sales Dashboard")

# KPI columns
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${total_revenue:.2f}")
col2.metric("Total Profit", f"${total_profit:.2f}")
col3.metric("Top Product", top_product)
col4.metric("Busiest Hour", f"{busiest_hour}:00")

# ---------------------------
# CHARTS
# ---------------------------

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Daily Revenue")
    daily_sales = filtered_df.groupby('date')['revenue'].sum()
    st.line_chart(daily_sales)

with col2:
    st.subheader("Sales by Product")
    sales_product = filtered_df.groupby('product')['revenue'].sum()
    st.bar_chart(sales_product)

# Row 2
col3, col4 = st.columns(2)

with col3:
    st.subheader("Sales by Category")
    sales_category = filtered_df.groupby('category')['revenue'].sum()
    st.bar_chart(sales_category)

with col4:
    st.subheader("Peak Hours")
    hourly_sales = hourly_sales.sort_index()
    st.bar_chart(hourly_sales)

# ---------------------------
# DATA TABLE
# ---------------------------
st.subheader("Filtered Data")
st.dataframe(filtered_df)