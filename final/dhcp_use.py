import argparse
import csv
from statistics import mean

import matplotlib.pyplot as plt
from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether
import datetime
import final.database as db

SW_NAME = ""

# Vérification de Windows et chargement de la bonne fonction pour les interfaces
if os.name == 'nt':
    from scapy.arch.windows import get_windows_if_list as get_if_list


# Fonction pour lister les interfaces disponibles
def list_interfaces():
    interfaces = get_if_list()
    print("\n🔹 Interfaces réseau disponibles :")
    for iface in interfaces:
        print(f"  ➜ {iface['name']} ({iface['mac']})")
    print("\nUtilisez `--iface <interface>` pour spécifier une interface.\n")
    exit(0)


# Fonction pour générer une adresse MAC aléatoire valide
def random_mac():
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(random.randint(0, 255) for _ in range(5))


# Fonction pour envoyer une requête DHCP DISCOVER et mesurer le temps de réponse
def dhcp_request(iface, results, index):
    conf.checkIPaddr = False
    mac_address = random_mac()

    dhcp_discover = Ether(src=mac_address, dst="ff:ff:ff:ff:ff:ff") / \
                    IP(src="0.0.0.0", dst="255.255.255.255") / \
                    UDP(sport=68, dport=67) / \
                    BOOTP(op=1, chaddr=mac_address.replace(":", "")) / \
                    DHCP(options=[("message-type", "discover"), "end"])

    print(f"[{index}] Envoi d'une requête DHCP DISCOVER depuis {mac_address}")

    start_time = time.time()
    sendp(dhcp_discover, iface=iface, verbose=False)

    def dhcp_response(pkt):
        if pkt.haslayer(DHCP):
            for opt in pkt[DHCP].options:
                if isinstance(opt, tuple) and opt[0] == "message-type" and opt[1] == 2:  # DHCP OFFER
                    print(f"[{index}] Réponse DHCP OFFER reçue.")
                    return True
        return False

    pkt = sniff(filter="udp and port 67", iface=iface, timeout=15, count=1, lfilter=dhcp_response)
    end_time = time.time()

    if pkt:
        results[index] = end_time - start_time
    else:
        print(f"[{index}] Aucune réponse reçue.")
        results[index] = None


# Fonction principale du benchmark
def benchmark_dhcp(iface, num_clients, duration, save_csv, graphs):
    available_interfaces = [i['name'] for i in get_if_list()]

    if iface not in available_interfaces:
        print(
            f"❌ Erreur : L'interface '{iface}' n'existe pas.\nUtilisez `--list` pour voir les interfaces disponibles.")
        exit(1)

    results = []
    start_time = time.time()

    while time.time() - start_time < duration:
        latencies = [None] * num_clients
        threads = []

        for i in range(num_clients):
            thread = threading.Thread(target=dhcp_request, args=(iface, latencies, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        latencies = [lat for lat in latencies if lat is not None]
        avg_latency = sum(latencies) / len(latencies) if latencies else float('15')

        results.append(avg_latency)
        print(f"🔹 Latence moyenne : {avg_latency:.4f} s")
        time.sleep(1)
    db.insert_in_base(SW_NAME,round(mean(results),2),"dhcp_latence")
    if save_csv:
        save_results_to_csv(results)
    if graphs:
        generate_graph(results)


# Enregistrement des résultats dans un fichier CSV
def save_results_to_csv(results):
    os.makedirs("benchmark_results", exist_ok=True)
    file_path = "benchmark_results/dhcp_benchmark.csv"
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Test", "Latence moyenne (s)"])
        for i, latency in enumerate(results):
            writer.writerow([i + 1, latency])
    print(f"✅ Résultats enregistrés dans {file_path}")


# Génération d'un graphique des résultats
def generate_graph(results):
    os.makedirs("benchmark_results/graphs", exist_ok=True)
    plt.plot(results, marker="o")
    plt.xlabel("Test")
    plt.ylabel("Latence moyenne (s)")
    plt.title("Benchmark DHCP")
    plt.grid()
    date = datetime.datetime.now()
    date = date.strftime("%d-%m-%Y-%H-%M")
    graph_path = f"benchmark_results/graphs/dhcp_benchmark_charge-{date}.png"
    plt.savefig(graph_path)
    plt.show()
    print(f"📊 Graphique enregistré dans {graph_path}")


# Exécution du programme
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark de performances DHCP")
    parser.add_argument("--list", action="store_true", help="Lister les interfaces réseau disponibles")
    parser.add_argument("--iface", help="Interface réseau à utiliser (ex: Ethernet, Wi-Fi)")
    parser.add_argument("--clients", type=int, default=10, help="Nombre de clients à tester simultanément")
    parser.add_argument("--duration", type=int, default=30, help="Durée du test en secondes")
    parser.add_argument("--save-csv", action="store_true", help="Enregistrer les résultats en CSV")
    parser.add_argument("--graphs", action="store_true", help="Générer un graphique des résultats")

    args = parser.parse_args()

    # Si --list est utilisé, on affiche les interfaces et on quitte
    if args.list:
        list_interfaces()

    if not args.iface:
        print(
            "❌ Erreur : Vous devez spécifier une interface avec `--iface <interface>`.\nUtilisez `--list` pour voir les interfaces disponibles.")
        exit(1)

    benchmark_dhcp(args.iface, args.clients, args.duration, args.save_csv, args.graphs)