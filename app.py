import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Business Data Analysis Dashboard", page_icon="📊", layout="wide")

st.title("📊 Business Data Analysis Dashboard")
st.caption("Explore sales, profitability, product performance and regional trends.")

@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_csv(Path(__file__).parent / "business_sales_data.csv")
    data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")
    required = {"Order_ID","Order_Date","Region","Category","Product","Units_Sold",
                "Revenue","Cost","Profit","Channel"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing)))
    return data.dropna(subset=["Order_Date"])

with st.sidebar:
    st.header("Data & filters")
    uploaded = st.file_uploader("Upload your sales CSV (optional)", type=["csv"])
    try:
        df = load_data(uploaded)
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    min_date, max_date = df["Order_Date"].min().date(), df["Order_Date"].max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date),
                               min_value=min_date, max_value=max_date)
    regions = st.multiselect("Region", sorted(df["Region"].dropna().unique()),
                             default=sorted(df["Region"].dropna().unique()))
    categories = st.multiselect("Category", sorted(df["Category"].dropna().unique()),
                                default=sorted(df["Category"].dropna().unique()))
    channels = st.multiselect("Channel", sorted(df["Channel"].dropna().unique()),
                              default=sorted(df["Channel"].dropna().unique()))

if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start, end = df["Order_Date"].min(), df["Order_Date"].max()

filtered = df[
    df["Order_Date"].between(start, end)
    & df["Region"].isin(regions)
    & df["Category"].isin(categories)
    & df["Channel"].isin(channels)
].copy()

if filtered.empty:
    st.warning("No records match the selected filters. Adjust the filters in the sidebar.")
    st.stop()

revenue = filtered["Revenue"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order_ID"].nunique()
units = filtered["Units_Sold"].sum()
margin = (profit / revenue * 100) if revenue else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total Revenue", f"₹{revenue:,.0f}")
k2.metric("Total Profit", f"₹{profit:,.0f}")
k3.metric("Orders", f"{orders:,}")
k4.metric("Units Sold", f"{units:,}")
k5.metric("Profit Margin", f"{margin:.1f}%")

st.divider()
left, right = st.columns(2)

monthly = (filtered.assign(Month=filtered["Order_Date"].dt.to_period("M").astype(str))
           .groupby("Month", as_index=False).agg(Revenue=("Revenue","sum"), Profit=("Profit","sum")))
with left:
    st.subheader("Monthly revenue trend")
    fig = px.line(monthly, x="Month", y="Revenue", markers=True,
                  labels={"Revenue":"Revenue (₹)", "Month":"Month"})
    st.plotly_chart(fig, use_container_width=True)

category = (filtered.groupby("Category", as_index=False)
            .agg(Revenue=("Revenue","sum"), Profit=("Profit","sum")))
with right:
    st.subheader("Revenue by category")
    fig = px.bar(category, x="Category", y="Revenue", color="Category",
                 labels={"Revenue":"Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
region = filtered.groupby("Region", as_index=False).agg(Revenue=("Revenue","sum"), Profit=("Profit","sum"))
with left:
    st.subheader("Regional performance")
    fig = px.bar(region, x="Region", y="Revenue", color="Region",
                 labels={"Revenue":"Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)

product = (filtered.groupby("Product", as_index=False)
           .agg(Revenue=("Revenue","sum"), Units=("Units_Sold","sum"))
           .sort_values("Revenue", ascending=False).head(10))
with right:
    st.subheader("Top 10 products by revenue")
    fig = px.bar(product.sort_values("Revenue"), x="Revenue", y="Product", orientation="h",
                 labels={"Revenue":"Revenue (₹)"})
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered sales records")
st.dataframe(filtered.sort_values("Order_Date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("⬇️ Download filtered data as CSV",
                   data=filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_business_sales.csv", mime="text/csv")

st.info("Sample data is synthetic and intended for learning/demo purposes. Replace it with authorized business data before using this dashboard professionally.")
