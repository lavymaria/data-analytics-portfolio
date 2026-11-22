CREATE TABLE fact_trip_summary AS
SELECT

pickup_datetime,
dropoff_datetime,

pulocationid,
dolocationid,

payment_type,

trip_distance,

fare_amount,
tip_amount,
total_amount,

EXTRACT(
EPOCH FROM
(dropoff_datetime-pickup_datetime)
)/60
AS trip_duration_minutes,

fare_amount/
NULLIF(trip_distance,0)
AS fare_per_mile,

(tip_amount/
NULLIF(fare_amount,0))*100
AS tip_percentage,

trip_distance/
NULLIF(
EXTRACT(
EPOCH FROM
(dropoff_datetime-pickup_datetime)
)/3600,
0
)
AS speed_mph,

EXTRACT(HOUR FROM pickup_datetime)
AS pickup_hour,

EXTRACT(DOW FROM pickup_datetime)
AS pickup_day,

EXTRACT(MONTH FROM pickup_datetime)
AS pickup_month,

EXTRACT(YEAR FROM pickup_datetime)
AS pickup_year

FROM taxi_trips;

SELECT *
FROM fact_trip_summary
LIMIT 10;
