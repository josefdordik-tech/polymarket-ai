import sqlite3

conn = sqlite3.connect("poly.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT
    market_slug,
    side,
    MIN(price) AS pmin,
    MAX(price) AS pmax,
    ROUND((MAX(price)-MIN(price))*100,2) AS move
FROM price_ticks
GROUP BY market_slug, side
HAVING COUNT(*) >= 2
ORDER BY move DESC
LIMIT 20
""").fetchall()

print("=" * 80)
print("TOP MOVES")
print("=" * 80)

for slug, side, pmin, pmax, move in rows:
    print(f"{move:6.2f} | {side:4} | {pmin:.3f} -> {pmax:.3f} | {slug}")

conn.close()
