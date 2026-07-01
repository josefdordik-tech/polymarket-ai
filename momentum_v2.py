import sqlite3

conn=sqlite3.connect("poly.db")
cur=conn.cursor()

rows=cur.execute("""
WITH t AS (
SELECT market_slug,
       ts,
       price,
       ROW_NUMBER() OVER(PARTITION BY market_slug ORDER BY ts) rn1,
       ROW_NUMBER() OVER(PARTITION BY market_slug ORDER BY ts DESC) rn2
FROM price_ticks
WHERE ts>=datetime('now','-60 seconds')
)
SELECT
a.market_slug,
a.price,
b.price,
ROUND((b.price-a.price)*100,2)
FROM t a
JOIN t b
ON a.market_slug=b.market_slug
WHERE a.rn1=1
AND b.rn2=1
ORDER BY 4 DESC;
""").fetchall()

for r in rows:
    print(r)

conn.close()
