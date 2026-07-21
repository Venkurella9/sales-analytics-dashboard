-- Business analysis queries
-- KPIs
-- Total Revenue
SELECT SUM(revenue) AS total_revenue FROM sales;
-- Total Orders
SELECT COUNT(DISTINCT order_id) AS total_orders FROM sales;
-- Average Order Value
SELECT AVG(order_value) AS aov FROM sales;
-- Total Profit
SELECT SUM(profit) AS total_profit FROM sales;
-- Profit Margin
SELECT SUM(profit)/SUM(revenue) AS profit_margin FROM sales;

-- Monthly Sales Trend
SELECT strftime('%Y-%m', order_date) AS year_month, SUM(revenue) AS revenue
FROM sales
GROUP BY year_month
ORDER BY year_month;

-- Sales by Category
SELECT category, SUM(revenue) AS revenue
FROM sales
GROUP BY category
ORDER BY revenue DESC;

-- Sales by Region
SELECT region, SUM(revenue) AS revenue
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- Top 10 Products
SELECT product_id, product_name, SUM(revenue) AS revenue
FROM sales
GROUP BY product_id, product_name
ORDER BY revenue DESC
LIMIT 10;

-- Top Customers
SELECT customer_id, customer_name, SUM(revenue) AS revenue, COUNT(order_id) AS orders
FROM sales
GROUP BY customer_id, customer_name
ORDER BY revenue DESC
LIMIT 10;

-- Year-over-Year Growth (by year)
SELECT strftime('%Y', order_date) AS year, SUM(revenue) AS revenue
FROM sales
GROUP BY year
ORDER BY year;
