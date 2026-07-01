import asyncio
import json
import websockets

WS_URL = "wss://ws-subscriptions-clob.polymarket.com/ws/market"

async def main():
    async with websockets.connect(WS_URL) as ws:
        print("CONNECTED")

        await ws.send(json.dumps({
            "type": "market",
            "assets_ids": []
        }))

        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=20)
                print(msg[:500])
            except asyncio.TimeoutError:
                print("NO DATA 20s - connection alive, but no market selected")

asyncio.run(main())
