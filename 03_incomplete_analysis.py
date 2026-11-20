
import pandas as pd

df = pd.read_excel("OLA_DataSet.xlsx", sheet_name="July")

print("\n--- Booking Status vs Incomplete Rides ---")
print(pd.crosstab(
    df["Booking_Status"],
    df["Incomplete_Rides"],
    dropna=False
))

print("\n--- Incomplete Ride Reasons by Status ---")
print(pd.crosstab(
    df["Booking_Status"],
    df["Incomplete_Rides_Reason"],
    dropna=False
))

print("\n--- Booking Value by Status ---")
print(df.groupby("Booking_Status")["Booking_Value"].describe())

print("\nAnalysis completed!")
