from pathlib import Path
import requests

# ==========================================
# PROJECT PATHS
# ==========================================

# Location of project root:
# 03-nyc-taxi-dashboard/

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw"

RAW_DATA_PATH.mkdir(
    parents=True,
    exist_ok=True
)

# ==========================================
# DOWNLOAD SETTINGS
# ==========================================

START_YEAR = 2025
START_MONTH = 1

END_YEAR = 2026
END_MONTH = 8

BASE_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data"
)

# ==========================================
# GENERATE MONTHS
# ==========================================

months = []

year = START_YEAR
month = START_MONTH

while (
    year < END_YEAR
    or
    (year == END_YEAR and month <= END_MONTH)
):

    months.append(
        f"{year}-{month:02d}"
    )

    month += 1

    if month > 12:
        month = 1
        year += 1

# ==========================================
# DOWNLOAD FILES
# ==========================================

for month in months:

    filename = (
        f"yellow_tripdata_{month}.parquet"
    )

    url = (
        f"{BASE_URL}/{filename}"
    )

    local_file = (
        RAW_DATA_PATH / filename
    )

    if local_file.exists():

        print(
            f"✓ Already downloaded: {filename}"
        )
        continue

    print(
        f"\nDownloading {filename}"
    )

    try:

        response = requests.get(
            url,
            stream=True,
            timeout=(30, 300)
        )

        if response.status_code == 200:

            with open(local_file, "wb") as f:

                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):

                    if chunk:
                        f.write(chunk)

            file_size = round(
                local_file.stat().st_size /
                (1024 * 1024),
                2
            )

            print(
                f"✓ Downloaded ({file_size} MB)"
            )

        else:

            print(
                f"✗ File not available: {filename}"
            )

    except requests.exceptions.ReadTimeout:

        print(
            f"✗ Read timeout: {filename}"
        )

    except requests.exceptions.ConnectTimeout:

        print(
            f"✗ Connection timeout: {filename}"
        )

    except Exception as e:

        print(
            f"✗ Error: {e}"
        )

print("\nDownload process completed.")