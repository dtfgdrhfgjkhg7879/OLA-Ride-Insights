
import pandas as pd

df = pd.read_excel(
    "OLA_DataSet.xlsx",
    sheet_name="July"
)

# 1. Check unique booking statuses
print("\n--- Booking Status ---")
print(df["Booking_Status"].unique())

# 2. Check cancellation reasons
print("\n--- Customer Cancellation ---")
print(df["Canceled_Rides_by_Customer"].value_counts(dropna=False))

print("\n--- Driver Cancellation ---")
print(df["Canceled_Rides_by_Driver"].value_counts(dropna=False))

# 3. Check incomplete rides
print("\n--- Incomplete Rides ---")
print(df["Incomplete_Rides"].value_counts(dropna=False))

print("\n--- Incomplete Reasons ---")
print(df["Incomplete_Rides_Reason"].value_counts(dropna=False))

# 4. Check payment methods
print("\n--- Payment Methods ---")
print(df["Payment_Method"].value_counts(dropna=False))

# 5. Cross-check booking status and cancellation data
print("\n--- Status vs Customer Cancellation ---")
print(pd.crosstab(
    df["Booking_Status"],
    df["Canceled_Rides_by_Customer"].notna()
))

print("\n--- Status vs Driver Cancellation ---")
print(pd.crosstab(
    df["Booking_Status"],
    df["Canceled_Rides_by_Driver"].notna()
))

# 6. Check zero-distance rides
print("\n--- Zero Distance Rides ---")
print((df["Ride_Distance"] == 0).sum())

print("\n--- Distance by Booking Status ---")
print(df.groupby("Booking_Status")["Ride_Distance"].describe())

print("\nData validation completed!")
