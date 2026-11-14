from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine,text

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
# GET ALREADY LOADED FILES
# =====================================

def get_loaded_files():

    query = """
    SELECT file_name
    FROM etl_file_log
    """

    try:
        df = pd.read_sql(query,engine)
        return set(df["file_name"])

    except:
        return set()


loaded_files = get_loaded_files()

# =====================================
# READ RAW FILES
# =====================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

raw_path = (
    PROJECT_ROOT /
    "data" /
    "raw"
)

files = sorted(
    raw_path.glob("yellow_tripdata_*.parquet")
)

# =====================================
# PROCESS FILES
# =====================================

for file in files:

    filename = file.name

    if filename in loaded_files:

        print(f"SKIPPING {filename}")
        continue

    print(f"LOADING {filename}")

    df = pd.read_parquet(file)

    df.columns = df.columns.str.lower()

    rename_map = {
        "tpep_pickup_datetime":"pickup_datetime",
        "tpep_dropoff_datetime":"dropoff_datetime"
    }

    df.rename(
        columns=rename_map,
        inplace=True
    )

    df["source_file"] = filename

    rows_loaded = len(df)

try:
        df.to_sql(
        "taxi_trips",
        engine,
        if_exists="append",
        index=False,
        method="multi",
        chunksize=50000
    )
except Exception as e:
    print("\nLOAD FAILED")
    print(type(e))
    print(e)
    raise

with engine.begin() as conn:

        conn.execute(
            text("""
            INSERT INTO etl_file_log
            (file_name, record_count)
            VALUES (:file,:count)
            """),
            {
                "file":filename,
                "count":rows_loaded
            }
        )

print(
        f"{rows_loaded:,} rows loaded"
    )

print("ETL COMPLETE")