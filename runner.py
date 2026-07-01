import time
import subprocess

while True:
    print("=" * 50)
    print("Collecting prices...")
    subprocess.run(["python3", "price_collector.py"])
    print("Sleeping 10 seconds...")
    time.sleep(10)
