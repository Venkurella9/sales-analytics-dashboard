"""
Simple cleaning pipeline: load generated CSV, basic fixes, save cleaned CSV and SQLite DB.
"""
import pandas as pd
import sqlite3
import os

RAW = 'data/sales_data.csv'
CLEAN = 'data/sales_data_clean.csv'
DB = 'sql/sales_data.db'


def clean():
    df = pd.read_csv(RAW, parse_dates=['order_date'])
    # Drop exact duplicates
    df = df.drop_duplicates()
    # Ensure types
    df['quantity'] = df['quantity'].astype(int)
    df['unit_price'] = df['unit_price'].astype(float)
    df['unit_cost'] = df['unit_cost'].astype(float)
    df['discount'] = df['discount'].astype(float)
    df['revenue'] = df['revenue'].astype(float)
    df['cost'] = df['cost'].astype(float)
    df['profit'] = df['profit'].astype(float)

    # Basic sanity filters
    df = df[df['quantity']>0]
    df = df[df['unit_price'] > 0]

    os.makedirs(os.path.dirname(CLEAN), exist_ok=True)
    df.to_csv(CLEAN, index=False)
    print(f"Saved cleaned CSV -> {CLEAN}")

    # Save to SQLite
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    conn = sqlite3.connect(DB)
    df.to_sql('sales', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Saved SQLite DB -> {DB}")


if __name__ == '__main__':
    clean()
