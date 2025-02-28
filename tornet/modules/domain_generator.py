# modules/domain_generator.py
import os

def generate_onion_domain():
    os.system("tor --hash-password mypassword > torrc")
    os.system("tor --service install")
    print("[*] New .onion domain generated and hosted locally.")

if __name__ == "__main__":
    generate_onion_domain()
