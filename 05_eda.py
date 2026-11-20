
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# 1. LOAD CLEANED DATA
# ==========================================

print("Loading cleaned OLA dataset...")

df = pd.read_csv(
    "data/processed/ola_cleaned.csv",
    parse_dates=["date", "ride_datetime"]
)

# Create output directory
output_dir = "reports/eda"
os.makedirs(output_dir, exist_ok=True)

sns.set_theme(style="whitegrid")

print("Dataset Shape:", df.shape)

# Only successful rides for completed-ride metrics
successful = df[df["booking_status"] == "Success"].copy()

# ==========================================
# 2. KPI SUMMARY
# ==========================================

total_bookings = len(df)
successful_bookings = len(successful)
cancelled_bookings = df["booking_status"].isin(
    ["Canceled by Driver", "Canceled by Customer"]
).sum()

total_revenue = successful["booking_value"].sum()
avg_distance = successful["ride_distance"].mean()
avg_customer_rating = successful["customer_rating"].mean()
avg_driver_rating = successful["driver_ratings"].mean()

print("\n========== OLA BUSINESS KPIs ==========")
print("Total Bookings:", total_bookings)
print("Successful Bookings:", successful_bookings)
print("Customer/Driver Cancellations:", cancelled_bookings)
print("Completed Booking Value:", total_revenue)
print("Average Ride Distance:", round(avg_distance, 2))
print("Average Customer Rating:", round(avg_customer_rating, 2))
print("Average Driver Rating:", round(avg_driver_rating, 2))

# Save KPI summary
kpis = pd.DataFrame({
    "Metric": [
        "Total Bookings",
        "Successful Bookings",
        "Customer/Driver Cancellations",
        "Completed Booking Value",
        "Average Ride Distance",
        "Average Customer Rating",
        "Average Driver Rating"
    ],
    "Value": [
        total_bookings,
        successful_bookings,
        cancelled_bookings,
        total_revenue,
        avg_distance,
        avg_customer_rating,
        avg_driver_rating
    ]
})

kpis.to_csv(f"{output_dir}/kpi_summary.csv", index=False)

# ==========================================
# 3. RIDE VOLUME OVER TIME
# ==========================================

daily_rides = df.groupby("date").size()

plt.figure(figsize=(12, 5))
daily_rides.plot(kind="line", marker="o")

plt.title("Daily Ride Volume")
plt.xlabel("Date")
plt.ylabel("Total Bookings")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(f"{output_dir}/daily_ride_volume.png")
plt.close()

# ==========================================
# 4. BOOKING STATUS BREAKDOWN
# ==========================================

plt.figure(figsize=(9, 5))

sns.countplot(
    data=df,
    x="booking_status",
    order=df["booking_status"].value_counts().index
)

plt.title("Booking Status Distribution")
plt.xlabel("Booking Status")
plt.ylabel("Number of Bookings")
plt.xticks(rotation=25)
plt.tight_layout()

plt.savefig(f"{output_dir}/booking_status.png")
plt.close()

# ==========================================
# 5. TOP 5 VEHICLE TYPES BY RIDE DISTANCE
# ==========================================

