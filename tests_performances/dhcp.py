import os
import csv
import argparse
import matplotlib.pyplot as plt


class DHCPBenchmark:
    def __init__(self, server_ip, port, concurrent_clients, test_duration, incremental=False, max_clients=None,
                 increment_step=5, increment_interval=10):
        self.server_ip = server_ip
        self.port = port
        self.concurrent_clients = concurrent_clients
        self.test_duration = test_duration
        self.incremental = incremental
        self.max_clients = max_clients
        self.increment_step = increment_step
        self.increment_interval = increment_interval

    def run_benchmark(self):
        # Simulation de l'exécution du benchmark DHCP
        report = {
            "server_ip": self.server_ip,
            "concurrent_clients": self.concurrent_clients,
            "test_duration_seconds": self.test_duration,
            "total_requests": 1000,
            "successful_responses": 950,
            "failed_requests": 50,
            "success_rate_percent": 95.0,
            "requests_per_second": 33.3,
            "avg_response_time_ms": 15.2,
            "min_response_time_ms": 10.1,
            "max_response_time_ms": 30.5,
            "standard_deviation_ms": 5.6,
            "percentile_50th_ms": 14.0,
            "percentile_90th_ms": 25.0,
            "percentile_99th_ms": 29.0,
            "error_details": {"Timeout": 30, "No Response": 20},
            "incremental_results": {},
            "response_time_bins": self.create_histogram_bins([10, 12, 15, 18, 20, 22, 25, 30], 5),
        }
        return report

    def create_histogram_bins(self, response_times, num_bins=10):
        if not response_times:
            return {}

        min_time, max_time = min(response_times), max(response_times)
        bin_width = (max_time - min_time) / num_bins if max_time > min_time else 1
        bins = {}

        for i in range(num_bins):
            lower = min_time + i * bin_width
            upper = lower + bin_width
            label = f"{lower:.2f}-{upper:.2f}"
            count = sum(1 for t in response_times if lower <= t < upper)
            bins[label] = count

        bins[list(bins.keys())[-1]] += sum(1 for t in response_times if t == max_time)
        return bins


def main():
    parser = argparse.ArgumentParser(description='Benchmark DHCP avec analyse des temps de réponse')
    parser.add_argument('--server', '-s', required=True, help='Adresse IP du serveur DHCP')
    parser.add_argument('--port', '-p', type=int, default=67, help='Port du serveur DHCP')
    parser.add_argument('--clients', '-c', type=int, default=10, help='Nombre de clients concurrents')
    parser.add_argument('--duration', '-d', type=int, default=30, help='Durée du test en secondes')
    args = parser.parse_args()

    print(f"Démarrage du benchmark DHCP sur {args.server}:{args.port}")
    benchmark = DHCPBenchmark(args.server, args.port, args.clients, args.duration)
    report = benchmark.run_benchmark()
    print(report)


if __name__ == "__main__":
    main()
