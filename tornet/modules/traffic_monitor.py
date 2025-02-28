#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import threading
import subprocess
import re
import os
import platform
import psutil
from collections import deque

class TrafficMonitor:
    """
    Monitors Tor network traffic showing upload and download
    rates in real-time.
    """
    
    def __init__(self, update_interval=1, history_size=60):
        self.logger = logging.getLogger('tornet.traffic_monitor')
        self.update_interval = update_interval  # seconds
        self.history_size = history_size  # number of data points to keep
        self.running = False
        self.tor_pid = None
        
        # Data storage
        self.download_history = deque(maxlen=history_size)
        self.upload_history = deque(maxlen=history_size)
        self.timestamp_history = deque(maxlen=history_size)
        
        # Initialize with zeros
        for _ in range(history_size):
            self.download_history.append(0)
            self.upload_history.append(0)
            self.timestamp_history.append(time.time() - (history_size - _) * update_interval)
            
    def start(self):
        """Start monitoring Tor traffic"""
        self.logger.info("Starting Tor Traffic Monitor")
        
        # Find Tor process
        if not self._find_tor_process():
            self.logger.error("Could not find Tor process. Make sure Tor is running.")
            return False
            
        self.running = True
        
        # Start monitoring thread
        monitor_thread = threading.Thread(target=self._monitor_loop)
        monitor_thread.daemon = True
        monitor_thread.start()
        
        try:
            # Keep the main thread running
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping Tor Traffic Monitor")
            self.running = False
            
        return True
        
    def _find_tor_process(self):
        """Find the Tor process ID"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and ('tor' in proc.info['name'].lower()):
                    self.tor_pid = proc.info['pid']
                    self.logger.info(f"Found Tor process (PID: {self.tor_pid})")
                    return True
            
            self.logger.warning("Tor process not found, will monitor system-wide traffic")
            return True  # Continue anyway
        except Exception as e:
            self.logger.error(f"Error finding Tor process: {e}")
            return False
            
    def _monitor_loop(self):
        """Main monitoring loop"""
        self.logger.info("Traffic monitoring started")
        
        # Initialize counters
        prev_download = 0
        prev_upload = 0
        start_time = time.time()
        
        if self.tor_pid:
            # Get initial network stats for Tor process
            try:
                tor_proc = psutil.Process(self.tor_pid)
                io_counters = tor_proc.io_counters()
                prev_download = io_counters.read_bytes
                prev_upload = io_counters.write_bytes
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self.logger.error(f"Cannot access Tor process stats: {e}")
                self.tor_pid = None  # Fall back to system monitoring
                
        if not self.tor_pid:
            # Get initial system-wide network stats
            io_counters = psutil.net_io_counters()
            prev_download = io_counters.bytes_recv
            prev_upload = io_counters.bytes_sent
            
        while self.running:
            try:
                # Sleep until next update
                time.sleep(self.update_interval)
                current_time = time.time()
                
                # Get current network stats
                if self.tor_pid:
                    try:
                        tor_proc = psutil.Process(self.tor_pid)
                        io_counters = tor_proc.io_counters()
                        curr_download = io_counters.read_bytes
                        curr_upload = io_counters.write_bytes
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        self.logger.warning("Lost access to Tor process, switching to system monitoring")
                        self.tor_pid = None
                        io_counters = psutil.net_io_counters()
                        curr_download = io_counters.bytes_recv
                        curr_upload = io_counters.bytes_sent
                else:
                    io_counters = psutil.net_io_counters()
                    curr_download = io_counters.bytes_recv
                    curr_upload = io_counters.bytes_sent
                    
                # Calculate rates
                download_rate = (curr_download - prev_download) / self.update_interval
                upload_rate = (curr_upload - prev_upload) / self.update_interval
                
                # Store the data
                self.download_history.append(download_rate)
                self.upload_history.append(upload_rate)

