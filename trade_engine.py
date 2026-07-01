import sqlite3
import requests

DB = "poly.db"

MIN_MOVE = 3.0
MAX_SPREAD = 5.0
MIN_DEPTH = 100.0
EST_FEE = 0.02

conn = sqlite3.connect(DB)
cur = conn.cursor()

rows = cur.execute("""
WITH t AS (
SELECT market_slug, token_id, side, ts, price,
ROW_NUMBER() OVER(PARTITION BY market_slug, token_id, side ORDER BY ts) rn1,
ROW_NUMBER() OVER(PARTITION BY market_slug, token_id, side ORDER BY ts DESC) rn2
FROM price_ticks
WHERE ts>=datetime('now','-60 seconds')
)
SELECT a.market_slug, a.token_id, a.side, a.price, b.price,
ROUND((b.price-a.price)*100,2) AS move
FROM t a
JOIN t b
ON a.market_slug=b.market_slug
AND a.token_id=b.token_id
AND a.side=b.side
WHERE a.rn1=1 AND b.rn2=1
AND ABS(move) >= ?
ORDER BY ABS(move) DESC
LIMIT 20
""", (MIN_MOVE,)).fetchall()

print("="*80)
print("TRADE ENGINE")
print("="*80)

if not rows:
    print("NO TRADE")
    conn.close()
    exit()

for slug, token, side, old, new, move in rows:
    r = requests.get(
        "https://clob.polymarket.com/book",
        params={"token_id": token},
        timeout=5
    )

    if r.status_code != 200:
        continue

    book = r.json()
    bids = book.get("bids", [])
    asks = book.get("asks", [])

    if not bids or not asks:
        continue

    bid = float(bids[0]["price"])
    ask = float(asks[0]["price"])
    spread = (ask - bid) * 100

    depth = sum(float(x["size"]) for x in asks[:5])

    expected_move = abs(move)
    net_edge = expected_move - spread - EST_FEE

    decision = "SKIP"

    if spread <= MAX_SPREAD and depth >= MIN_DEPTH and net_edge > 0:
        decision = "BUY_READY"

    print(f"{decision} | move {move:+.2f} | spread {spread:.2f} | depth {depth:.1f} | edge {net_edge:.2f} | {slug}")

conn.close()
