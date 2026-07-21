import sqlite3
from pathlib import Path


def test_db_exists_and_has_rows():
    db = Path('sql/sales_data.db')
    assert db.exists(), 'SQLite DB not found at sql/sales_data.db'
    conn = sqlite3.connect(str(db))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM sales")
    cnt = cur.fetchone()[0]
    conn.close()
    assert cnt >= 100000, f'Expected >=100000 rows in sales table, found {cnt}'
