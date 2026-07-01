import sqlite3
from datetime import datetime, timezone

conn = sqlite3.connect("poly.db")
cur = conn.cursor()

ts = cur.execute("SELECT MAX(ts) FROM price_ticks").fetchone()[0]

if ts is None:
    print("ERROR: žádná data")
    exit(1)

last = datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
last = last.replace(tzinfo=timezone.utc)

age = (datetime.now(timezone.utc) - last).total_seconds()

if age <= 30:
    print(f"OK  poslední tick před {age:.1f} s")
else:
    print(f"WARNING  poslední tick před {age:.1f} s")

conn.close()
