-- highest revenue borough
SELECT

z.borough,

SUM(f.total_amount)
AS revenue

FROM fact_trip_summary f

JOIN taxi_zones z

ON f.pulocationid = z.locationid

GROUP BY z.borough

ORDER BY revenue DESC;

-- busiest pickup hour
SELECT

pickup_hour,

COUNT(*)

FROM fact_trip_summary

GROUP BY pickup_hour

ORDER BY 2 DESC;

-- average tip by payment type
SELECT

payment_type,

AVG(tip_percentage)

FROM fact_trip_summary

GROUP BY payment_type;
