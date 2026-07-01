import sqlite3
import requests

DB = "poly.db"

conn = sqlite3.connect(DB)
cur = conn.cursor()

row = cur.execute("""
SELECT market_slug, token_id
FROM price_ticks
LIMIT 1
""").fetchone()

slug, token = row

r = requests.get(
    "https://clob.polymarket.com/book",
    params={"token_id": token},
    timeout=5
)

print("="*70)
print("BUY ENGINE")
print("="*70)

if r.status_code != 200:
    print("API ERROR", r.status_code)
    exit()

book = r.json()

best_bid = float(book["bids"][0]["price"])
best_ask = float(book["asks"][0]["price"])

spread = (best_ask - best_bid) * 100

print(slug)
print("Bid:", best_bid)
print("Ask:", best_ask)
print(f"Spread: {spread:.2f} bodu")

conn.close()
