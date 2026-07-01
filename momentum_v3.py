import sqlite3

conn=sqlite3.connect("poly.db")
cur=conn.cursor()

rows=cur.execute("""
WITH t AS (
SELECT market_slug, token_id, side, ts, price,
ROW_NUMBER() OVER(PARTITION BY market_slug, token_id, side ORDER BY ts) rn1,
ROW_NUMBER() OVER(PARTITION BY market_slug, token_id, side ORDER BY ts DESC) rn2
FROM price_ticks
WHERE ts>=datetime('now','-60 seconds')
)
SELECT
a.market_slug,
a.side,
a.price,
b.price,
ROUND((b.price-a.price)*100,2) AS move
FROM t a
JOIN t b
ON a.market_slug=b.market_slug
AND a.token_id=b.token_id
AND a.side=b.side
WHERE a.rn1=1
AND b.rn2=1
ORDER BY ABS(move) DESC
LIMIT 20;
""").fetchall()

for slug, side, old, new, move in rows:
    print(f"{move:7.2f} | {side:4} | {old:.3f} -> {new:.3f} | {slug}")

conn.close()
