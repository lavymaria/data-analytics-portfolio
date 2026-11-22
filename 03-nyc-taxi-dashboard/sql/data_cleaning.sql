WITH thresholds AS (
    SELECT
        PERCENTILE_CONT(0.99)
            WITHIN GROUP (ORDER BY fare_amount) AS fare_limit,

        PERCENTILE_CONT(0.99)
            WITHIN GROUP (ORDER BY trip_distance) AS distance_limit

    FROM taxi_trips
)

SELECT COUNT(*)
FROM taxi_trips t
CROSS JOIN thresholds th
WHERE t.fare_amount <= 0
   OR t.trip_distance <= 0
   OR t.fare_amount > th.fare_limit
   OR t.trip_distance > th.distance_limit;

-- Create cleaned table
DROP TABLE IF EXISTS taxi_trips_clean;

CREATE TABLE taxi_trips_clean AS
SELECT *
FROM taxi_trips
WHERE fare_amount > 0
  AND trip_distance > 0
  AND fare_amount <= 82.5
  AND trip_distance <= 21.7;

-- Viewing and deleting Null values
SELECT COUNT(*)
FROM taxi_trips_clean
WHERE pickup_datetime IS NULL
   OR dropoff_datetime IS NULL
   OR fare_amount IS NULL
   OR trip_distance IS NULL;

DELETE FROM taxi_trips_clean
WHERE pickup_datetime IS NULL
   OR dropoff_datetime IS NULL
   OR fare_amount IS NULL
   OR trip_distance IS NULL;

   

--Viewing and Deleting negative time
SELECT COUNT(*)
FROM taxi_trips_clean
WHERE dropoff_datetime < pickup_datetime;
DELETE FROM taxi_trips_clean
WHERE dropoff_datetime < pickup_datetime;

-- Viewing and Deleting duplicates
SELECT
    pickup_datetime,
    dropoff_datetime,
    pulocationid,
    dolocationid,
    trip_distance,
    fare_amount,
    COUNT(*)
FROM taxi_trips
GROUP BY
    pickup_datetime,
    dropoff_datetime,
    pulocationid,
    dolocationid,
    trip_distance,
    fare_amount
HAVING COUNT(*) > 1;

DELETE FROM taxi_trips_clean
WHERE ctid IN (
    SELECT ctid
    FROM (
        SELECT
            ctid,
            ROW_NUMBER() OVER (
                PARTITION BY
                    pickup_datetime,
                    dropoff_datetime,
                    pulocationid,
                    dolocationid,
                    trip_distance,
                    fare_amount
                ORDER BY ctid
            ) AS rn
        FROM taxi_trips
    ) t
    WHERE rn > 1
);
