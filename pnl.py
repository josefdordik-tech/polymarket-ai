cat > pnl.py << 'EOF'
import sqlite3

DB = "poly.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS paper_pnl (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trade_id INTEGER,
    entry_price REAL,
    current_price REAL,
    size_usd REAL,
    pnl_usd REAL,
    pnl_pct REAL,
    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

trades = cur.execute("""
SELECT id, token_id, entry_price, size_usd
FROM paper_trades
WHERE status='OPEN'
""").fetchall()

if not trades:
    print("NO OPEN PAPER TRADES")
    conn.commit()
    conn.close()
    exit()

for trade_id, token_id, entry_price, size_usd in trades:
    row = cur.execute("""
    SELECT price
    FROM price_ticks
    WHERE token_id=?
    ORDER BY ts DESC
    LIMIT 1
    """, (token_id,)).fetchone()

    if not row:
        continue

    current_price = row[0]
    pnl_pct = ((current_price - entry_price) / entry_price) * 100
    pnl_usd = size_usd * (pnl_pct / 100)

    cur.execute("""
    INSERT INTO paper_pnl
    (trade_id, entry_price, current_price, size_usd, pnl_usd, pnl_pct)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (trade_id, entry_price, current_price, size_usd, pnl_usd, pnl_pct))

    print(f"TRADE {trade_id} | {entry_price:.3f}->{current_price:.3f} | PNL {pnl_usd:+.4f} USD ({pnl_pct:+.2f}%)")

conn.commit()
conn.close()
