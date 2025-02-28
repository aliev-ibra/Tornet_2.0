# modules/proxy_mode.py
import subprocess

def enable_proxy_mode():
    subprocess.run(["iptables", "-t", "nat", "-A", "OUTPUT", "-p", "tcp", "--syn", "-j", "REDIRECT", "--to-ports", "9040"])
    print("[*] Proxy mode enabled. All traffic routed through Tor.")

if __name__ == "__main__":
    enable_proxy_mode()
