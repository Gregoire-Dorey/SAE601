# --------------------
# TEST DE LATENCE ROUTEUR AVEC MAC ALÉATOIRE
# --------------------

from scapy.all import *
from scapy.layers.inet import IP, ICMP
from scapy.layers.l2 import Ether, getmacbyip
import time
import random
import final.database as db

# Fonction pour générer une MAC aléatoire
def random_mac():
    return ":".join(f"{random.randint(0x00, 0xFF):02x}" for _ in range(6))

# Fonction pour mesurer la latence vers un routeur Cisco
def latence_routeur(router_name, ip):
    ip_routeur = ip
    num_trames = 500
    latencies = []

    # Trouve l'interface réseau par défaut (à adapter si besoin)
    iface = conf.iface
    # Récupère la MAC de destination via ARP
    try:
        dst_mac = getmacbyip(ip_routeur)
        if dst_mac is None:
            raise Exception("MAC de destination introuvable")
    except:
        print("❌ Impossible de résoudre l'adresse MAC du routeur.")
        return

    print(f"🔍 Début du test de latence vers le routeur {router_name} ({ip_routeur}) avec MAC aléatoires")

    for i in range(num_trames):
        # Génère une MAC source aléatoire
        src_mac = random_mac()
        # Forge la trame Ethernet avec IP/ICMP
        pkt = Ether(src=src_mac, dst=dst_mac) / IP(dst=ip_routeur) / ICMP() / Raw(load="LAT TEST")

        start_time = time.time()
        response = srp1(pkt, timeout=1, verbose=0, iface=iface)
        end_time = time.time()

        if response:
            latency = end_time - start_time
            latencies.append(latency)
            print(f"Trame {i + 1}: Latence = {latency * 1000:.2f} ms | MAC source: {src_mac}")
        else:
            print(f"Trame {i + 1}: ❌ Pas de réponse | MAC source: {src_mac} (ignorée)")

    valid_latencies = [l for l in latencies if l < 1]

    if valid_latencies:
        average_latency = sum(valid_latencies) / len(valid_latencies)
        print(f"\n📊 Latence moyenne (valeurs < 1s) vers le routeur {router_name}: {average_latency * 1000:.2f} ms")
        db.insert_in_base_router(router_name, round(average_latency * 1000, 2), "router_latence")
    else:
        print("\n⚠️ Aucune latence valide mesurée. Rien inséré en base.")

# Exemple d’appel
latence_routeur("9300", "192.168.99.6")
