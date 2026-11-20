
import pandas as pd
from sqlalchemy import create_engine, URL, text
from getpass import getpass
import traceback
import os

def main():
    engine = None

    try:
        print("STEP 1: Starting import...", flush=True)

        password = getpass("Enter MySQL root password: ")

        print("STEP 2: Creating connection using PyMySQL...", flush=True)

        connection_url = URL.create(
            drivername="mysql+pymysql",
            username="root",
            password=password,
            host="127.0.0.1",
            port=3306,
            database="ola_analytics"
        )

        engine = create_engine(
            connection_url,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10}
        )

        print("STEP 3: Connecting to MySQL...", flush=True)

        with engine.connect() as conn:
            db = conn.execute(
                text("SELECT DATABASE()")
            ).scalar()

            print("Connected successfully:", db, flush=True)

        csv_path = "data/processed/ola_cleaned.csv"

        if not os.path.exists(csv_path):
            raise FileNotFoundError(csv_path)

        print("STEP 4: Loading CSV...", flush=True)

        df = pd.read_csv(csv_path)

        print("Dataset shape:", df.shape, flush=True)

        for column in ["date", "ride_datetime"]:
            if column in df.columns:
                df[column] = pd.to_datetime(
                    df[column], errors="coerce"
                )

        print("STEP 5: Importing data...", flush=True)

        df.to_sql(
            "bookings",
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=500
        )

        print("STEP 6: Verifying import...", flush=True)

        with engine.connect() as conn:
            count = conn.execute(
                text("SELECT COUNT(*) FROM bookings")
            ).scalar()

        print("Imported records:", count, flush=True)

        if count == len(df):
            print("SUCCESS: All records imported!", flush=True)
        else:
            print("WARNING: Record count mismatch!", flush=True)

    except Exception as error:
        print("\nIMPORT FAILED:", error, flush=True)
        traceback.print_exc()

    finally:
        if engine is not None:
            engine.dispose()

        print("Script finished.", flush=True)


if __name__ == "__main__":
    main()
