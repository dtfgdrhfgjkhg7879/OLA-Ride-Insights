# OLA Ride Insights — Data Analytics Project

## 1. Project Overview

OLA Ride Insights is a data analytics project designed to analyze ride-booking data and identify meaningful business insights related to ride performance, customer behavior, revenue generation, cancellations, vehicle performance, and customer satisfaction.

The project uses Python, SQL, Power BI, and Streamlit to transform raw ride-booking data into actionable business insights through interactive dashboards and visualizations.

## 2. Project Objectives

- Analyze overall ride-booking performance.
- Identify successful and unsuccessful bookings.
- Evaluate vehicle-wise ride performance.
- Analyze revenue and payment methods.
- Understand customer and driver cancellation patterns.
- Evaluate customer and driver ratings.
- Develop interactive dashboards for business analysis.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| MySQL | Data storage and SQL analysis |
| Power BI | Interactive business dashboards |
| Streamlit | Web-based analytics application |
| Plotly | Interactive charts |
| SQLAlchemy | Python–MySQL connectivity |

## 4. Dataset Description

The project uses an OLA ride-booking dataset containing:

- Total records: 103,024
- Original columns: 20
- Processed columns: 21
- Data period: July 2024

Important attributes include:

- Booking ID
- Booking Status
- Customer ID
- Vehicle Type
- Pickup Location
- Drop Location
- Booking Value
- Payment Method
- Ride Distance
- Driver Ratings
- Customer Rating
- Cancellation Reasons

## 5. Project Workflow

### Phase 1: Data Understanding
- Dataset inspection
- Data types analysis
- Missing value analysis
- Duplicate record checking
- Statistical summaries

### Phase 2: Data Validation and Cleaning
- Data validation
- Missing value investigation
- Duplicate checking
- Date and time conversion
- Column name standardization
- Numeric data validation

### Phase 3: Exploratory Data Analysis
- Booking status distribution
- Vehicle type analysis
- Revenue analysis
- Payment method analysis
- Cancellation analysis
- Customer and driver rating analysis

### Phase 4: SQL Analysis

Ten business questions were analyzed using MySQL:

1. Retrieve successful bookings.
2. Calculate average ride distance by vehicle type.
3. Count customer-cancelled rides.
4. Identify the top five customers by ride count.
5. Analyze driver cancellations due to personal or car-related issues.
6. Find maximum and minimum driver ratings for Prime Sedan.
7. Retrieve UPI bookings.
8. Calculate average customer ratings by vehicle type.
9. Calculate total booking value of successful rides.
10. Identify incomplete rides and their reasons.

### Phase 5: Power BI Dashboard

Five dashboard pages were designed:

1. Overall Dashboard
2. Vehicle Type Analysis
3. Revenue Analysis
4. Cancellation Analysis
5. Ratings Analysis

### Phase 6: Streamlit Application

An interactive web application was developed using Streamlit and Plotly.

Features include:
- MySQL database connectivity
- Interactive KPI cards
- Booking status analysis
- Daily ride volume
- Vehicle performance analysis
- Revenue analysis
- Cancellation analysis
- Ratings analysis
- Interactive filters

## 6. Key Analytical Findings

| Metric | Result |
|---|---:|
| Total Bookings | 103,024 |
| Successful Bookings | 63,967 |
| Customer Cancellations | 10,499 |
| Driver Cancellations | 18,434 |
| Driver Not Found | 10,124 |
| Incomplete Rides | 3,926 |
| Successful Booking Revenue | ₹35,080,467 |
| Average Successful Ride Distance | 22.85 km |
| Average Customer Rating | 4.0 |
| Average Driver Rating | 4.0 |

## 7. Database Details

Database: `ola_analytics`

Main table: `bookings`

Total imported records: 103,024

The cleaned dataset was imported into MySQL using Python, SQLAlchemy, and PyMySQL.

## 8. Project Structure

```text
Ola Pro/
│
├── data/
│   └── processed/
│       └── ola_cleaned.csv
│
├── reports/
│   └── eda/
│
├── 01_data_understanding.py
├── 02_data_validation.py
├── 03_incomplete_analysis.py
├── 04_data_cleaning.py
├── 05_eda.py
├── 06_import_mysql.py
├── 07_ola_sql_analysis.sql
├── app.py
├── Ola_Ride_Insights.pbix
└── README.md
```

## 9. How to Run the Application

### Step 1: Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Ola-Pro
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

```bash
pip install pandas numpy matplotlib seaborn streamlit plotly sqlalchemy pymysql
```

### Step 5: Configure MySQL

Create the database:

```sql
CREATE DATABASE ola_analytics;
```

Import the cleaned dataset into the `bookings` table using the provided import script.

Configure database credentials securely using environment variables or Streamlit secrets.

### Step 6: Run Streamlit

```bash
python -m streamlit run app.py
```

## 10. Conclusion

OLA Ride Insights demonstrates an end-to-end data analytics workflow, covering data cleaning, exploratory data analysis, SQL querying, business intelligence dashboards, and interactive web application development.

The project provides insights into ride-booking trends, vehicle performance, revenue generation, cancellation behavior, and customer satisfaction.

## 11. Future Enhancements

- Real-time ride analytics.
- Predictive ride demand analysis.
- Revenue forecasting.
- Customer segmentation.
- Advanced cancellation prediction.
- Cloud deployment.
- Automated data refresh.

## 12. Author

**Project:** OLA Ride Insights  
**Domain:** Data Analytics and Business Intelligence  
**Technologies:** Python, MySQL, Power BI, Streamlit