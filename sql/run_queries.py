"""Execute queries from queries.sql against the SQLite DB and report results.
This script will parse `queries.sql`, split on semicolons, skip comments, execute each statement,
and print a brief summary for verification.
"""
import sqlite3
import re
from pathlib import Path

DB = Path('sql/sales_data.db')
QUERIES = Path('sql/queries.sql')

def load_queries(path):
    text = path.read_text()
    # Remove -- comments
    lines = []
    for line in text.splitlines():
        if line.strip().startswith('--'):
            continue
        lines.append(line)
    cleaned = '\n'.join(lines)
    # Split by semicolon but keep content
    parts = [p.strip() for p in re.split(r';\s*\n', cleaned) if p.strip()]
    return parts

def run():
    if not DB.exists():
        raise SystemExit(f"DB not found: {DB}")
    conn = sqlite3.connect(str(DB))
    cur = conn.cursor()
    queries = load_queries(QUERIES)
    success = 0
    results = []
    for i, q in enumerate(queries, 1):
        try:
            cur.execute(q)
            rows = cur.fetchall()
            # For aggregate single-row results, show the values
            if rows and len(rows) <= 10:
                results.append((i, q[:80].replace('\n',' '), len(rows), rows))
            else:
                results.append((i, q[:80].replace('\n',' '), len(rows), None))
            success += 1
        except Exception as e:
            results.append((i, q[:80].replace('\n',' '), 'ERROR', str(e)))
    conn.close()
    # Print summary
    for r in results:
        if r[2] == 'ERROR':
            print(f"Query {r[0]}: ERROR -> {r[3]}")
        else:
            print(f"Query {r[0]}: returned {r[2]} rows | preview: {r[3] if r[3] else ''}")
    print(f"\nExecuted {success}/{len(queries)} queries successfully.")
    return success, len(queries)

if __name__ == '__main__':
    run()
