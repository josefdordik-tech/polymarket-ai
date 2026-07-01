import sqlite3

DB = "poly.db"

MIN_MOVE = 5.0

conn = sqlite3.connect(DB)
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
HAVING COUNT(*) >= 2 AND move >= ?
ORDER BY move DESC
LIMIT 20
""", (MIN_MOVE,)).fetchall()

print("=" * 80)
print("SIGNALS")
print("=" * 80)

if not rows:
    print("NO SIGNALS")

for slug, side, pmin, pmax, move in rows:
    signal = "WATCH"
    if move >= 10:
        signal = "STRONG WATCH"

    print(f"{signal} | {move:6.2f} bodů | {side:4} | {pmin:.3f} -> {pmax:.3f} | {slug}")

conn.close()
