# modules/dns_resolver.py
import subprocess

def configure_tor_dns():
    # Configure Tor to handle DNS requests
    with open("/etc/tor/torrc", "a") as torrc:
        torrc.write("DNSPort 9053\n")
    print("[*] Tor DNS resolver configured on port 9053.")
    subprocess.run(["systemctl", "restart", "tor"])

if __name__ == "__main__":
    configure_tor_dns()
