import json
import sqlite3
import requests

DB = "poly.db"
URL = "https://gamma-api.polymarket.com/events"

def to_float(value):
    try:
        return float(value or 0)
    except:
        return 0.0

def save_market(cur, market):
    tokens_raw = market.get("clobTokenIds")
    slug = market.get("slug")

    if not tokens_raw or not slug:
        return 0

    tokens = json.loads(tokens_raw) if isinstance(tokens_raw, str) else tokens_raw
    if len(tokens) < 2:
        return 0

    cur.execute("""
        INSERT OR IGNORE INTO markets
        (question, slug, volume, liquidity, token_yes, token_no)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        market.get("question"),
        slug,
        to_float(market.get("volume") or market.get("volume24hr")),
        to_float(market.get("liquidity")),
        tokens[0],
        tokens[1],
    ))

    return cur.rowcount

def main():
    r = requests.get(URL, params={
        "active": "true",
        "closed": "false",
        "limit": 20
    }, timeout=20)
    r.raise_for_status()

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    saved = 0
    seen = 0

    for event in r.json():
        for market in event.get("markets", []):
            seen += 1
            saved += save_market(cur, market)

    conn.commit()
    conn.close()

    print(f"SEEN: {seen}")
    print(f"NEW SAVED: {saved}")

if __name__ == "__main__":
    main()
