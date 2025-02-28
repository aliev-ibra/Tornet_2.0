# modules/vpn_mode.py
import subprocess

def enable_vpn_mode():
    # Redirect all traffic through Tor
    subprocess.run(["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "tcp", "--syn", "-j", "REDIRECT", "--to-ports", "9040"])
    print("[*] VPN mode enabled. All traffic routed through Tor.")

if __name__ == "__main__":
    enable_vpn_mode()
