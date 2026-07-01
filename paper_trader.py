import sqlite3
from datetime import datetime

DB = "poly.db"

MIN_MOVE = 3.0
FAKE_SIZE_USD = 5.0
TAKE_PROFIT = 1.5
STOP_LOSS = 1.0

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS paper_trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    market_slug TEXT,
    token_id TEXT,
    side TEXT,
    entry_price REAL,
    size_usd REAL,
    status TEXT,
    opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    closed_at TIMESTAMP,
    exit_price REAL,
    pnl REAL
)
""")

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
LIMIT 5
""", (MIN_MOVE,)).fetchall()

if not rows:
    print("NO PAPER TRADE")
    conn.commit()
    conn.close()
    exit()

opened = 0

for slug, token, side, old, new, move in rows:
    exists = cur.execute("""
    SELECT COUNT(*) FROM paper_trades
    WHERE market_slug=? AND token_id=? AND status='OPEN'
    """, (slug, token)).fetchone()[0]

    if exists:
        continue

    cur.execute("""
    INSERT INTO paper_trades
    (market_slug, token_id, side, entry_price, size_usd, status)
    VALUES (?, ?, ?, ?, ?, 'OPEN')
    """, (slug, token, side, new, FAKE_SIZE_USD))

    opened += 1
    print(f"PAPER BUY | {new:.3f} | {FAKE_SIZE_USD} USD | move {move:+.2f} | {slug}")

conn.commit()
conn.close()

print("OPENED:", opened)
