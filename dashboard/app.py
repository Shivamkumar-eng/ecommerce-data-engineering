import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GOLD_PATH = PROJECT_ROOT / "data" / "gold"


# =========================================================
# LOAD GOLD DATA
# =========================================================

@st.cache_data
def load_data():

    customer_revenue = pd.read_parquet(
        GOLD_PATH / "customer_revenue"
    )

    product_sales = pd.read_parquet(
        GOLD_PATH / "product_sales"
    )

    daily_sales = pd.read_parquet(
        GOLD_PATH / "daily_sales"
    )

    payment_summary = pd.read_parquet(
        GOLD_PATH / "payment_summary"
    )

    return (
        customer_revenue,
        product_sales,
        daily_sales,
        payment_summary
    )


customer_revenue, product_sales, daily_sales, payment_summary = load_data()


# =========================================================
# TITLE
# =========================================================

st.title("📊 E-Commerce Analytics Dashboard")

st.markdown(
    "Business analytics powered by the Gold layer of the "
    "E-Commerce Data Engineering Pipeline."
)

st.divider()


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_revenue = product_sales["total_revenue"].sum()

total_orders = product_sales["total_orders"].sum()

total_units = product_sales["units_sold"].sum()

total_customers = customer_revenue["customer_id"].nunique()


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "🛒 Total Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "📦 Units Sold",
        f"{total_units:,}"
    )

with col4:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )


st.divider()


# =========================================================
# DAILY REVENUE
# =========================================================

st.subheader("📈 Daily Revenue Trend")

daily_sales["order_date"] = pd.to_datetime(
    daily_sales["order_date"]
)

daily_sales_sorted = daily_sales.sort_values(
    "order_date"
)

fig_daily = px.line(
    daily_sales_sorted,
    x="order_date",
    y="total_revenue",
    markers=True,
    labels={
        "order_date": "Date",
        "total_revenue": "Revenue"
    }
)

fig_daily.update_layout(
    hovermode="x unified"
)

st.plotly_chart(
    fig_daily,
    use_container_width=True
)


# =========================================================
# PRODUCT ANALYSIS
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🏆 Top 10 Products by Revenue")

    top_products = (
        product_sales
        .sort_values(
            "total_revenue",
            ascending=False
        )
        .head(10)
        .sort_values("total_revenue")
    )

    fig_products = px.bar(
        top_products,
        x="total_revenue",
        y="product_id",
        orientation="h",
        labels={
            "product_id": "Product ID",
            "total_revenue": "Revenue"
        }
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True
    )


with col2:

    st.subheader("📦 Top 10 Products by Units Sold")

    top_units = (
        product_sales
        .sort_values(
            "units_sold",
            ascending=False
        )
        .head(10)
        .sort_values("units_sold")
    )

    fig_units = px.bar(
        top_units,
        x="units_sold",
        y="product_id",
        orientation="h",
        labels={
            "product_id": "Product ID",
            "units_sold": "Units Sold"
        }
    )

    st.plotly_chart(
        fig_units,
        use_container_width=True
    )


# =========================================================
# PAYMENT ANALYSIS
# =========================================================

st.subheader("💳 Payment Method Distribution")

payment_summary_display = payment_summary.copy()

payment_summary_display["payment_method"] = (
    payment_summary_display["payment_method"]
    .fillna("Unknown")
)

fig_payment = px.pie(
    payment_summary_display,
    names="payment_method",
    values="total_payments",
    hole=0.45
)

st.plotly_chart(
    fig_payment,
    use_container_width=True
)


# =========================================================
# CUSTOMER REVENUE
# =========================================================

st.subheader("👥 Top Customers by Revenue")

top_customers = (
    customer_revenue
    .sort_values(
        "total_revenue",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_customers,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Built with Python • Streamlit • Pandas • Plotly • PySpark"
)