vehicle_distance = (
    successful.groupby("vehicle_type")["ride_distance"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

plt.figure(figsize=(9, 5))
vehicle_distance.sort_values().plot(kind="barh")

plt.title("Top 5 Vehicle Types by Total Ride Distance")
plt.xlabel("Total Distance (km)")
plt.ylabel("Vehicle Type")
plt.tight_layout()

plt.savefig(f"{output_dir}/top_vehicle_distance.png")
plt.close()

# ==========================================
# 6. AVERAGE CUSTOMER RATINGS
# ==========================================

rating_data = successful.groupby(
    "vehicle_type"
)["customer_rating"].mean().sort_values()

plt.figure(figsize=(9, 5))
rating_data.plot(kind="bar")

plt.title("Average Customer Rating by Vehicle Type")
plt.xlabel("Vehicle Type")
plt.ylabel("Average Rating")
plt.ylim(0, 5)
plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(f"{output_dir}/customer_ratings.png")
plt.close()

# ==========================================
# 7. CUSTOMER CANCELLATION REASONS
# ==========================================

customer_cancel = (
    df["canceled_rides_by_customer"]
    .dropna()
    .value_counts()
)

plt.figure(figsize=(10, 5))
customer_cancel.plot(kind="bar")

plt.title("Customer Cancellation Reasons")
plt.xlabel("Reason")
plt.ylabel("Number of Cancellations")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig(f"{output_dir}/customer_cancellations.png")
plt.close()

# ==========================================
# 8. DRIVER CANCELLATION REASONS
# ==========================================

driver_cancel = (
    df["canceled_rides_by_driver"]
    .dropna()
    .value_counts()
)

plt.figure(figsize=(10, 5))
driver_cancel.plot(kind="bar")

plt.title("Driver Cancellation Reasons")
plt.xlabel("Reason")
plt.ylabel("Number of Cancellations")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig(f"{output_dir}/driver_cancellations.png")
plt.close()

# ==========================================
# 9. REVENUE BY PAYMENT METHOD
# ==========================================

payment_revenue = (
    successful.groupby("payment_method")["booking_value"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))
payment_revenue.plot(kind="bar")

plt.title("Revenue by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Completed Booking Value")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig(f"{output_dir}/payment_revenue.png")
plt.close()

# ==========================================
# 10. TOP 5 CUSTOMERS BY BOOKING VALUE
# ==========================================

top_customers = (
    successful.groupby("customer_id")["booking_value"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

top_customers.to_csv(
    f"{output_dir}/top_5_customers.csv"
)

plt.figure(figsize=(9, 5))
top_customers.sort_values().plot(kind="barh")

plt.title("Top 5 Customers by Booking Value")
plt.xlabel("Total Booking Value")
plt.ylabel("Customer ID")
plt.tight_layout()

plt.savefig(f"{output_dir}/top_customers.png")
plt.close()

# ==========================================
# 11. RIDE DISTANCE DISTRIBUTION
# ==========================================

plt.figure(figsize=(9, 5))

sns.histplot(
    successful["ride_distance"],
    bins=25,
    kde=True
)

plt.title("Ride Distance Distribution")
plt.xlabel("Ride Distance (km)")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(f"{output_dir}/ride_distance_distribution.png")
plt.close()

# ==========================================
# 12. DRIVER RATINGS DISTRIBUTION
# ==========================================

plt.figure(figsize=(9, 5))

sns.histplot(
    successful["driver_ratings"].dropna(),
    bins=10,
    kde=True
)

plt.title("Driver Ratings Distribution")
plt.xlabel("Driver Rating")
plt.ylabel("Frequency")
plt.tight_layout()

plt.savefig(f"{output_dir}/driver_ratings_distribution.png")
plt.close()

# ==========================================
# 13. CUSTOMER VS DRIVER RATINGS
# ==========================================

rating_comparison = pd.DataFrame({
    "Customer Rating": successful["customer_rating"],
    "Driver Rating": successful["driver_ratings"]
})

rating_comparison = rating_comparison.melt(
    var_name="Rating Type",
    value_name="Rating"
)

plt.figure(figsize=(8, 5))

sns.boxplot(
    data=rating_comparison,
    x="Rating Type",
    y="Rating"
)

plt.title("Customer vs Driver Ratings")
plt.tight_layout()

plt.savefig(f"{output_dir}/rating_comparison.png")
plt.close()

# ==========================================
# 14. INCOMPLETE RIDE REASONS
# ==========================================

incomplete_reasons = (
    df["incomplete_rides_reason"]
    .dropna()
    .value_counts()
)

incomplete_reasons.to_csv(
    f"{output_dir}/incomplete_ride_reasons.csv"
)

# ==========================================
# 15. EXPORT ANALYSIS TABLES
# ==========================================

vehicle_distance.to_csv(
    f"{output_dir}/vehicle_distance.csv"
)

payment_revenue.to_csv(
    f"{output_dir}/payment_revenue.csv"
)

customer_cancel.to_csv(
    f"{output_dir}/customer_cancellation.csv"
)

driver_cancel.to_csv(
    f"{output_dir}/driver_cancellation.csv"
)

# ==========================================
# COMPLETION
# ==========================================

print("\n================================")
print("EDA COMPLETED SUCCESSFULLY")
print("================================")

print("Total charts generated: 11")
print("Reports saved in:", output_dir)

print("\nTop 5 Customers:")
print(top_customers)

print("\nTop Vehicle Types:")
print(vehicle_distance)

print("\nRevenue by Payment Method:")
print(payment_revenue)
