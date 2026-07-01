import sqlite3

DB = "poly.db"
WINDOW = 60

conn = sqlite3.connect(DB)
cur = conn.cursor()

rows = cur.execute("""
WITH recent AS (
    SELECT *
    FROM price_ticks
    WHERE ts >= datetime('now', ?)
)
SELECT
    market_slug,
    side,
    MIN(price),
    MAX(price),
    ROUND((MAX(price)-MIN(price))*100,2) AS move
FROM recent
GROUP BY market_slug, side
HAVING COUNT(*) >= 2
ORDER BY move DESC
LIMIT 20
""", (f"-{WINDOW} seconds",)).fetchall()

print("="*80)
print(f"LAST {WINDOW} SECONDS")
print("="*80)

for slug, side, pmin, pmax, move in rows:
    print(f"{move:6.2f} | {side:4} | {pmin:.3f} -> {pmax:.3f} | {slug}")

conn.close()
