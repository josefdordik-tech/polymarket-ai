import sqlite3

conn=sqlite3.connect("poly.db")
cur=conn.cursor()

rows=cur.execute("""
SELECT market_slug,
COUNT(*),
MIN(price),
MAX(price),
ROUND((MAX(price)-MIN(price))*100,2)
FROM price_ticks
WHERE ts>=datetime('now','-60 seconds')
GROUP BY market_slug
HAVING COUNT(*)>5
ORDER BY 5 DESC
LIMIT 20
""").fetchall()

for r in rows:
    print(r)

conn.close()
