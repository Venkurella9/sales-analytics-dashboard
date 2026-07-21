import os
import sqlite3
import pandas as pd
from functools import lru_cache

DB_PATH = 'sql/sales_data.db'


def _ensure_db_exists():
    """Create the synthetic dataset and SQLite DB if it doesn't exist."""
    if os.path.exists(DB_PATH):
        return
    print('sales_data.db not found — generating synthetic data and building DB...')
    try:
        # Import generation/cleaning pipeline from the top-level `data` package
        import data.generate_data as gen
        import data.clean_data as clean
    except Exception as e:
        raise RuntimeError('Failed to import data generation modules') from e

    # Generate CSV then run cleaning pipeline which also writes the SQLite DB
    gen.main(rows=100000, out_csv='data/sales_data.csv')
    clean.clean()


@lru_cache(maxsize=1)
def load_sales_table(limit=None):
    _ensure_db_exists()
    conn = sqlite3.connect(DB_PATH)
    query = 'SELECT * FROM sales'
    if limit:
        query += f' LIMIT {int(limit)}'
    df = pd.read_sql_query(query, conn, parse_dates=['order_date'])
    conn.close()
    return df
