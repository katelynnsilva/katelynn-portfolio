-- Retail Sales & Storefront Performance Analysis
-- Table: retail_sales(week_start, store_id, location, region, channel,
--                      category, units_sold, unit_price, unit_cost, overhead_allocated)

-- 1. Monthly revenue trend
SELECT
    strftime('%Y-%m', week_start) AS month,
    ROUND(SUM(units_sold * unit_price), 2) AS revenue
FROM retail_sales
GROUP BY month
ORDER BY month;

-- 2. Revenue, cost, profit, and margin by store location
SELECT
    location,
    ROUND(SUM(units_sold * unit_price), 2) AS revenue,
    ROUND(SUM(units_sold * unit_cost) + SUM(overhead_allocated), 2) AS total_cost,
    ROUND(SUM(units_sold * unit_price) - (SUM(units_sold * unit_cost) + SUM(overhead_allocated)), 2) AS profit,
    ROUND(
        100.0 * (SUM(units_sold * unit_price) - (SUM(units_sold * unit_cost) + SUM(overhead_allocated)))
        / SUM(units_sold * unit_price), 1
    ) AS margin_pct
FROM retail_sales
GROUP BY location
ORDER BY profit DESC;

-- 3. Top product categories by total profit
SELECT
    category,
    ROUND(SUM(units_sold * unit_price), 2) AS revenue,
    ROUND(SUM(units_sold * unit_price) - (SUM(units_sold * unit_cost) + SUM(overhead_allocated)), 2) AS profit,
    ROUND(
        100.0 * (SUM(units_sold * unit_price) - (SUM(units_sold * unit_cost) + SUM(overhead_allocated)))
        / SUM(units_sold * unit_price), 1
    ) AS margin_pct
FROM retail_sales
GROUP BY category
ORDER BY profit DESC;

-- 4. In-Store vs Online channel comparison
SELECT
    channel,
    ROUND(SUM(units_sold * unit_price), 2) AS revenue,
    SUM(units_sold) AS units_sold,
    ROUND(
        100.0 * (SUM(units_sold * unit_price) - (SUM(units_sold * unit_cost) + SUM(overhead_allocated)))
        / SUM(units_sold * unit_price), 1
    ) AS margin_pct
FROM retail_sales
GROUP BY channel
ORDER BY revenue DESC;

-- 5. Overhead as a percentage of revenue, by store location
SELECT
    location,
    ROUND(SUM(overhead_allocated), 2) AS total_overhead,
    ROUND(SUM(units_sold * unit_price), 2) AS revenue,
    ROUND(100.0 * SUM(overhead_allocated) / SUM(units_sold * unit_price), 1) AS overhead_pct_of_revenue
FROM retail_sales
WHERE channel = 'In-Store'
GROUP BY location
ORDER BY overhead_pct_of_revenue DESC;
