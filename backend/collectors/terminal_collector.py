import os
import time
import json
import requests
import sys

API_URL = "http://127.0.0.1:8000/api/v1/events/batch"
HISTORY_FILE = os.path.expanduser("~/.bash_history")

def tail_history():
    if not os.path.exists(HISTORY_FILE):
        print(f"History file {HISTORY_FILE} not found.")
        sys.exit(1)
        
    print(f"Tailing {HISTORY_FILE} for new commands...")
    with open(HISTORY_FILE, "r", encoding="utf-8", errors="ignore") as f:
        f.seek(0, 2) # Go to the end of the file
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            
            line = line.strip()
            if line:
                payload = {
                    "source": "terminal",
                    "events": [{"command": line}]
                }
                try:
                    res = requests.post(API_URL, json=payload)
                    print(f"Sent: {line} -> Status: {res.status_code}")
                except Exception as e:
                    print(f"Failed to send event: {e}")

if __name__ == "__main__":
    tail_history()
