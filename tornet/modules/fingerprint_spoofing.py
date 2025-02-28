# modules/fingerprint_spoofing.py
from fake_useragent import UserAgent
import random

def spoof_fingerprint():
    ua = UserAgent()
    user_agent = ua.random
    screen_size = f"{random.randint(800, 1920)}x{random.randint(600, 1080)}"
    print(f"Spoofed User-Agent: {user_agent}")
    print(f"Spoofed Screen Size: {screen_size}")

if __name__ == "__main__":
    spoof_fingerprint()
