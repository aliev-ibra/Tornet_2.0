#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import socket
import struct
import threading
import requests
import json
from stem import Signal
from stem.control import Controller
from scapy.all import sniff, IP, TCP, UDP, DNS
import psutil

class TrafficAnalyzer:
    """
    Analyzes Tor network traffic to track requests and responses.
    Shows which exit nodes are being used and provides statistics.
    """
    
    def __init__(self, tor_port=9050, control_port=9051):
        self.logger = logging.getLogger('tornet.analyzer')
        self.tor_port = tor_port
        self.control_port = control_port
        self.exit_nodes = set()
        self.requests_count = 0
        self.responses_by_code = {}
        self.domains_visited = {}
        self.is_running = False
        self.lock = threading.Lock()
        
    def start(self):
        """Start the traffic analyzer"""
        self.logger.info("Starting Tor Traffic Analyzer")
        self.is_running = True
        
        # Start threads for different monitoring tasks
        threads = [
            threading.Thread(target=self._monitor_exit_nodes),
            threading.Thread(target=self._monitor_network_traffic),
            threading.Thread(target=self._display_stats)
        ]
        
        for thread in threads:
            thread.daemon = True
            thread.start()
            
        try:
            # Keep main thread running
            while self.is_running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping Tor Traffic Analyzer")
            self.is_running = False
            
        # Wait for threads to finish
        for thread in threads:
            thread.join(timeout=3)
            
        return True
        
    def _monitor_exit_nodes(self):
        """Monitor which exit nodes are being used"""
        self.logger.info("Monitoring Tor exit nodes")
        
        while self.is_running:
            try:
                with Controller.from_port(port=self.control_port) as controller:
                    controller.authenticate()
                    
                    for circuit in controller.get_circuits():
                        if circuit.status == 'BUILT':
                            # The last relay in the circuit is the exit node (if it's an exit circuit)
                            if circuit.purpose == 'GENERAL':
                                exit_node = circuit.path[-1][0]
                                with self.lock:
                                    self.exit_nodes.add(exit_node)
                                    
            except Exception as e:
                self.logger.error(f"Error monitoring exit nodes: {e}")
                
            time.sleep(10)  # Check every 10 seconds
    
    def _monitor_network_traffic(self):
        """Monitor network traffic using scapy"""
        self.logger.info("Monitoring network traffic")
        
        # Function to process captured packets
        def process_packet(packet):
            if not self.is_running:
                return
                
            try:
                if IP in packet:
                    # Check if this packet is related to Tor
                    if packet.haslayer(TCP) and (packet[TCP].dport == self.tor_port or packet[TCP].sport == self.tor_port):
                        with self.lock:
                            self.requests_count += 1
                            
                    # Try to extract HTTP status code from packets (simplified)
                    if packet.haslayer(TCP) and packet.haslayer(Raw):
                        raw_data = packet[Raw].load.decode('utf-8', errors='ignore')
                        if 'HTTP/' in raw_data and ' ' in raw_data:
                            try:
                                status_line = raw_data.split('\r\n')[0]
                                if 'HTTP/' in status_line and ' ' in status_line:
                                    status_code = status_line.split(' ')[1]
                                    if status_code.isdigit():
                                        with self.lock:
                                            if status_code in self.responses_by_code:
                                                self.responses_by_code[status_code] += 1
                                            else:
                                                self.responses_by_code[status_code] = 1
                            except Exception:
                                pass
                                
                    # Extract domain names from DNS queries
                    if packet.haslayer(DNS) and packet.haslayer(DNSQR):
                        domain = packet[DNSQR].qname.decode('utf-8')
                        with self.lock:
                            if domain in self.domains_visited:
                                self.domains_visited[domain] += 1
                            else:
                                self.domains_visited[domain] = 1
            except Exception as e:
                self.logger.error(f"Error processing packet: {e}")
                
        # Start packet sniffing
        try:
            sniff(filter=f"tcp port {self.tor_port}", prn=process_packet, store=0)
        except Exception as e:
            self.logger.error(f"Error sniffing packets: {e}")
            
    def _display_stats(self):
        """Display traffic statistics periodically"""
        self.logger.info("Starting statistics display")
        
        while self.is_running:
            try:
                with self.lock:
                    # Display statistics
                    self.logger.info("----- Tor Traffic Statistics -----")
                    self.logger.info(f"Total Requests: {self.requests_count}")
                    self.logger.info(f"Unique Exit Nodes: {len(self.exit_nodes)}")
                    
                    if self.responses_by_code:
                        self.logger.info("Response Codes:")
                        for code, count in self.responses_by_code.items():
                            self.logger.info(f"  HTTP {code}: {count}")
                            
                    if self.domains_visited:
                        self.logger.info("Top 5 Domains:")
                        top_domains = sorted(self.domains_visited.items(), key=lambda x: x[1], reverse=True)[:5]
                        for domain, count in top_domains:
                            self.logger.info(f"  {domain}: {count}")
                            
                    self.logger.info("--------------------------------")
                    
            except Exception as e:
                self.logger.error(f"Error displaying stats: {e}")
                
            time.sleep(30)  # Update every 30 seconds

if __name__ == "__main__":
    # For testing this module independently
    logging.basicConfig(level=logging.INFO)
    analyzer = TrafficAnalyzer()
    analyzer.start()
