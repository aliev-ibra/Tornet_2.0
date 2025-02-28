#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import requests
import threading
from stem import Signal
from stem.control import Controller

class AutoIdentitySwitcher:
    """
    Automatically switch Tor identity (circuit) for each request,
    providing a new IP address for enhanced anonymity.
    """
    
    def __init__(self, control_port=9051, password=None, switch_delay=10):
        self.logger = logging.getLogger('tornet.identity_switcher')
        self.control_port = control_port
        self.password = password
        self.switch_delay = switch_delay
        self.running = False
        self.last_ip = None
        self.identity_count = 0
        self.lock = threading.Lock()
        
    def start(self):
        """Start the Auto Identity Switcher"""
        self.logger.info("Starting Auto Identity Switcher")
        self.running = True
        
        # Test connection to Tor Control Port
        if not self._test_tor_control():
            self.logger.error("Could not connect to Tor Control Port. Make sure Tor is running and properly configured.")
            return False
            
        # Start the identity switching thread
        switch_thread = threading.Thread(target=self._switch_identity_loop)
        switch_thread.daemon = True
        switch_thread.start()
        
        # Start the IP display thread
        display_thread = threading.Thread(target=self._display_current_ip)
        display_thread.daemon = True
        display_thread.start()
        
        try:
            # Keep the main thread running
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping Auto Identity Switcher")
            self.running = False
            
        return True
        
    def _test_tor_control(self):
        """Test connection to Tor Control Port"""
        try:
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate(password=self.password)
                self.logger.info(f"Successfully connected to Tor Control Port (version: {controller.get_version()})")
                return True
        except Exception as e:
            self.logger.error(f"Error connecting to Tor Control Port: {e}")
            return False
            
    def _switch_identity_loop(self):
        """Continuously switch Tor identity at specified intervals"""
        while self.running:
            try:
                self._switch_identity()
                time.sleep(self.switch_delay)
            except Exception as e:
                self.logger.error(f"Error in identity switch loop: {e}")
                time.sleep(5)  # Wait before retrying
                
    def _switch_identity(self):
        """Switch the Tor identity and get a new circuit"""
        try:
            with Controller.from_port(port=self.control_port) as controller:
                controller.authenticate(password=self.password)
                
                # Send NEWNYM signal to switch identity
                controller.signal(Signal.NEWNYM)
                
                with self.lock:
                    self.identity_count += 1
                    
                self.logger.info(f"Identity switched (#{self.identity_count})")
                return True
        except Exception as e:
            self.logger.error(f"Error switching identity: {e}")
            return False
            
    def _display_current_ip(self):
        """Periodically display the current Tor exit node IP"""
        while self.running:
            try:
                current_ip = self._get_current_ip()
                
                if current_ip != self.last_ip:
                    self.logger.info(f"Current Tor exit node IP: {current_ip}")
                    self.last_ip = current_ip
                    
            except Exception as e:
                self.logger.error(f"Error checking current IP: {e}")
                
            time.sleep(5)  # Check every 5 seconds
            
    def _get_current_ip(self):
        """Get the current Tor exit node IP address"""
        try:
            # Configure request to use Tor
            proxies = {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050'
            }
            
            # Request IP from a service
            response = requests.get('https://check.torproject.org/api/ip', proxies=proxies, timeout=30)
            data = response.json()
            
            return data.get('IP', 'Unknown')
        except Exception as e:
            self.logger.error(f"Error getting current IP: {e}")
            return "Error"
            
    def switch_identity_now(self):
        """Manually switch identity (for API use)"""
        return self._switch_identity()

if __name__ == "__main__":
    # For testing this module independently
    logging.basicConfig(level=logging.INFO)
    switcher = AutoIdentitySwitcher(switch_delay=15)
    switcher.start()
