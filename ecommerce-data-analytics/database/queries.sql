-- =============================================
-- Useful SQL Queries for E-Commerce Analysis
-- =============================================

-- 1. Total Sales by Month
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') as month,
    COUNT(DISTINCT o.order_id) as total_orders,
    ROUND(SUM(oi.quantity * oi.item_price * (1 - oi.discount_pct/100)), 2) as total_revenue
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY month
ORDER BY month DESC;

-- 2. Top 10 Best Selling Products
SELECT 
    p.product_name,
    SUM(oi.quantity) as total_quantity_sold,
    ROUND(SUM(oi.quantity * oi.item_price * (1 - oi.discount_pct/100)), 2) as total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
ORDER BY total_quantity_sold DESC
LIMIT 10;

-- 3. Customer Lifetime Value
SELECT 
    c.customer_id,
    c.first_name,
    c.last_name,
    COUNT(DISTINCT o.order_id) as order_count,
    ROUND(SUM(oi.quantity * oi.item_price * (1 - oi.discount_pct/100)), 2) as total_spent
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'Completed'
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_spent DESC;

-- 4. Return Rate by Category
SELECT 
    cat.category_name,
    COUNT(DISTINCT oi.order_item_id) as total_items_sold,
    COUNT(DISTINCT r.return_id) as total_returns,
    ROUND(COUNT(DISTINCT r.return_id) * 100.0 / COUNT(DISTINCT oi.order_item_id), 2) as return_rate
FROM categories cat
JOIN products p ON cat.category_id = p.category_id
JOIN order_items oi ON p.product_id = oi.product_id
LEFT JOIN returns r ON oi.order_item_id = r.order_item_id
GROUP BY cat.category_id, cat.category_name
ORDER BY return_rate DESC;

-- 5. Daily Order Trend (Last 30 Days)
SELECT 
    DATE(order_date) as order_day,
    COUNT(*) as orders,
    COUNT(DISTINCT customer_id) as unique_customers
FROM orders
WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY DATE(order_date)
ORDER BY order_day DESC;