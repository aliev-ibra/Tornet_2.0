# modules/ai_ip_predictor.py
import random
import time

class IPPredictor:
    def __init__(self):
        self.ip_history = []
        self.latency_history = []

    def simulate_ip_change(self):
        # Simulate IP change and latency
        new_ip = f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}"
        latency = random.randint(10, 500)
        self.ip_history.append(new_ip)
        self.latency_history.append(latency)
        return new_ip, latency

    def recommend_stable_node(self):
        # Recommend the IP with the lowest latency
        if not self.latency_history:
            return None
        min_latency_index = self.latency_history.index(min(self.latency_history))
        return self.ip_history[min_latency_index]

if __name__ == "__main__":
    predictor = IPPredictor()
    for _ in range(5):
        ip, latency = predictor.simulate_ip_change()
        print(f"New IP: {ip}, Latency: {latency}ms")
        time.sleep(1)
    print(f"Recommended Stable Node: {predictor.recommend_stable_node()}")
