#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import requests
import threading
import queue
import os
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import socks
import socket
from tqdm import tqdm

class HiddenServiceScanner:
    """
    Scans .onion hidden services to check which ones are active,
    and collects response codes and basic information.
    """
    
    def __init__(self, onion_list_file, threads=10, timeout=30):
        self.logger = logging.getLogger('tornet.scanner')
        self.onion_list_file = onion_list_file
        self.threads = threads
        self.timeout = timeout
        self.results = {}
        self.queue = queue.Queue()
        self.active_count = 0
        self.total_count = 0
        self.lock = threading.Lock()
        
        # Configure requests to use Tor
        self._configure_tor_session()
        
    def _configure_tor_session(self):
        """Configure requests to use Tor SOCKS proxy"""
        self.session = requests.Session()
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        })
        
    def start(self):
        """Start scanning hidden services"""
        self.logger.info(f"Starting Hidden Service Scanner with {self.threads} threads")
        
        # Load onion domains
        if not self._load_onion_domains():
            return False
            
        # Start worker threads
        workers = []
        for _ in range(self.threads):
            worker = threading.Thread(target=self._worker)
            worker.daemon = True
            worker.start()
            workers.append(worker)
            
        # Add a progress bar
        with tqdm(total=self.total_count, desc="Scanning .onion sites") as pbar:
            processed = 0
            while processed < self.total_count:
                with self.lock:
                    new_processed = len(self.results)
                if new_processed > processed:
                    pbar.update(new_processed - processed)
                    processed = new_processed
                time.sleep(0.1)
                
                # Check if all workers are done
                if self.queue.empty() and all(not worker.is_alive() for worker in workers):
                    break
        
        # Save results to file
        self._save_results()
        
        self.logger.info(f"Scan completed. {self.active_count} active out of {self.total_count} onion services.")
        return True
        
    def _load_onion_domains(self):
        """Load .onion domains from file"""
        try:
            if not os.path.exists(self.onion_list_file):
                self.logger.error(f"Onion list file not found: {self.onion_list_file}")
                return False
                
            domains = []
            with open(self.onion_list_file, 'r') as f:
                for line in f:
                    domain = line.strip()
                    if domain and domain.endswith('.onion'):
                        # Ensure domain has protocol
                        if not domain.startswith('http'):
                            domain = f"http://{domain}"
                        domains.append(domain)
                        
            self.total_count = len(domains)
            self.logger.info(f"Loaded {self.total_count} .onion domains to scan")
            
            # Add domains to the queue
            for domain in domains:
                self.queue.put(domain)
                
            return True
        except Exception as e:
            self.logger.error(f"Error loading onion domains: {e}")
            return False
            
    def _worker(self):
        """Worker thread that processes domains from the queue"""
        while True:
            try:
                # Get a domain from the queue
                domain = self.queue.get(block=False)
            except queue.Empty:
                # No more domains to process
                break
                
            try:
                # Scan the domain
                result = self._scan_domain(domain)
                
                with self.lock:
                    self.results[domain] = result
                    if result['status'] == 'active':
                        self.active_count += 1
            except Exception as e:
                self.logger.error(f"Error scanning {domain}: {e}")
                with self.lock:
                    self.results[domain] = {
                        'status': 'error',
                        'error': str(e)
                    }
                    
            finally:
                self.queue.task_done()
                
    def _scan_domain(self, url):
        """Scan a single onion domain"""
        result = {
            'status': 'inactive',
            'response_code': None,
            'title': None,
            'server': None,
            'content_type': None,
            'links': 0,
            'scan_time': time.time()
        }
        
        try:
            # Make the request
            response = self.session.get(url, timeout=self.timeout)
            
            # Parse the response
            result['response_code'] = response.status_code
            result['status'] = 'active'
            result['server'] = response.headers.get('Server', 'Unknown')
            result['content_type'] = response.headers.get('Content-Type', 'Unknown')
            
            # Try to parse HTML
            if 'text/html' in result['content_type']:
                soup = BeautifulSoup(response.text, 'html.parser')
                result['title'] = soup.title.text.strip() if soup.title else 'No title'
                result['links'] = len(soup.find_all('a'))
                
        except requests.exceptions.RequestException as e:
            # Site is not responding
            return result
            
        return result
        
    def _save_results(self):
        """Save scan results to a file"""
        output_file = f"onion_scan_results_{int(time.time())}.txt"
        
        with open(output_file, 'w') as f:
            f.write(f"# Onion Service Scan Results\n")
            f.write(f"# Total scanned: {self.total_count}\n")
            f.write(f"# Active: {self.active_count}\n")
            f.write(f"# Scan time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # Write active sites first
            f.write("## Active Sites\n\n")
            for domain, result in sorted(self.results.items()):
                if result['status'] == 'active':
                    f.write(f"URL: {domain}\n")
                    f.write(f"Response Code: {result['response_code']}\n")
                    f.write(f"Title: {result['title']}\n")
                    f.write(f"Server: {result['server']}\n")
                    f.write(f"Content Type: {result['content_type']}\n")
                    f.write(f"Links: {result['links']}\n")
                    f.write("\n")
                    
            # Write inactive sites
            f.write("## Inactive Sites\n\n")
            for domain, result in sorted(self.results.items()):
                if result['status'] == 'inactive':
                    f.write(f"URL: {domain}\n")
                    
            # Write error sites
            f.write("## Error Sites\n\n")
            for domain, result in sorted(self.results.items()):
                if result['status'] ==
