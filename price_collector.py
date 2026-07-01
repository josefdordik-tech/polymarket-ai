import sqlite3
import requests

DB = "poly.db"
PRICE_URL = "https://clob.polymarket.com/price"

def get_price(token_id, side):
    r = requests.get(
        PRICE_URL,
        params={"token_id": token_id, "side": side},
        timeout=10
    )
    if r.status_code != 200:
        return None
    data = r.json()
    return float(data["price"]) if "price" in data else None

def main():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    markets = cur.execute("""
        SELECT slug, token_yes, token_no
        FROM markets
        LIMIT 20
    """).fetchall()

    saved = 0

    for slug, token_yes, token_no in markets:
        for token_id in [token_yes, token_no]:
            for side in ["BUY", "SELL"]:
                price = get_price(token_id, side)
                if price is None:
                    continue

                cur.execute("""
                    INSERT INTO price_ticks
                    (market_slug, token_id, price, side)
                    VALUES (?, ?, ?, ?)
                """, (slug, token_id, price, side))

                saved += 1

    conn.commit()
    conn.close()

    print(f"SAVED PRICE TICKS: {saved}")

if __name__ == "__main__":
    main()
