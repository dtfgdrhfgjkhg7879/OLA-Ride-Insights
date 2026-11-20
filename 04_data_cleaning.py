
import pandas as pd
import os

# =====================================
# 1. LOAD DATASET
# =====================================

print("Loading OLA dataset...")

df = pd.read_excel(
    "OLA_DataSet.xlsx",
    sheet_name="July"
)

print("Original Shape:", df.shape)

# =====================================
# 2. STANDARDIZE COLUMN NAMES
# =====================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"[^a-z0-9]+", "_", regex=True)
    .str.strip("_")
)

print("\nStandardized Columns:")
print(df.columns.tolist())


# 3. CLEAN TEXT COLUMNS

for col in df.columns:

    if col == "time":
        continue

    df[col] = df[col].map(
        lambda value: value.strip()
        if isinstance(value, str)
        else value
    )

    df[col] = df[col].replace("", pd.NA)

# =====================================
# 4. REMOVE DUPLICATE ROWS
# =====================================

before = len(df)

df = df.drop_duplicates()

after = len(df)

print("\nDuplicate Rows Removed:", before - after)

# =====================================
# 5. CONVERT DATA TYPES
# =====================================

df["date"] = pd.to_datetime(
    df["date"],
    errors="coerce"
)

numeric_columns = [
    "v_tat",
    "c_tat",
    "booking_value",
    "ride_distance",
    "driver_ratings",
    "customer_rating"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

# Standardize time format
parsed_time = pd.to_datetime(
    df["time"].astype("string"),
    format="%H:%M:%S",
    errors="coerce"
)

df["time"] = parsed_time.dt.strftime("%H:%M:%S")

# Create combined ride datetime
df["ride_datetime"] = pd.to_datetime(
    df["date"].dt.strftime("%Y-%m-%d")
    + " "
    + df["time"].astype("string"),
    errors="coerce"
)

# =====================================
# 6. VALIDATE NUMERICAL VALUES
# =====================================

print("\n--- Invalid Value Checks ---")

print(
    "Negative Booking Values:",
    (df["booking_value"] < 0).sum()
)

print(
    "Negative Ride Distances:",
    (df["ride_distance"] < 0).sum()
)

print(
    "Invalid Driver Ratings:",
    (~df["driver_ratings"].between(1, 5) &
     df["driver_ratings"].notna()).sum()
)

print(
    "Invalid Customer Ratings:",
    (~df["customer_rating"].between(1, 5) &
     df["customer_rating"].notna()).sum()
)

print(
    "Duplicate Booking IDs:",
    df["booking_id"].duplicated().sum()
)

# =====================================
# 7. VERIFY BOOKING STATUS
# =====================================

print("\n--- Booking Status Summary ---")

print(df["booking_status"].value_counts(dropna=False))

# =====================================
# 8. VERIFY MISSING VALUES
# =====================================

print("\n--- Missing Values After Cleaning ---")

print(df.isnull().sum())

# =====================================
# 9. SAVE CLEANED DATASET
# =====================================

os.makedirs("data/processed", exist_ok=True)

output_path = "data/processed/ola_cleaned.csv"

df.to_csv(output_path, index=False)

print("\n================================")
print("DATA CLEANING COMPLETED")
print("================================")

print("Final Shape:", df.shape)
print("Output File:", output_path)
