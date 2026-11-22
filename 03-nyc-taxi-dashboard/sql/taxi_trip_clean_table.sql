DROP TABLE IF EXISTS taxi_trips_clean;

CREATE TABLE taxi_trips_clean AS
SELECT *
FROM taxi_trips
WHERE fare_amount > 0
  AND trip_distance > 0
  AND fare_amount <= 82.5
  AND trip_distance <= 21.7;