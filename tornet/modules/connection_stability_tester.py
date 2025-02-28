#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import time
import threading
import requests
import statistics
import datetime
import matplotlib.pyplot as plt
import numpy as np
from stem import Signal
from stem.control import Controller

class ConnectionStabilityTester:
    """
    Tests the stability and speed of Tor connections by measuring
    response times and conducting speed tests.
    """
    
    def __init__(self, test_interval=300, test_urls=None, test_count=10):
        self.logger = logging.getLogger('tornet.stability_tester')
        self.test_interval = test_interval  # Time between tests in seconds
        self.test_count = test_count  # Number of tests in each batch
        self.test_urls = test_urls or [
            'https://check.torproject.org/',
            'https://duckduckgo.com/',
            'https://en.wikipedia.org/',
        ]
        self.results = []
        self.running = False
        
    def start(self):
        """Start the connection stability tester"""
        self.logger.info("Starting Tor Connection Stability Tester")
        self.running = True
        
        # Configure request session
        self.session = requests.Session()
        self.session.proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
        })
        
        # Start the testing thread
        test_thread = threading.Thread(target=self._test_loop)
        test_thread.daemon = True
        test_thread.start()
        
        try:
            # Keep the main thread running
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("Stopping Connection Stability Tester")
            self.running = False
            
        # Create final report
        if self.results:
            self._generate_report()
            
        return True
        
    def _test_loop(self):
        """Run tests periodically"""
        while self.running:
            try:
                # Run a batch of tests
                batch_results = self._run_test_batch()
                
                # Store the results
                self.results.append(batch_results)
                
                # Display summary of the latest test
                self._display_batch_summary(batch_results)
                
            except Exception as e:
                self.logger.error(f"Error in test loop: {e}")
                
            # Sleep until next test
            self.logger.info(f"Next test in {self.test_interval} seconds")
            time.sleep(self.test_interval)
            
    def _run_test_batch(self):
        """Run a batch of tests and return the results"""
        self.logger.info("Starting test batch")
        batch_start_time = time.time()
        
        batch_results = {
            'timestamp': datetime.datetime.now().isoformat(),
            'tests': [],
            'summary': {}
        }
        
        # Run tests for each URL
        for url in self.test_urls:
            url_results = []
            
            for i in range(self.test_count):
                try:
                    # Measure response time
                    start_time = time.time()
                    response = self.session.get(url, timeout=30)
                    response_time = time.time() - start_time
                    
                    url_results.append({
                        'attempt': i + 1,
                        'status_code': response.status_code,
                        'response_time': response_time,
                        'success': response.status_code == 200
                    })
                    
                except Exception as e:
                    url_results.append({
                        'attempt': i + 1,
                        'status_code': None,
                        'response_time': None,
                        'success': False,
                        'error': str(e)
                    })
                    
                # Small delay between tests
                time.sleep(1)
                
            # Calculate statistics for this URL
            success_count = sum(1 for r in url_results if r['success'])
            response_times = [r['response_time'] for r in url_results if r['response_time'] is not None]
            
            url_summary = {
                'url': url,
                'success_rate': success_count / self.test_count if self.test_count > 0 else 0,
                'min_time': min(response_times) if response_times else None,
                'max_time': max(response_times) if response_times else None,
                'avg_time': statistics.mean(response_times) if response_times else None,
                'median_time': statistics.median(response_times) if response_times else None
            }
            
            batch_results['tests'].append({
                'url': url,
                'results': url_results,
                'summary': url_summary
            })
            
        # Calculate overall batch statistics
        all_response_times = []
        all_success_count = 0
        
        for test in batch_results['tests']:
            all_success_count += sum(1 for r in test['results'] if r['success'])
            all_response_times.extend([r['response_time'] for r in test['results'] if r['response_time'] is not None])
            
        batch_results['summary'] = {
            'total_tests': len(self.test_urls) * self.test_count,
            'success_rate': all_success_count / (len(self.test_urls) * self.test_count) if self.test_count > 0 else 0,
            'min_time': min(all_response_times) if all_response_times else None,
            'max_time': max(all_response_times) if all_response_times else None,
            'avg_time': statistics.mean(all_response_times) if all_response_times else None,
            'median_time': statistics.median(all_response_times) if all_response_times else None,
            'batch_duration': time.time() - batch_start_time
        }
        
        return batch_results
        
    def _display_batch_summary(self, batch_results):
        """Display a summary of the test batch results"""
        self.logger.info("----- Tor Connection Test Results -----")
        self.logger.info(f"Time: {batch_results['timestamp']}")
        self.logger.info(f"Overall Success Rate: {batch_results['summary']['success_rate']*100:.1f}%")
        
        if batch_results['summary']['avg_time']:
            self.logger.info(f"Average Response Time: {batch_results['summary']['avg_time']*1000:.1f}ms")
            self.logger.info(f"Median Response Time: {batch_results['summary']['median_time']*1000:.1f}ms")
            
        self.logger.info("\nResults by URL:")
        for test in batch_results['tests']:
            self.logger.info(f"  {test['url']}:")
            self.logger.info(f"    Success Rate: {test['summary']['success_rate']*100:.1f}%")
            if test['summary']['avg_time']:
                self.logger.info(f"    Average Time: {test['summary']['avg_time']*1000:.1f}ms")
        self.logger.info("---------------------------------------")
        
    def _generate_report(self):
        """Generate a detailed report with graphs"""
        report_file = f"tor_stability_report_{int(time.time())}.txt"
        
        with open(report_file, 'w') as f:
            f.write("# Tor Connection Stability Report\n\n")
            f.write(f"Report Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Test Batches: {len(self.results)}\n")
            f.write(f"Test URLs: {', '.join(self.test_urls)}\n\n")
            
            # Overall statistics
            all_success_rates = [batch['summary']['success_rate'] for batch in self.results]
            all_avg_times = [batch['summary']['avg_time'] for batch in self.results if batch['summary']['avg_time']]
            
            f.write("## Overall Statistics\n\n")
            f.write(f"Average Success Rate: {statistics.mean(all_success_rates)*100:.1f}%\n")
            if all_avg_times:
                f.write(f"Average Response Time: {statistics.mean(all_avg_times)*1000:.1f}ms\n")
                f.write(f"Min Response Time: {min(all_avg_times)*1000:.1f}ms\n")
                f.write(f"Max Response Time: {max(all_avg_times)*1000:.1f}ms\n")
            
            # URL-specific statistics
            f.write("\n## URL-Specific Statistics\n\n")
            for i, url in enumerate(self.test_urls):
                url_success_rates = [batch['tests'][i]['summary']['success_rate'] for batch in self.results]
                url_avg_times = [batch['tests'][i]['summary']['avg_time'] for batch in self.results 
                                if batch['tests'][i]['summary']['avg_time']]
                
                f.write(f"### {url}\n\n")
                f.write(f"Average Success Rate: {statistics.mean(url_success_rates)*100:.1f}%\n")
                if url_avg_times:
                    f.write(f"Average Response Time: {statistics.mean(url_avg_times)*1000:.1f}ms\n")
                    f.write(f"Min Response Time: {min(url_avg_times)*1000:.1f}ms\n")
                    f.write(f"Max Response Time: {max(url_avg_times)*1000:.1f}ms\n")
                f.write("\n")
                
        self.logger.info(f"Stability report saved to {report_file}")
        
        # Generate graphs
        self._generate_graphs()
        
    def _generate_graphs(self):
        """Generate graphs of the test results"""
        try:
            plt.figure(figsize=(12, 8))
            
            # Plot success rates
            plt.subplot(2, 1, 1)
            timestamps = [datetime.datetime.fromisoformat(batch['timestamp']) for batch in self.results]
            success_rates = [batch['summary']['success_rate'] * 100 for batch in self.results]
            
            plt.plot(timestamps, success_rates, 'b-', label='Success Rate (%)')
            plt.xlabel('Time')
            plt.ylabel('Success Rate (%)')
            plt.title('Tor Connection Success Rate Over Time')
            plt.grid(True)
            plt.legend()
            
            # Plot response times
            plt.subplot(2, 1, 2)
            avg_times = [batch['summary']['avg_time'] * 1000 if batch['summary']['avg_time'] else 0 
                        for batch in self.results]
            
            plt.plot(timestamps, avg_times, 'r-', label='Avg Response Time (ms)')
            plt.xlabel('Time')
            plt.ylabel('Response Time (ms)')
            plt.title('Tor Connection Response Time Over Time')
            plt.grid(True)
            plt.legend()
            
            plt.tight_layout()
            plt.savefig(f"tor_stability_graph_{int(time.time())}.png")
            plt.close()
            
            self.logger.info(f"Stability graphs generated")
        except Exception as e:
            self.logger.error(f"Error generating graphs: {e}")

if __name__ == "__main__":
    # For testing this module independently
    logging.basicConfig(level=logging.INFO)
    tester = ConnectionStabilityTester(test_interval=60)
    tester.start()
