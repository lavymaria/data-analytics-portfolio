from pathlib import Path

import pandas as pd

from sqlalchemy import create_engine, text


# =====================================
# DATABASE SETTINGS
# =====================================

DB_USER = "postgres"
DB_PASSWORD = "lavy24"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nyc_taxi"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


# =====================================
# HELPER FUNCTIONS
# =====================================

def standardize_columns(df):
    """
    Standardize NYC Taxi column names to match PostgreSQL table.
    """

    # Convert all column names to lowercase
    df.columns = df.columns.str.lower()

    # Rename datetime columns
    df = df.rename(
        columns={
            "tpep_pickup_datetime": "pickup_datetime",
            "tpep_dropoff_datetime": "dropoff_datetime"
        }
    )

    return df


def get_loaded_files():
    """
    Get list of files already loaded.
    """

    query = """
    SELECT file_name
    FROM etl_file_log
    """

    try:

        df = pd.read_sql(query, engine)

        return set(df["file_name"])

    except Exception:
        return set()


# =====================================
# LOAD FILE LOG
# =====================================

loaded_files = get_loaded_files()


# =====================================
# LOCATE RAW FILES
# =====================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
)

files = sorted(
    RAW_PATH.glob("yellow_tripdata_*.parquet")
)

print(f"Found {len(files)} parquet files")


# =====================================
# PROCESS FILES
# =====================================

for file in files:

    filename = file.name

    # ---------------------------------
    # SKIP ALREADY LOADED FILES
    # ---------------------------------

    if filename in loaded_files:

        print(f"SKIPPING {filename}")

        continue

    print("\n" + "=" * 80)
    print(f"LOADING {filename}")
    print("=" * 80)

    try:

        # ---------------------------------
        # READ PARQUET FILE
        # ---------------------------------

        df = pd.read_parquet(file)

        print(f"Original Shape: {df.shape}")

        # ---------------------------------
        # STANDARDIZE COLUMN NAMES
        # ---------------------------------

        df = standardize_columns(df)
        

        if "request_source" in df.columns:
            df = df.drop(columns=["request_source"])

        # ---------------------------------
        # ADD SOURCE FILE COLUMN
        # ---------------------------------

        df["source_file"] = filename

        # ---------------------------------
        # VALIDATE COLUMN STRUCTURE
        # ---------------------------------

        required_columns = {
            "vendorid",
            "pickup_datetime",
            "dropoff_datetime",
            "passenger_count",
            "trip_distance",
            "ratecodeid",
            "store_and_fwd_flag",
            "pulocationid",
            "dolocationid",
            "payment_type",
            "fare_amount",
            "extra",
            "mta_tax",
            "tip_amount",
            "tolls_amount",
            "improvement_surcharge",
            "total_amount",
            "congestion_surcharge",
            "airport_fee",
            "cbd_congestion_fee",
            "source_file"
        }

        missing = required_columns - set(df.columns)

        if missing:

            raise ValueError(
                f"Missing columns: {missing}"
            )

        print("\nColumns:")
        print(df.columns.tolist())

        rows_loaded = len(df)

        print(f"\nRows to load: {rows_loaded:,}")

        # ---------------------------------
        # LOAD DATA INTO POSTGRESQL
        # ---------------------------------

        df.to_sql(
            name="taxi_trips",
            con=engine,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=5000
        )

        print(f"SUCCESS: Loaded {rows_loaded:,} rows")

        # ---------------------------------
        # RECORD SUCCESSFUL LOAD
        # ---------------------------------

        with engine.begin() as conn:

            conn.execute(
                text(
                    """
                    INSERT INTO etl_file_log
                    (
                        file_name,
                        record_count
                    )
                    VALUES
                    (
                        :file,
                        :count
                    )
                    """
                ),
                {
                    "file": filename,
                    "count": rows_loaded
                }
            )

        print(f"Logged {filename}")

    except Exception as e:

        print("\n" + "=" * 80)
        print(f"FAILED: {filename}")
        print("=" * 80)

        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message:\n{e}")

        raise


# =====================================
# COMPLETE
# =====================================

print("\nETL COMPLETE")