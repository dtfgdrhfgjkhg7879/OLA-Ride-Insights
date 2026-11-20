
import pandas as pd

# Load Excel dataset
file_path = "OLA_DataSet.xlsx"

df = pd.read_excel(file_path, sheet_name="July")

# 1. Dataset dimensions
print("Dataset Shape:", df.shape)

# 2. First five records
print("\nFirst 5 Records:")
print(df.head())

# 3. Column information
print("\nDataset Information:")
print(df.info())

# 4. Missing values
print("\nMissing Values:")
print(df.isnull().sum())

# 5. Duplicate records
print("\nDuplicate Records:", df.duplicated().sum())

# 6. Booking status
print("\nBooking Status:")
print(df["Booking_Status"].value_counts())

# 7. Vehicle types
print("\nVehicle Types:")
print(df["Vehicle_Type"].value_counts())

# 8. Numerical summary
print("\nStatistical Summary:")
print(df.describe())

print("\nStep 1 Completed!")
