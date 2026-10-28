-- ============================================================
-- NOVA CORPORATION
-- BR001 - RAW ANALYTICAL EXTRACTION
-- ============================================================
-- Purpose:
-- Build the reproducible raw analytical population required
-- for the Executive Performance Review.
--
-- Grain:
-- One product line within one customer order.
--
-- Period:
-- H1 2025 and H1 2026.
--
-- Design Decision:
-- LEFT JOIN is used to preserve the fact_sales population.
-- Missing dimensional matches must remain observable for
-- subsequent data-quality assessment.
-- ============================================================


SELECT
    -- Transaction identifiers
    fact_sales.sales_line_id,
    fact_sales.order_id,
    fact_sales.order_date,

    -- Date attributes
    dim_date.year,
    dim_date.half_year,
    dim_date.quarter,
    dim_date.month_number,
    dim_date.month_name,
    dim_date.year_month,

    -- Customer
    fact_sales.customer_id,
    dim_customer.customer_name,
    dim_customer.customer_segment,

    -- Product
    fact_sales.product_id,
    dim_product.product_name,
    dim_product.category,
    dim_product.subcategory,
    dim_product.brand,

    -- Channel
    fact_sales.channel_id,
    dim_channel.channel_name,
    dim_channel.channel_group,
    dim_channel.is_digital,

    -- Geography
    fact_sales.region_id,
    dim_region.country AS market_country,
    dim_region.region_name,
    dim_region.market_tier,

    -- Commercial measures
    fact_sales.quantity,
    fact_sales.unit_price,
    fact_sales.unit_cost,
    fact_sales.discount_pct,
    fact_sales.gross_revenue,
    fact_sales.discount_amount,
    fact_sales.net_revenue,
    fact_sales.total_cost,
    fact_sales.gross_profit,

    -- Transaction attributes
    fact_sales.payment_method,
    fact_sales.order_status

FROM fact_sales

LEFT JOIN dim_customer
    ON fact_sales.customer_id = dim_customer.customer_id

LEFT JOIN dim_product
    ON fact_sales.product_id = dim_product.product_id

LEFT JOIN dim_channel
    ON fact_sales.channel_id = dim_channel.channel_id

LEFT JOIN dim_region
    ON fact_sales.region_id = dim_region.region_id

LEFT JOIN dim_date
    ON fact_sales.order_date = dim_date.full_date

WHERE
       fact_sales.order_date BETWEEN '2025-01-01' AND '2025-06-30'
    OR fact_sales.order_date BETWEEN '2026-01-01' AND '2026-06-30'

ORDER BY
    fact_sales.order_date,
    fact_sales.order_id,
    fact_sales.sales_line_id;