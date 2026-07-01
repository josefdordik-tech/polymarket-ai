import time
import subprocess
from datetime import datetime

LOOP_SECONDS = 10

while True:
    print("=" * 80)
    print("RUNNER V2", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    subprocess.run(["python3", "price_collector.py"])
    subprocess.run(["python3", "signal.py"])
    subprocess.run(["python3", "trade_engine.py"])
    subprocess.run(["python3", "paper_trader.py"])
    subprocess.run(["python3", "watchdog.py"])

    print(f"SLEEP {LOOP_SECONDS}s")
    time.sleep(LOOP_SECONDS)
