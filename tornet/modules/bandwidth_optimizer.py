# modules/bandwidth_optimizer.py
import subprocess

def optimize_tor_bandwidth():
    # Update torrc to use faster nodes
    with open("/etc/tor/torrc", "a") as torrc:
        torrc.write("StrictNodes 1\n")
        torrc.write("ExitNodes {US},{DE},{NL}\n")
    print("[*] Tor bandwidth optimized for US, DE, and NL nodes.")
    subprocess.run(["systemctl", "restart", "tor"])

if __name__ == "__main__":
    optimize_tor_bandwidth()
