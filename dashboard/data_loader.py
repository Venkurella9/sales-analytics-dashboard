import sqlite3
import pandas as pd
from functools import lru_cache

DB_PATH = 'sql/sales_data.db'

@lru_cache(maxsize=1)
def load_sales_table(limit=None):
    conn = sqlite3.connect(DB_PATH)
    query = 'SELECT * FROM sales'
    if limit:
        query += f' LIMIT {int(limit)}'
    df = pd.read_sql_query(query, conn, parse_dates=['order_date'])
    conn.close()
    return df
