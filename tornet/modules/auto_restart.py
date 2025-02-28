# modules/auto_restart.py
import subprocess
import time

def monitor_tor_connection():
    while True:
        result = subprocess.run(["curl", "--socks5", "localhost:9050", "https://check.torproject.org"], capture_output=True, text=True)
        if "Congratulations" not in result.stdout:
            print("[*] Tor connection lost. Restarting...")
            subprocess.run(["systemctl", "restart", "tor"])
        time.sleep(60)

if __name__ == "__main__":
    monitor_tor_connection()
