
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, URL, text

st.set_page_config(
    page_title="OLA Ride Insights",
    page_icon="🚕",
    layout="wide"
)

st.title("🚕 OLA Ride Insights")
# Dashboard Navigation
st.sidebar.title("🚕 OLA Analytics")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overall Dashboard",
        "Vehicle Analysis",
        "Revenue Analysis",
        "Cancellation Analysis",
        "Ratings Analysis"
    ]
)
st.caption("Interactive Ride Booking & Business Analytics Dashboard")

# ---------------- DATABASE CONNECTION ----------------

@st.cache_data(ttl=300)
def load_data(password):
    url = URL.create(
        drivername="mysql+pymysql",
        username="root",
        password=password,
        host="localhost",
        port=3306,
        database="ola_analytics"
    )

    engine = create_engine(url)

    try:
        with engine.connect() as conn:
            df = pd.read_sql(
                text("SELECT * FROM bookings"),
                conn
            )
    finally:
        engine.dispose()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    for col in ["booking_value", "ride_distance",
                "customer_rating", "driver_ratings"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

# ---------------- SIDEBAR ----------------

st.sidebar.header("Database Connection")

password = st.sidebar.text_input(
    "MySQL Root Password",
    type="password"
)

if not password:
    st.info("Enter your MySQL root password in the sidebar to load the dashboard.")
    st.stop()

try:
    df = load_data(password)
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()

st.sidebar.success("MySQL Connected")

# ---------------- FILTERS ----------------

st.sidebar.header("Dashboard Filters")

statuses = sorted(df["booking_status"].dropna().unique())
vehicles = sorted(df["vehicle_type"].dropna().unique())

selected_status = st.sidebar.multiselect(
    "Booking Status",
    statuses,
    default=statuses
)

selected_vehicles = st.sidebar.multiselect(
    "Vehicle Type",
    vehicles,
    default=vehicles
)

min_date = df["date"].min().date()
max_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Booking Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered = df[
    df["booking_status"].isin(selected_status)
    & df["vehicle_type"].isin(selected_vehicles)
].copy()

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[
        filtered["date"].dt.date.between(start_date, end_date)
    ]



if page == "Overall Dashboard":
    st.header("📊 Overall Dashboard")

elif page == "Vehicle Analysis":
    st.header("🚗 Vehicle Performance Analysis")

elif page == "Revenue Analysis":
    st.header("💰 Revenue Analysis")

elif page == "Cancellation Analysis":
    st.header("❌ Cancellation Analysis")

elif page == "Ratings Analysis":
    st.header("⭐ Customer & Driver Ratings")

# ---------------- KPI METRICS ----------------

success = filtered[
    filtered["booking_status"] == "Success"
]

total_bookings = len(filtered)
successful_bookings = len(success)

revenue = success["booking_value"].sum()
avg_distance = success["ride_distance"].mean()

customer_cancel = (
    filtered["booking_status"] == "Canceled by Customer"
).sum()

driver_cancel = (
    filtered["booking_status"] == "Canceled by Driver"
).sum()

c1, c2, c3 = st.columns(3)

c1.metric("Total Bookings", f"{total_bookings:,}")
c2.metric("Successful Bookings", f"{successful_bookings:,}")
c3.metric("Total Revenue", f"₹{revenue:,.0f}")

c4, c5, c6 = st.columns(3)

c4.metric("Customer Cancellations", f"{customer_cancel:,}")
c5.metric("Driver Cancellations", f"{driver_cancel:,}")
c6.metric("Average Ride Distance", f"{avg_distance:.2f} km" if pd.notna(avg_distance) else "N/A")

st.divider()

# ---------------- BOOKING ANALYSIS ----------------

st.subheader("📊 Booking Analysis")

col1, col2 = st.columns(2)

with col1:
    status_data = filtered["booking_status"].value_counts().reset_index()
    status_data.columns = ["Booking Status", "Count"]

    fig = px.pie(
        status_data,
        names="Booking Status",
        values="Count",
        hole=0.45,
        title="Booking Status Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    daily = (
        filtered.groupby(filtered["date"].dt.date)
        .size()
        .reset_index(name="Bookings")
    )
    daily.columns = ["Date", "Bookings"]

    fig = px.line(
        daily,
        x="Date",
        y="Bookings",
        markers=True,
        title="Daily Ride Volume"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- VEHICLE ANALYSIS ----------------

st.subheader("🚕 Vehicle Analysis")

vehicle_data = (
    success.groupby("vehicle_type")
    .agg(
        Total_Rides=("booking_id", "count"),
        Average_Distance=("ride_distance", "mean"),
        Average_Rating=("customer_rating", "mean"),
        Revenue=("booking_value", "sum")
    )
    .reset_index()
)

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        vehicle_data,
        x="vehicle_type",
        y="Total_Rides",
        title="Successful Rides by Vehicle Type",
        text_auto=True
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        vehicle_data,
        x="vehicle_type",
        y="Average_Distance",
        title="Average Ride Distance by Vehicle"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- REVENUE ANALYSIS ----------------

st.subheader("💰 Revenue Analysis")

col1, col2 = st.columns(2)

with col1:
    payment_data = (
        success.groupby("payment_method")["booking_value"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        payment_data,
        names="payment_method",
        values="booking_value",
        hole=0.4,
        title="Revenue by Payment Method"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        vehicle_data,
        x="vehicle_type",
        y="Revenue",
        title="Revenue by Vehicle Type"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- CANCELLATION ANALYSIS ----------------

st.subheader("❌ Cancellation Analysis")

col1, col2 = st.columns(2)

with col1:
    customer_reasons = filtered[
        filtered["booking_status"] == "Canceled by Customer"
    ]["canceled_rides_by_customer"].value_counts().reset_index()

    customer_reasons.columns = ["Reason", "Count"]

    fig = px.bar(
        customer_reasons,
        x="Count",
        y="Reason",
        orientation="h",
        title="Customer Cancellation Reasons"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    driver_reasons = filtered[
        filtered["booking_status"] == "Canceled by Driver"
    ]["canceled_rides_by_driver"].value_counts().reset_index()

    driver_reasons.columns = ["Reason", "Count"]

    fig = px.bar(
        driver_reasons,
        x="Count",
        y="Reason",
        orientation="h",
        title="Driver Cancellation Reasons"
    )
    st.plotly_chart(fig, use_container_width=True)

# ---------------- RATINGS ANALYSIS ----------------

st.subheader("⭐ Ratings Analysis")

rating_data = (
    success.groupby("vehicle_type")
    .agg(
        Customer_Rating=("customer_rating", "mean"),
        Driver_Rating=("driver_ratings", "mean")
    )
    .reset_index()
    .melt(
        id_vars="vehicle_type",
        var_name="Rating Type",
        value_name="Average Rating"
    )
)

fig = px.bar(
    rating_data,
    x="vehicle_type",
    y="Average Rating",
    color="Rating Type",
    barmode="group",
    title="Customer vs Driver Ratings by Vehicle"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- DATA TABLE ----------------

with st.expander("View Booking Records"):
    st.dataframe(filtered, use_container_width=True)

st.caption("OLA Ride Insights | Built with Python, Streamlit, Plotly and MySQL")