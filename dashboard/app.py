import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Page Config
st.set_page_config(
    page_title="Restaurant Sales Dashboard",
    page_icon="🍽️",
    layout="wide"
)

st.title("🍽️ Restaurant Sales Analysis Dashboard")

# CSV Path
BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR.parent / "data" / "restaurant_sales.csv"

# Load Data
df = pd.read_csv(CSV_PATH)

# Create Revenue Column
df["Revenue"] = df["Quantity"] * df["Price"]

# KPIs
total_revenue = df["Revenue"].sum()
total_orders = df["Order_ID"].nunique()
total_items = df["Quantity"].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Items Sold", total_items)

st.divider()

# Top Selling Items
st.subheader("Top Selling Items")

top_items = (
    df.groupby("Item")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 4))
top_items.plot(kind="bar", ax=ax)
ax.set_ylabel("Quantity Sold")
st.pyplot(fig)

# Revenue by Category
st.subheader("Revenue by Category")

category_sales = (
    df.groupby("Category")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(8, 4))
category_sales.plot(kind="bar", ax=ax)
ax.set_ylabel("Revenue")
st.pyplot(fig)

# Daily Revenue Trend
st.subheader("Daily Revenue Trend")

df["Date"] = pd.to_datetime(df["Date"])

daily_sales = (
    df.groupby("Date")["Revenue"]
    .sum()
)

fig, ax = plt.subplots(figsize=(10, 4))
daily_sales.plot(ax=ax)
ax.set_ylabel("Revenue")
st.pyplot(fig)

# Raw Data
st.subheader("Dataset Preview")
st.dataframe(df.head(20), use_container_width=True)