CREATE TABLE taxi_trips (
    vendorid INTEGER,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count NUMERIC,
    trip_distance NUMERIC,
    ratecodeid NUMERIC,
    store_and_fwd_flag VARCHAR(1),
    pulocationid INTEGER,
    dolocationid INTEGER,
    payment_type INTEGER,
    fare_amount NUMERIC,
    extra NUMERIC,
    mta_tax NUMERIC,
    tip_amount NUMERIC,
    tolls_amount NUMERIC,
    improvement_surcharge NUMERIC,
    total_amount NUMERIC,
    congestion_surcharge NUMERIC,
    airport_fee NUMERIC,
    source_file VARCHAR(100)
);

CREATE TABLE taxi_zones (
    locationid INTEGER PRIMARY KEY,
    borough VARCHAR(50),
    zone VARCHAR(150),
    service_zone VARCHAR(50)
);

CREATE TABLE etl_file_log (
    file_name VARCHAR(100) PRIMARY KEY,
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_count INTEGER
);

SELECT
    column_name,
    data_type
FROM information_schema.columns
WHERE table_name = 'taxi_trips';

ALTER TABLE taxi_trips
ADD COLUMN cbd_congestion_fee NUMERIC;

ALTER TABLE taxi_trips
    ALTER COLUMN source_file TYPE VARCHAR(100);

SELECT 
	source_file,
	COUNT (*) AS records
FROM taxi_trips
GROUP BY source_file
ORDER BY source_file;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'taxi_trips'
ORDER BY column_name;
	