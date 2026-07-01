import sqlite3

conn = sqlite3.connect("poly.db")
cur = conn.cursor()

rows = cur.execute("""
SELECT
    slug,
    liquidity,
    volume
FROM markets
ORDER BY liquidity DESC
LIMIT 20
""").fetchall()

print("="*80)
print("TOP LIQUIDITY")
print("="*80)

for slug, liq, vol in rows:
    print(f"{liq:12.2f} | {vol:12.2f} | {slug}")

conn.close()
