import argparse
import time
import csv
import os
import threading
import matplotlib.pyplot as plt
from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether


# Fonction pour envoyer une requête DHCP DISCOVER et mesurer le temps de réponse
def dhcp_request(server_ip, results, index):
    conf.checkIPaddr = False
    iface = conf.iface  # Utiliser l'interface par défaut
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(sport=68,
                                                                                                    dport=67) / BOOTP(
        op=1, chaddr=RandMAC()) / DHCP(options=[("message-type", "discover"), "end"])

    print(f"Envoi de la requête DHCP DISCOVER : {dhcp_discover.show()}")  # Affiche la requête envoyée
    start_time = time.time()
    sendp(dhcp_discover, iface=iface, verbose=False)

    def dhcp_response(pkt):
        if pkt.haslayer(DHCP):
            # Affichage de la réponse pour vérifier
            print(f"Réponse DHCP reçue : {pkt[DHCP].options}")
            return pkt[DHCP].options[0][1] == 2  # Vérifie si c'est un DHCP OFFER
        return False

    # Augmenter le timeout à 10 secondes pour donner plus de temps à la réponse
    pkt = sniff(filter="udp", iface=iface, timeout=10, count=1, lfilter=dhcp_response)
    end_time = time.time()

    if pkt:
        results[index] = end_time - start_time
    else:
        results[index] = None  # Pas de réponse reçue


def benchmark_dhcp(server_ip, num_clients, duration, save_csv, graphs):
    results = []
    start_time = time.time()

    while time.time() - start_time < duration:
        latencies = [None] * num_clients
        threads = []
        for i in range(num_clients):
            thread = threading.Thread(target=dhcp_request, args=(server_ip, latencies, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        latencies = [lat for lat in latencies if lat is not None]  # Exclure les requêtes sans réponse
        if latencies:
            avg_latency = sum(latencies) / len(latencies)
        else:
            avg_latency = float('inf')  # Aucun paquet reçu, latence infinie

        results.append(avg_latency)
        print(f"Latence moyenne : {avg_latency:.4f} s")
        time.sleep(1)

    if save_csv:
        save_results_to_csv(results)
    if graphs:
        generate_graph(results)


def save_results_to_csv(results):
    os.makedirs("benchmark_results", exist_ok=True)
    file_path = "benchmark_results/dhcp_benchmark.csv"
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Test", "Latence moyenne (s)"])
        for i, latency in enumerate(results):
            writer.writerow([i + 1, latency])
    print(f"Résultats enregistrés dans {file_path}")


def generate_graph(results):
    os.makedirs("benchmark_results/graphs", exist_ok=True)
    plt.plot(results, marker="o")
    plt.xlabel("Test")
    plt.ylabel("Latence moyenne (s)")
    plt.title("Benchmark DHCP")
    plt.grid()
    graph_path = "benchmark_results/graphs/dhcp_benchmark.png"
    plt.savefig(graph_path)
    plt.show()
    print(f"Graphique enregistré dans {graph_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark de performances DHCP")
    parser.add_argument("--server", required=True, help="Adresse IP du serveur DHCP à tester")
    parser.add_argument("--clients", type=int, default=10, help="Nombre de clients à tester simultanément")
    parser.add_argument("--duration", type=int, default=30, help="Durée du test en secondes")
    parser.add_argument("--save-csv", action="store_true", help="Enregistrer les résultats en CSV")
    parser.add_argument("--graphs", action="store_true", help="Générer un graphique des résultats")

    args = parser.parse_args()
    benchmark_dhcp(args.server, args.clients, args.duration, args.save_csv, args.graphs)
