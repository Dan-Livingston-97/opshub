
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="OpsHub",
    page_icon="📊",
    layout="wide"
)

st.title("OpsHub")
st.subheader("Business Operations Intelligence Platform")

st.write(
    "Welcome to OpsHub, a business operations "
    "analytics application."
)

# Sample fictional order data
orders = pd.DataFrame({
    "Order ID": [1001, 1002, 1003, 1004, 1005],
    "Customer": [
        "Northstar Retail",
        "Summit Supply",
        "Metro Distribution",
        "Lakeside Goods",
        "Pioneer Wholesale"
    ],
    "Status": [
        "Shipped",
        "Processing",
        "Delayed",
        "Shipped",
        "Processing"
    ],
    "Order Value": [1250, 890, 2100, 750, 1600]
})

st.divider()

col1, col2, col3 = st.columns(3)

col1.metric("Total Orders", len(orders))
col2.metric(
    "Total Order Value",
    f"${orders['Order Value'].sum():,.2f}"
)
col3.metric(
    "Delayed Orders",
    len(orders[orders["Status"] == "Delayed"])
)

st.subheader("Order Management")

st.dataframe(
    orders,
    use_container_width=True,
    hide_index=True
)
