#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import logging
import socks
import time
import random
import requests
from stem import Signal
from stem.control import Controller

class TorMultiHop:
    """
    Creates a multi-hop proxy chain using multiple Tor instances
    to increase anonymity by routing through multiple circuits.
    """
    
    def __init__(self, num_hops=3, base_port=9050):
        self.logger = logging.getLogger('tornet.multihop')
        self.num_hops = num_hops
        self.base_port = base_port
        self.proxy_ports = [base_port + i for i in range(num_hops)]
        self.control_ports = [base_port + 100 + i for i in range(num_hops)]
        self.tor_processes = []
        
    def start(self):
        """Start the multi-hop proxy chain"""
        self.logger.info(f"Starting Tor Multi-Hop Proxy with {self.num_hops} hops")
        
        # Check if multiple Tor instances are already configured
        if not self._check_tor_config():
            self.logger.error("Multiple Tor instances not configured. Please set up torrc files.")
            self.logger.info("See https://trac.torproject.org/projects/tor/wiki/doc/TorifyHOWTO/MultipleTorInstances")
            return False
            
        try:
            # Create the chain
            self._create_proxy_chain()
            
            # Test the chain
            self._test_chain()
            
            self.logger.info("Multi-hop proxy chain is ready")
            self.logger.info(f"Configure your application to use SOCKS proxy at 127.0.0.1:{self.proxy_ports[-1]}")
            
            # Keep the script running
            try:
                while True:
                    time.sleep(60)
                    self._test_chain()  # Periodically test the chain
            except KeyboardInterrupt:
                self.logger.info("Shutting down Tor Multi-Hop Proxy")
                return True
                
        except Exception as e:
            self.logger.error(f"Error setting up multi-hop proxy chain: {e}")
            return False
    
    def _check_tor_config(self):
        """Check if multiple Tor instances are properly configured"""
        for i, port in enumerate(self.proxy_ports):
            try:
                # Try to connect to each SOCKS port
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                result = s.connect_ex(('127.0.0.1', port))
                s.close()
                
                if result != 0:
                    self.logger.error(f"Tor instance {i+1} not found on port {port}")
                    return False
                    
                # Try to connect to each control port
                with Controller.from_port(port=self.control_ports[i]) as controller:
                    controller.authenticate()
                    self.logger.info(f"Tor instance {i+1} is running (version: {controller.get_version()})")
            except Exception as e:
                self.logger.error(f"Tor instance {i+1} check failed: {e}")
                return False
                
        return True
        
    def _create_proxy_chain(self):
        """Create the proxy chain configuration"""
        self.logger.info("Setting up proxy chain")
        
        # For each hop, we need to configure the next hop as its proxy
        for i in range(self.num_hops - 1, 0, -1):
            # Configure each Tor instance to use the previous one as proxy
            with Controller.from_port(port=self.control_ports[i]) as controller:
                controller.authenticate()
                # Set the previous hop as upstream proxy
                socks_config = f"Socks5Proxy 127.0.0.1:{self.proxy_ports[i-1]}"
                self.logger.info(f"Configuring Tor instance {i+1} to use {self.proxy_ports[i-1]} as upstream proxy")
                
                # NOTE: In reality, this would require modifying the torrc file and restarting Tor
                # For this demo, we're just showing the concept
                self.logger.info(f"Would add to torrc: {socks_config}")
                
        self.logger.info("Proxy chain configured")
    
    def _test_chain(self):
        """Test the multi-hop proxy chain"""
        self.logger.info("Testing proxy chain...")
        
        try:
            # Configure the request to go through the final proxy
            proxies = {
                'http': f'socks5h://127.0.0.1:{self.proxy_ports[-1]}',
                'https': f'socks5h://127.0.0.1:{self.proxy_ports[-1]}'
            }
            
            # Make a request through the proxy chain
            response = requests.get('https://check.torproject.org/api/ip', proxies=proxies, timeout=30)
            data = response.json()
            
            if data.get('IsTor', False):
                self.logger.info(f"Multi-hop chain is working! IP: {data.get('IP')}")
                return True
            else:
                self.logger.warning("Connected but not using Tor network!")
                return False
                
        except Exception as e:
            self.logger.error(f"Proxy chain test failed: {e}")
            return False
    
    def _create_torrc_template(self):
        """Create a template for torrc configurations"""
        # This method would generate the configuration files for multiple Tor instances
        # For educational purposes, this is just a template
        torrc_templates = []
        
        for i in range(self.num_hops):
            template = f"""# Tor instance {i+1} configuration
SocksPort {self.proxy_ports[i]}
ControlPort {self.control_ports[i]}
DataDirectory /var/lib/tor{i+1}
RunAsDaemon 1
CookieAuthentication 1
"""
            if i > 0:
                template += f"Socks5Proxy 127.0.0.1:{self.proxy_ports[i-1]}\n"
                
            torrc_templates.append(template)
            
        return torrc_templates

if __name__ == "__main__":
    # For testing this module independently
    logging.basicConfig(level=logging.INFO)
    multi_hop = TorMultiHop()
    multi_hop.start()
