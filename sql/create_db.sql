-- SQL schema for sales table
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
  order_id INTEGER PRIMARY KEY,
  order_date TEXT,
  customer_id INTEGER,
  customer_name TEXT,
  region TEXT,
  payment_method TEXT,
  product_id INTEGER,
  product_name TEXT,
  category TEXT,
  unit_price REAL,
  unit_cost REAL,
  quantity INTEGER,
  discount REAL,
  revenue REAL,
  cost REAL,
  profit REAL,
  order_value REAL,
  country TEXT,
  city TEXT
);

CREATE INDEX IF NOT EXISTS idx_order_date ON sales(order_date);
CREATE INDEX IF NOT EXISTS idx_category ON sales(category);
CREATE INDEX IF NOT EXISTS idx_region ON sales(region);
CREATE INDEX IF NOT EXISTS idx_customer ON sales(customer_id);
