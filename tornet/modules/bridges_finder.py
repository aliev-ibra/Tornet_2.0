# modules/bridges_finder.py
import requests

def find_bridges():
    response = requests.get("https://bridges.torproject.org/bridges")
    print(f"[*] Found Bridges: {response.text}")

if __name__ == "__main__":
    find_bridges()
