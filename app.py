import streamlit as st
import pandas as pd

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

# ----------------------------
# LOAD DATA
# ----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("online_retail.csv", encoding="ISO-8859-1")

    df.columns = df.columns.str.strip()

    df = df.dropna(subset=["CustomerID", "Description"])
    df = df[df["Quantity"] > 0]
    df = df[df["UnitPrice"] > 0]

    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    df["Date"] = df["InvoiceDate"].dt.date
    df["Hour"] = df["InvoiceDate"].dt.hour
    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    return df


df = load_data()

# ----------------------------
# SIDEBAR FILTER
# ----------------------------
st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["Country"].dropna().unique())
)

if country != "All":
    df = df[df["Country"] == country]

# ----------------------------
# HEADER
# ----------------------------
st.title("🛍️ Retail Analytics Dashboard")

st.markdown("""
Analyze sales performance, customer behavior, and revenue trends across markets.
""")

st.divider()

# ----------------------------
# KPIs
# ----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"${df['Revenue'].sum():,.0f}")
col2.metric("🧾 Total Orders", f"{df['InvoiceNo'].nunique():,}")
col3.metric("👤 Total Customers", f"{df['CustomerID'].nunique():,}")

st.divider()

# ----------------------------
# INSIGHTS
# ----------------------------
top_product = df.groupby("Description")["Revenue"].sum().idxmax()
top_country = df.groupby("Country")["Revenue"].sum().idxmax()

st.success(f"""
🔥 Top Product: **{top_product}**  
🌍 Top Market: **{top_country}**
""")

# ----------------------------
# TOP PRODUCTS & COUNTRIES
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Products")
    st.bar_chart(
        df.groupby("Description")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

with col2:
    st.subheader("🌍 Top 10 Countries")
    st.bar_chart(
        df.groupby("Country")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

# ----------------------------
# TIME ANALYSIS
# ----------------------------
st.subheader("📈 Sales Over Time")
st.line_chart(df.groupby("Date")["Revenue"].sum())

st.subheader("⏰ Sales by Hour")
st.bar_chart(df.groupby("Hour")["Revenue"].sum())

# ----------------------------
# ADVANCED ANALYTICS
# ----------------------------
st.divider()
st.header("📊 Advanced Analytics")

# Monthly trend
st.subheader("📅 Monthly Revenue Trend")
monthly_revenue = df.groupby("Month")["Revenue"].sum()
st.line_chart(monthly_revenue)

# Growth
st.subheader("📈 Month-over-Month Growth (%)")
st.line_chart(monthly_revenue.pct_change() * 100)

# Customer segmentation
st.subheader("👥 Customer Segmentation")
customer_revenue = df.groupby("CustomerID")["Revenue"].sum()

vip = customer_revenue[customer_revenue > 1000]
regular = customer_revenue[customer_revenue <= 1000]

col1, col2 = st.columns(2)
col1.metric("VIP Customers", len(vip))
col2.metric("Regular Customers", len(regular))

# Repeat customers
st.subheader("🔁 Customer Behavior")
customer_orders = df.groupby("CustomerID")["InvoiceNo"].nunique()

col1, col2 = st.columns(2)
col1.metric("Repeat Customers", (customer_orders > 1).sum())
col2.metric("One-Time Customers", (customer_orders == 1).sum())

# ----------------------------
# RFM ANALYSIS
# ----------------------------
st.divider()
st.header("🧠 RFM Analysis")

snapshot_date = df["InvoiceDate"].max()

rfm = df.groupby("CustomerID").agg({
    "InvoiceDate": lambda x: (snapshot_date - x.max()).days,
    "InvoiceNo": "nunique",
    "Revenue": "sum"
})

rfm.columns = ["Recency", "Frequency", "Monetary"]

# FIXED scoring (no more qcut error)
rfm["R_score"] = pd.qcut(rfm["Recency"].rank(method="first"), 4, labels=[4,3,2,1])
rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1,2,3,4])
rfm["M_score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 4, labels=[1,2,3,4])

rfm["RFM_Score"] = (
    rfm["R_score"].astype(str) +
    rfm["F_score"].astype(str) +
    rfm["M_score"].astype(str)
)

# Segmentation
def segment(row):
    if row["RFM_Score"] in ["444", "443", "434"]:
        return "High Value"
    elif row["RFM_Score"] in ["344", "334", "333"]:
        return "Mid Value"
    else:
        return "Low Value"

rfm["Segment"] = rfm.apply(segment, axis=1)

# Segment descriptions
segment_summary = {
    "High Value": "Loyal & high spenders",
    "Mid Value": "Regular customers with growth potential",
    "Low Value": "Low engagement / at-risk"
}

rfm["Segment_Description"] = rfm["Segment"].map(segment_summary)

# Visualization
st.subheader("📊 Customer Segments")
st.bar_chart(rfm["Segment"].value_counts())

# Insights
st.subheader("📌 Segment Insights")

high_pct = (rfm["Segment"] == "High Value").mean() * 100
low_pct = (rfm["Segment"] == "Low Value").mean() * 100

st.write(f"🔝 High-value customers: **{high_pct:.1f}%**")
st.write(f"⚠️ Low-value customers: **{low_pct:.1f}%**")

# ----------------------------
# CLV
# ----------------------------
st.subheader("💰 Customer Lifetime Value")

avg_order_value = df["Revenue"].mean()
purchase_freq = df.groupby("CustomerID")["InvoiceNo"].nunique().mean()

clv = avg_order_value * purchase_freq
st.metric("Estimated CLV", f"${clv:,.2f}")

# ----------------------------
# CHURN
# ----------------------------
st.subheader("📉 Churn Indicator")

rfm["Churn_Risk"] = rfm["Recency"].apply(
    lambda x: "High Risk" if x > 90 else "Active"
)

st.bar_chart(rfm["Churn_Risk"].value_counts())

# ----------------------------
# RECOMMENDATIONS
# ----------------------------
st.subheader("🎯 Recommended Actions")

st.markdown("""
- **High Value** → Loyalty programs, VIP offers  
- **Mid Value** → Upsell & cross-sell campaigns  
- **Low Value** → Re-engagement campaigns (discounts, email)
""")

# ----------------------------
# RAW DATA
# ----------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(df.head(100))