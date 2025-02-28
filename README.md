# Tornet_2.0

## About
Tornet_2.0 is a powerful toolset designed for analyzing, optimizing, and enhancing Tor network usage. It provides multiple functionalities to improve anonymity, monitor traffic, and interact with the dark web securely.

## Features
- **Tor Multi-Hop Proxy:** Chain multiple proxies for increased anonymity.
- **Tor Traffic Analyzer:** Monitor network traffic and analyze HTTP/HTTPS requests over Tor.
- **Tor Hidden Service Scanner:** Scan .onion sites to check their availability.
- **Tor Auto Identity Switcher:** Change IP for every request.
- **Tor Connection Stability Tester:** Test internet speed over Tor.
- **Tor Traffic Monitor:** Track data sent/received over Tor in real time.
- **Tor Proxy Mode:** Route all system traffic through Tor.
- **Dark Web Domain Generator:** Create random .onion domains.
- **Tor CAPTCHA Bypass:** Optimize Tor settings to reduce CAPTCHA frequency.
- **Automatic Tor Bridges Finder:** Automatically find Tor bridges for censored regions.
- **Tor Hidden Chat:** Enable anonymous messaging via Tor.
- **AI-Based IP Change Predictor:** Use AI to select the most stable Tor exit nodes.
- **Tor Fingerprint Spoofing:** Change browser fingerprint to prevent tracking.
- **Tor Bandwidth Optimizer:** Optimize Tor connections for higher speed.
- **Stealth Mode:** Make Tor traffic look like normal HTTPS traffic.
- **Tor-Based DNS Resolver:** Route DNS queries through Tor for anonymity.
- **Exit Node Selector:** Choose Tor exit nodes by country.
- **Tor Hidden VPN Mode:** Use Tor as a system-wide VPN.
- **Tor Connection Auto-Restart:** Automatically restart Tor if the connection drops.
- **Tor Malicious Node Detector:** Detect malicious exit nodes modifying traffic.
- **Tor P2P File Sharing:** Share files anonymously over Tor.
- **Tor Connection Visualizer:** Display Tor network routes graphically.

## Installation
### Requirements
Ensure you have the following dependencies installed:
```bash
sudo apt update && sudo apt install tor python3 python3-pip
```
Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Below is the list of available functionalities and how to use them:

- **Tor Multi-Hop Proxy** (Chain multiple proxies for increased anonymity)
```bash
python main.py --multi-hop
```
- **Tor Traffic Analyzer** (Monitor HTTP/HTTPS traffic over Tor)
```bash
python main.py --traffic-analyzer
```
- **Tor Hidden Service Scanner** (Scan .onion sites to check their availability)
```bash
python main.py --scan-onion
```
- **Tor Auto Identity Switcher** (Change Tor IP for every request)
```bash
python main.py --auto-identity
```
- **Tor Connection Stability Tester** (Test network speed over Tor)
```bash
python main.py --test-speed
```
- **Tor Traffic Monitor** (Track data sent/received in real-time)
```bash
python main.py --monitor-traffic
```
- **Tor Proxy Mode** (Route all system traffic through Tor)
```bash
python main.py --proxy-mode
```
- **Dark Web Domain Generator** (Create random .onion domains)
```bash
python main.py --create-onion
```
- **Tor CAPTCHA Bypass** (Bypass CAPTCHAs by selecting better exit nodes)
```bash
python main.py --captcha-bypass
```
- **Automatic Tor Bridges Finder** (Find Tor bridges for censored countries)
```bash
python main.py --find-bridges
```
- **Tor Hidden Chat** (Enable anonymous messaging via Tor)
```bash
python main.py --chat
```
- **AI-Based IP Change Predictor** (Analyze IP changes and predict stable nodes)
```bash
python main.py --smart-ip
```
- **Tor Fingerprint Spoofing** (Spoof browser fingerprint for anonymity)
```bash
python main.py --spoof-fingerprint
```
- **Tor Bandwidth Optimizer** (Optimize exit node selection for speed)
```bash
python main.py --fast-tor
```
- **Stealth Mode** (Make Tor traffic appear as normal HTTPS traffic)
```bash
python main.py --stealth
```
- **Tor-Based DNS Resolver** (Route DNS queries through Tor)
```bash
python main.py --dns-tor
```
- **Exit Node Selector** (Select Tor exit nodes by country)
```bash
python main.py --exit-country US
```
- **Tor Hidden VPN Mode** (Use Tor as a VPN for all traffic)
```bash
python main.py --vpn-mode
```
- **Tor Connection Auto-Restart** (Restart Tor if the connection drops)
```bash
python main.py --auto-restart
```
- **Tor Malicious Node Detector** (Detect exit nodes modifying traffic)
```bash
python main.py --detect-malicious
```
- **Tor P2P File Sharing** (Share files anonymously over Tor)
```bash
python main.py --file-share
```
- **Tor Connection Visualizer** (Graphically display Tor network routes)
```bash
python main.py --visualize-tor
```

## Directory Structure
```
tornet/
│── modules/
│   │── tor_multi_hop.py
│   │── traffic_analyzer.py
│   │── hidden_service_scanner.py
│   │── auto_identity_switcher.py
│   │── connection_stability_tester.py
│   │── traffic_monitor.py
│   │── proxy_mode.py
│   │── domain_generator.py
│   │── captcha_bypass.py
│   │── bridges_finder.py
│   │── hidden_chat.py
│   │── ai_ip_predictor.py
│   │── fingerprint_spoofing.py
│   │── bandwidth_optimizer.py
│   │── stealth_mode.py
│   │── dns_resolver.py
│   │── exit_node_selector.py
│   │── vpn_mode.py
│   │── auto_restart.py
│   │── malicious_node_detector.py
│   │── p2p_sharing.py
│   │── tor_visualizer.py
│── main.py
│── requirements.txt
│── README.md
```

## License
This project is licensed under the MIT License.

## Author
Developed by **[aliev-ibra]**

