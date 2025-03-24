# --------------------
# TEST DE LATENCE ROUTEUR
# --------------------

from scapy.all import *
from scapy.layers.inet import IP, ICMP
import time
import final.database as db

# Fonction pour mesurer la latence vers un routeur Cisco
def latence_routeur(router_name, ip):
    ip_routeur = "192.168.99.228"
    num_trames = 500
    latencies = []

    print(f"🔍 Début du test de latence vers le routeur {router_name} ({ip_routeur})")

    for i in range(num_trames):
        start_time = time.time()
        response = sr1(IP(dst=ip_routeur) / ICMP(), timeout=1, verbose=0)
        end_time = time.time()

        if response:
            latency = end_time - start_time
            latencies.append(latency)
            print(f"Trame {i + 1}: Latence = {latency * 1000:.2f} ms")
        else:
            latencies.append(1)
            print(f"Trame {i + 1}: ❌ Pas de réponse, latence fixée à 1s")

    average_latency = sum(latencies) / len(latencies) if latencies else 0
    print(f"\n📊 Latence moyenne vers le routeur {router_name}: {average_latency * 1000:.2f} ms")

    # Insertion en base (ex: table des tests réseau)
    db.insert_in_base_router(router_name, round(average_latency * 1000, 2), "router_latence")

# Exemple d’appel
latence_routeur("2801", "192.168.99.228")
