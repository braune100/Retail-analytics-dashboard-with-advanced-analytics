# 🛍️ Retail Analytics Dashboard

An interactive **retail sales analytics dashboard** built with Python and Streamlit.  
This project transforms raw transactional data into **business insights**, including KPIs, customer segmentation, RFM analysis, churn detection, and revenue trends.

---

## 🚀 Live Demo
👉 https://Retail-analytics-dashboard-with-advanced-analytics.streamlit.app

---

## 📊 Project Overview

This dashboard helps analyze retail performance and customer behavior by answering key business questions:

- What is the total revenue and sales performance?
- Who are the best customers?
- Which products and countries generate the most revenue?
- How do customers behave over time?
- Which customers are at risk of churning?

---

## 🧠 Key Features

### 📈 Business KPIs
- Total Revenue
- Total Orders
- Total Customers

### 🏆 Sales Performance
- Top 10 Products by Revenue
- Top 10 Countries by Revenue
- Sales trends over time
- Hourly sales distribution

### 👥 Customer Analytics
- Customer segmentation (VIP vs Regular)
- Repeat vs One-time customers

### 🧠 Advanced Analytics
- RFM (Recency, Frequency, Monetary) analysis
- Customer segmentation (High / Mid / Low value)
- Customer Lifetime Value (CLV)
- Churn risk identification

---

## 🛠️ Tech Stack

- Python 🐍
- Streamlit 📊
- Pandas 📦
- Data Visualization (Streamlit charts)

---

## 📁 Dataset

The dataset used is the **Online Retail Dataset**, which contains transactional data including:

- Invoice number
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

---

## 📊 RFM Analysis Explained

RFM is a customer segmentation technique:

- **Recency** → How recently a customer purchased
- **Frequency** → How often they purchase
- **Monetary** → How much they spend

This allows segmentation into:
- 🏆 High Value Customers
- ⚖️ Mid Value Customers
- ⚠️ Low Value / At Risk Customers

---

## 📉 Business Impact

This dashboard helps businesses:

- Identify high-value customers
- Improve customer retention strategies
- Detect churn risk early
- Optimize marketing campaigns
- Increase revenue through targeted actions

---

## 📷 Dashboard Preview

(Add screenshot here)

---

## 🚀 How to Run Locally

```bash
# Clone repository
git clone https://github.com/braune100/retail-dashboard.git

# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
