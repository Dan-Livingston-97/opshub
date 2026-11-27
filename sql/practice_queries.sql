-- List overdue open orders by promised ship date.
SELECT order_id, customer_id, promised_ship_date
FROM orders
WHERE status = 'Delayed'
ORDER BY promised_ship_date, order_id;

-- Show customer names alongside overdue orders.
SELECT orders.order_id, customers.customer_name, orders.promised_ship_date
FROM orders
JOIN customers ON orders.customer_id = customers.customer_id
WHERE orders.status = 'Delayed'
ORDER BY orders.promised_ship_date, orders.order_id;

-- Calculate the value of order 1001 in cents.
SELECT SUM(quantity * unit_price_cents)
FROM order_lines
WHERE order_id = 1001;
