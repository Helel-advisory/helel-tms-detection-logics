-- HELEL Oversight & Compliance Advisory
-- SQL Detection Logic: Corridor Velocity Spike Detection

SELECT 
    t.customer_id,
    t.destination_country,
    COUNT(t.transaction_id) AS txn_count_24h,
    SUM(t.amount_usd) AS total_volume_24h,
    b.avg_daily_volume,
    ROUND((SUM(t.amount_usd) / NULLIF(b.avg_daily_volume, 0)) * 100, 2) AS velocity_percentage
FROM transactions t
JOIN (
    SELECT 
        customer_id, 
        destination_country, 
        AVG(daily_total) AS avg_daily_volume
    FROM (
        SELECT customer_id, destination_country, DATE(created_at) as dt, SUM(amount_usd) as daily_total
        FROM transactions
        WHERE created_at >= NOW() - INTERVAL '30 DAYS'
        GROUP BY customer_id, destination_country, DATE(created_at)
    ) hist
    GROUP BY customer_id, destination_country
) b ON t.customer_id = b.customer_id AND t.destination_country = b.destination_country
WHERE t.created_at >= NOW() - INTERVAL '24 HOURS'
GROUP BY t.customer_id, t.destination_country, b.avg_daily_volume
HAVING SUM(t.amount_usd) >= 2.5 * b.avg_daily_volume 
   AND SUM(t.amount_usd) >= 15000;
