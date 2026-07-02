-- Query 1: Monthly Revenue Trend
SELECT 
    strftime('%Y-%m', order_date) AS month,
    SUM(total_amount) AS total_revenue,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month

-- Query 2: On-Time Delivery Rate
SELECT 
    COUNT(*) AS total_orders,
    SUM(CASE WHEN actual_delivery <= expected_delivery THEN 1 ELSE 0 END) AS on_time_orders,
    ROUND(SUM(CASE WHEN actual_delivery <= expected_delivery THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS on_time_percentage
FROM orders
WHERE status = 'delivered'

-- Query 3: Overdue Invoices by Segment
SELECT c.segment, COUNT(*) AS overdue_count
FROM invoices i
JOIN orders o ON i.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE i.status = 'overdue'
GROUP BY c.segment
ORDER BY overdue_count DESC

-- Query 4: Top 10 Products by Revenue
SELECT p.name AS product_name, 
       SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.name
ORDER BY total_revenue DESC
LIMIT 10

-- Query 5: Products to Reorder
SELECT name, category, stock_quantity, reorder_level
FROM products
WHERE stock_quantity <= reorder_level
ORDER BY stock_quantity ASC

-- Query 6: Customer Lifetime Value
SELECT c.name, c.segment, c.region, COUNT(o.order_id) AS total_orders, SUM(o.total_amount) AS lifetime_value
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.segment, c.region
ORDER BY lifetime_value DESC

-- Query 7: Average Days to Resolve Tickets
SELECT priority, AVG(julianday(resolved_date) - julianday(created_date)) AS avg_days_to_resolve
FROM tickets
WHERE status = 'closed'
GROUP BY priority
ORDER BY avg_days_to_resolve

-- Query 8: Repeat Buyers vs One-Time Customers
SELECT 
    CASE WHEN order_count > 1 THEN 'repeat' ELSE 'one-time' END AS customer_type,
    COUNT(*) AS num_customers
FROM (
    SELECT customer_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
) 
GROUP BY customer_type

-- Query 9: Average Payment Lag
SELECT ROUND(AVG(julianday(paid_date) - julianday(due_date)), 1) AS avg_days_late
FROM invoices
WHERE status = 'paid'

-- Query 10: Revenue by Region
SELECT SUM(total_amount) AS total_revenue, region
FROM orders JOIN customers ON orders.customer_id = customers.customer_id
GROUP BY region
ORDER BY total_revenue DESC

-- Query 11: Revenue by Segment
SELECT SUM(total_amount) AS total_revenue, segment
FROM orders JOIN customers ON orders.customer_id = customers.customer_id
GROUP BY segment
ORDER BY total_revenue DESC

-- Query 12: Monthly Order Volume Trend
SELECT strftime('%Y-%m', order_date) AS month,
       COUNT(order_id) AS total_orders
FROM orders
GROUP BY strftime('%Y-%m', order_date)
ORDER BY month

-- Query 13: Dead Stock
SELECT p.name, p.category, p.stock_quantity
FROM products p
WHERE p.product_id NOT IN (SELECT product_id FROM order_items)

-- Query 14: Churn Risk
SELECT c.name, c.segment, c.region, MAX(o.order_date) AS last_order_date, 
ROUND(julianday('now') - julianday(MAX(o.order_date)), 0) AS days_since_last_order
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name, c.segment, c.region
HAVING julianday('now') - julianday(MAX(o.order_date)) >= 180
ORDER BY days_since_last_order DESC

-- Query 15: Support Ticket Volume by Category
SELECT category, COUNT(*) AS ticket_count
FROM tickets
GROUP BY category
ORDER BY ticket_count DESC