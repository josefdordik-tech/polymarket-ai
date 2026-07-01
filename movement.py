import sqlite3

conn = sqlite3.connect("poly.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT
    market_slug,
    token_id,
    side,
    MIN(ts),
    MAX(ts),
    MIN(price),
    MAX(price),
    ROUND((MAX(price)-MIN(price))*100,4)
FROM price_ticks
GROUP BY market_slug, token_id, side
HAVING COUNT(*) >= 2
ORDER BY MAX(ts) DESC
LIMIT 20
""").fetchall()

print("=" * 80)

for r in rows:
    print(r[0])
    print(f"{r[2]} | {r[5]} -> {r[6]} | Δ {r[7]} bodů")
    print("-" * 80)

conn.close()
