#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import logging
from pathlib import Path

# Import modules
from modules.tor_multi_hop import TorMultiHop
from modules.traffic_analyzer import TrafficAnalyzer
from modules.hidden_service_scanner import HiddenServiceScanner
from modules.auto_identity_switcher import AutoIdentitySwitcher
from modules.connection_stability_tester import ConnectionStabilityTester
from modules.traffic_monitor import TrafficMonitor
from modules.proxy_mode import ProxyMode
from modules.domain_generator import DomainGenerator
from modules.captcha_bypass import CaptchaBypass
from modules.bridges_finder import BridgesFinder
from modules.hidden_chat import HiddenChat
from modules.ai_ip_predictor import AIIPPredictor
from modules.fingerprint_spoofing import FingerprintSpoofing
from modules.bandwidth_optimizer import BandwidthOptimizer
from modules.stealth_mode import StealthMode
from modules.dns_resolver import DNSResolver
from modules.exit_node_selector import ExitNodeSelector
from modules.vpn_mode import VPNMode
from modules.auto_restart import AutoRestart
from modules.malicious_node_detector import MaliciousNodeDetector
from modules.p2p_sharing import P2PSharing
from modules.tor_visualizer import TorVisualizer

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('tornet')

def check_tor_installed():
    """Check if Tor is installed on the system"""
    try:
        import stem
        return True
    except ImportError:
        return False

def check_root():
    """Check if the script is run with root/admin privileges"""
    return os.geteuid() == 0 if hasattr(os, 'geteuid') else False

def setup_argparser():
    """Configure command line arguments"""
    parser = argparse.ArgumentParser(description='TorNet - Advanced Tor Networking Tool')
    
    # Main arguments
    parser.add_argument('--multi-hop', action='store_true', help='Use multiple proxies in chain')
    parser.add_argument('--analyze-traffic', action='store_true', help='Analyze Tor traffic')
    parser.add_argument('--scan-onion', action='store_true', help='Scan .onion sites')
    parser.add_argument('--onion-list', type=str, help='File with list of .onion domains to scan')
    parser.add_argument('--switch-identity', action='store_true', help='Switch Tor identity on each request')
    parser.add_argument('--test-stability', action='store_true', help='Test Tor connection stability')
    parser.add_argument('--monitor-traffic', action='store_true', help='Monitor Tor traffic')
    parser.add_argument('--proxy-mode', action='store_true', help='Use Tor as universal proxy')
    parser.add_argument('--create-onion', action='store_true', help='Create a new .onion domain')
    parser.add_argument('--bypass-captcha', action='store_true', help='Try to bypass CAPTCHAs')
    parser.add_argument('--find-bridges', action='store_true', help='Find Tor bridges automatically')
    parser.add_argument('--chat', action='store_true', help='Start hidden chat service')
    parser.add_argument('--smart-ip', action='store_true', help='Use AI to predict best IP changes')
    parser.add_argument('--spoof-fingerprint', action='store_true', help='Spoof browser fingerprint')
    parser.add_argument('--fast-tor', action='store_true', help='Optimize Tor for speed')
    parser.add_argument('--stealth', action='store_true', help='Use stealth mode to hide Tor traffic')
    parser.add_argument('--dns-tor', action='store_true', help='Use Tor for DNS resolution')
    parser.add_argument('--exit-country', type=str, help='Select exit nodes from specific country (e.g., US,DE)')
    parser.add_argument('--vpn-mode', action='store_true', help='Use Tor as a VPN')
    parser.add_argument('--auto-restart', action='store_true', help='Automatically restart Tor connection if it fails')
    parser.add_argument('--detect-malicious', action='store_true', help='Detect malicious Tor nodes')
    parser.add_argument('--file-share', action='store_true', help='Start P2P file sharing over Tor')
    parser.add_argument('--visualize', action='store_true', help='Visualize Tor connection routes')

    return parser

def main():
    logger = setup_logging()
    logger.info("Starting TorNet...")
    
    if not check_tor_installed():
        logger.error("Tor and Stem library must be installed. Run 'pip install stem' and install Tor.")
        sys.exit(1)

    parser = setup_argparser()
    args = parser.parse_args()

    # If no arguments, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    # For some features, root privileges are required
    root_required_features = ['proxy-mode', 'vpn-mode', 'dns-tor', 'stealth']
    needs_root = any(getattr(args, arg.replace('-', '_')) for arg in root_required_features)
    
    if needs_root and not check_root():
        logger.error("Some features require root privileges. Please run with sudo.")
        sys.exit(1)
    
    # Initialize and run modules based on arguments
    try:
        if args.multi_hop:
            multi_hop = TorMultiHop()
            multi_hop.start()
            
        if args.analyze_traffic:
            analyzer = TrafficAnalyzer()
            analyzer.start()
            
        if args.scan_onion:
            if not args.onion_list:
                logger.error("Please provide a list of .onion domains using --onion-list")
                sys.exit(1)
            scanner = HiddenServiceScanner(args.onion_list)
            scanner.start()
            
        if args.switch_identity:
            identity_switcher = AutoIdentitySwitcher()
            identity_switcher.start()
            
        if args.test_stability:
            stability_tester = ConnectionStabilityTester()
            stability_tester.start()
            
        if args.monitor_traffic:
            traffic_monitor = TrafficMonitor()
            traffic_monitor.start()
            
        if args.proxy_mode:
            proxy = ProxyMode()
            proxy.start()
            
        if args.create_onion:
            domain_gen = DomainGenerator()
            domain_gen.start()
            
        if args.bypass_captcha:
            captcha_bypass = CaptchaBypass()
            captcha_bypass.start()
            
        if args.find_bridges:
            bridges_finder = BridgesFinder()
            bridges_finder.start()
            
        if args.chat:
            hidden_chat = HiddenChat()
            hidden_chat.start()
            
        if args.smart_ip:
            ai_predictor = AIIPPredictor()
            ai_predictor.start()
            
        if args.spoof_fingerprint:
            fingerprint_spoof = FingerprintSpoofing()
            fingerprint_spoof.start()
            
        if args.fast_tor:
            optimizer = BandwidthOptimizer()
            optimizer.start()
            
        if args.stealth:
            stealth = StealthMode()
            stealth.start()
            
        if args.dns_tor:
            dns_resolver = DNSResolver()
            dns_resolver.start()
            
        if args.exit_country:
            exit_selector = ExitNodeSelector(args.exit_country)
            exit_selector.start()
            
        if args.vpn_mode:
            vpn = VPNMode()
            vpn.start()
            
        if args.auto_restart:
            auto_restart = AutoRestart()
            auto_restart.start()
            
        if args.detect_malicious:
            detector = MaliciousNodeDetector()
            detector.start()
            
        if args.file_share:
            file_share = P2PSharing()
            file_share.start()
            
        if args.visualize:
            visualizer = TorVisualizer()
            visualizer.start()
            
    except KeyboardInterrupt:
        logger.info("Shutting down TorNet...")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
