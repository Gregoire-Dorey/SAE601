# --------------------
# TEST DE CHARGE GLOBAL
# --------------------

# Importation des modules nécessaires dont scapy pour forger des paquets
from scapy.all import *
import multiprocessing
import time
from scapy.layers.inet import IP, UDP, TCP, ICMP

# Paramètres du test
TARGET_IP = "192.168.111.178"  # Adresse IP du switch ou d'un hôte derrière
PORT = 80  # Port cible pour le trafic TCP/UDP
PACKETS = 10000  # Nombre de paquets envoyés par process
PROCESSES = 5  # Nombre de processus pour générer du trafic en parallèle

# Fonction pour envoyer des paquets TCP
def send_tcp_flood():
    packet = IP(dst=TARGET_IP) / TCP(dport=PORT, flags="S") / Raw(load="TCP TEST")
    print(packet.summary())
    send(packet, count=PACKETS, inter=0.0001, verbose=False)

# Fonction pour envoyer des paquets UDP
def send_udp_flood():
    packet = IP(dst=TARGET_IP) / UDP(dport=PORT) / Raw(load="UDP TEST")
    print(packet.summary())
    send(packet, count=PACKETS, inter=0.0001, verbose=False)

# Fonction pour envoyer des pings (ICMP)
def send_icmp_flood():
    packet = IP(dst=TARGET_IP) / ICMP() / Raw(load="PING TEST")
    print(packet.summary())
    send(packet, count=PACKETS, inter=0.0001, verbose=False)

# Fonction pour lancer plusieurs processus en parallèle
def launch_charge():
    processes = []
    # Lancement des processus pour chaque paquets
    for _ in range(PROCESSES):
        processes.append(multiprocessing.Process(target=send_tcp_flood))
        processes.append(multiprocessing.Process(target=send_udp_flood))
        processes.append(multiprocessing.Process(target=send_icmp_flood))
    # Démarrer les processus
    for process in processes:
        process.start()
    # Attendre que tous les processus se terminent
    for process in processes:
        process.join()

# Lancement du test de charge
if __name__ == "__main__":
    print("Démarrage du test de charge...")
    # Enregistre le temps de début
    start_time = time.time()
    # Lance la fonction pour envoyer la charge
    launch_charge()
    # Affichage du temps total écoulé
    print(f"Test terminé en {time.time() - start_time:.2f} secondes")
