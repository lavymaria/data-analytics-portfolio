-- daily metrics view
CREATE OR REPLACE VIEW vw_daily_metrics AS

SELECT

DATE(pickup_datetime)
AS trip_date,

COUNT(*) AS total_trips,

SUM(total_amount)
AS revenue,

AVG(fare_amount)
AS avg_fare,

AVG(trip_distance)
AS avg_distance

FROM fact_trip_summary

GROUP BY 1;

-- hourly demand view
CREATE OR REPLACE VIEW vw_hourly_demand AS

SELECT

pickup_hour,

COUNT(*) trips,

SUM(total_amount)
revenue

FROM fact_trip_summary

GROUP BY pickup_hour;

-- zone revenue view
CREATE OR REPLACE VIEW vw_zone_revenue AS

SELECT

z.zone,

z.borough,

COUNT(*) trips,

SUM(f.total_amount)
revenue

FROM fact_trip_summary f

JOIN taxi_zones z

ON z.locationid =
f.pulocationid

GROUP BY
z.zone,
z.borough;

SELECT COUNT(*)
FROM fact_trip_summary f
JOIN taxi_zones z
ON z.locationid = f.pulocationid;

SELECT *
FROM vw_zone_revenue
LIMIT 10;

