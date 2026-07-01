import sqlite3

DB = "poly.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

rows = cur.execute("""
SELECT market_slug, token_id, side, COUNT(*) as ticks,
       MIN(price), MAX(price),
       ROUND((MAX(price) - MIN(price)) * 100, 4) as change_points
FROM price_ticks
GROUP BY market_slug, token_id, side
HAVING ticks >= 2
ORDER BY ABS(change_points) DESC
LIMIT 10
""").fetchall()

print("TOP PRICE MOVES")
print("=" * 60)

for r in rows:
    print("MARKET:", r[0])
    print("SIDE:", r[2])
    print("TICKS:", r[3])
    print("MIN:", r[4], "MAX:", r[5], "MOVE:", r[6], "points")
    print("-" * 60)

conn.close()
