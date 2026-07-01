import requests
import json

URL = "https://gamma-api.polymarket.com/events"

params = {
    "active": "true",
    "closed": "false",
    "order": "volume_24hr",
    "ascending": "false",
    "limit": 20
}

r = requests.get(URL, params=params, timeout=20)
print("STATUS:", r.status_code)
r.raise_for_status()

events = r.json()

for e in events:
    print("=" * 80)
    print("EVENT:", e.get("title") or e.get("slug"))

    for m in e.get("markets", []):
        q = m.get("question")
        tokens = m.get("clobTokenIds")
        volume = m.get("volume24hr") or m.get("volume")
        liquidity = m.get("liquidity")

        print("QUESTION:", q)
        print("VOLUME:", volume, "LIQ:", liquidity)
        print("TOKENS:", tokens)
