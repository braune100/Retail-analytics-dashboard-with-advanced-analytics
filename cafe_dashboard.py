import streamlit as st
import pandas as pd

df = pd.read_csv("coffee_sales.csv")

df["revenue"] = df["quantity"] * df["price"]

st.title("☕ Coffee Shop Dashboard")

# KPIs
total_revenue = df["revenue"].sum()
total_orders = df["quantity"].sum()
avg_ticket = total_revenue / total_orders

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:.2f}")
col2.metric("Total Items Sold", int(total_orders))
col3.metric("Avg Ticket", f"${avg_ticket:.2f}")

# Filters
product_filter = st.multiselect("Filter by product", df["product"].unique())
category_filter = st.multiselect("Filter by category", df["category"].unique())

filtered = df.copy()

if product_filter:
    filtered = filtered[filtered["product"].isin(product_filter)]

if category_filter:
    filtered = filtered[filtered["category"].isin(category_filter)]

# Charts
st.subheader("Revenue by Product")
st.bar_chart(filtered.groupby("product")["revenue"].sum())

st.subheader("Revenue by Category")
st.bar_chart(filtered.groupby("category")["revenue"].sum())

st.subheader("Hourly Sales")
filtered["hour"] = pd.to_datetime(filtered["time"]).dt.hour
st.bar_chart(filtered.groupby("hour")["revenue"].sum())