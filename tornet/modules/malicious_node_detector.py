# modules/malicious_node_detector.py
import requests

def detect_malicious_nodes():
    # Check for malicious nodes using Tor's consensus data
    response = requests.get("https://onionoo.torproject.org/summary?search=flag:bad")
    if response.status_code == 200:
        print("[*] Malicious nodes detected:")
        print(response.json())
    else:
        print("[*] No malicious nodes found.")

if __name__ == "__main__":
    detect_malicious_nodes()
