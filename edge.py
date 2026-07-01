import sqlite3
import requests

DB="poly.db"

conn=sqlite3.connect(DB)
cur=conn.cursor()

markets=cur.execute("""
SELECT DISTINCT market_slug,token_id
FROM price_ticks
LIMIT 20
""").fetchall()

print("="*90)
print("EDGE SCANNER")
print("="*90)

for slug,token in markets:
    try:
        r=requests.get(
            "https://clob.polymarket.com/book",
            params={"token_id":token},
            timeout=5
        )

        if r.status_code!=200:
            continue

        book=r.json()

        bids=book.get("bids",[])
        asks=book.get("asks",[])

        if not bids or not asks:
            continue

        bid=float(bids[0]["price"])
        ask=float(asks[0]["price"])

        spread=(ask-bid)*100

        bid_size=sum(float(x["size"]) for x in bids[:5])
        ask_size=sum(float(x["size"]) for x in asks[:5])

        imbalance=bid_size/(bid_size+ask_size)

        print(f"{spread:5.2f} | {imbalance:0.3f} | {slug}")

    except Exception:
        pass

conn.close()
