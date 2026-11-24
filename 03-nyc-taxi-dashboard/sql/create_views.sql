-- daily metrics view
CREATE OR REPLACE VIEW vw_daily_metrics AS

SELECT

DATE(pickup_datetime)
AS trip_date,

COUNT(*) AS total_trips,

ROUND(CAST(SUM(total_amount) AS NUMERIC), 2)
AS revenue,

ROUND(CAST(AVG(fare_amount) AS NUMERIC), 2)
AS avg_fare,

ROUND(CAST(AVG(trip_distance) AS NUMERIC), 2)
AS avg_distance

FROM fact_trip_summary

GROUP BY 1;

-- hourly demand view
CREATE OR REPLACE VIEW vw_hourly_demand AS

SELECT

pickup_hour,

COUNT(*) trips,

ROUND(SUM(total_amount)::NUMERIC, 2) AS
revenue

FROM fact_trip_summary

GROUP BY pickup_hour;

-- zone revenue view
CREATE OR REPLACE VIEW vw_zone_revenue AS

SELECT

z.zone,

z.borough,

COUNT(*) trips,

ROUND(SUM(f.total_amount)::NUMERIC, 2) AS
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


SELECT *
FROM vw_hourly_demand
LIMIT 10;


SELECT *
FROM vw_daily_metrics
LIMIT 10;

SELECT COUNT(*)
FROM vw_daily_metrics;

SELECT COUNT(*)
FROM vw_hourly_demand;

SELECT COUNT(*)
FROM vw_zone_revenue;

SELECT
column_name,
data_type
FROM information_schema.columns
WHERE table_name = 'vw_daily_metrics';


SELECT
column_name,
data_type
FROM information_schema.columns
WHERE table_name = 'vw_hourly_demand';

SELECT
column_name,
data_type
FROM information_schema.columns
WHERE table_name = 'vw_zone_revenue';

-- monthly revenue view
CREATE OR REPLACE VIEW vw_monthly_revenue AS

SELECT

pickup_year,
pickup_month,

COUNT(*) AS total_trips,

ROUND(SUM(total_amount)::NUMERIC, 2) AS total_revenue,

ROUND(AVG(fare_amount)::NUMERIC, 2) AS avg_fare,

ROUND(AVG(tip_amount)::NUMERIC, 2) AS avg_tip

FROM fact_trip_summary

GROUP BY

pickup_year,
pickup_month

ORDER BY

pickup_year,
pickup_month;

SELECT *
FROM vw_monthly_revenue;


-- borough revenue view
CREATE OR REPLACE VIEW vw_borough_revenue AS

SELECT

z.borough,

COUNT(*) AS trips,

ROUND(SUM(f.total_amount)::NUMERIC, 2) AS revenue,

ROUND(AVG(f.trip_distance)::NUMERIC, 2) AS avg_distance,

ROUND(AVG(f.tip_percentage)::NUMERIC, 2) AS avg_tip_pct

FROM fact_trip_summary f

JOIN taxi_zones z

ON f.pulocationid = z.locationid

GROUP BY z.borough;

SELECT *
FROM vw_borough_revenue;


-- top pickup zones view
CREATE OR REPLACE VIEW vw_top_pickups AS

SELECT

z.zone,

z.borough,

COUNT(*) AS trip_count

FROM fact_trip_summary f

JOIN taxi_zones z

ON f.pulocationid = z.locationid

GROUP BY

z.zone,
z.borough;

SELECT *
FROM vw_top_pickups