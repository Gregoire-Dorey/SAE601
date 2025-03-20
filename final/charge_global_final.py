# --------------------
# TEST DE CHARGE GLOBAL
# --------------------

from scapy.all import *
import time

from scapy.layers.inet import TCP, UDP, ICMP, IP

# Paramètres du test
TARGET_IP = "192.168.99.203"  # Adresse IP du switch ou d'un hôte derrière
PORT = 80  # Port cible pour le trafic TCP/UDP
PACKETS = 10000  # Nombre total de paquets à envoyer


# Fonction pour créer et envoyer les trois types de paquets en séquence
def send_combined_flood():
    # Création des paquets
    tcp_packet = IP(dst=TARGET_IP) / TCP(dport=PORT, flags="S") / Raw(load="TCP TEST")
    udp_packet = IP(dst=TARGET_IP) / UDP(dport=PORT) / Raw(load="UDP TEST")
    icmp_packet = IP(dst=TARGET_IP) / ICMP() / Raw(load="PING TEST")

    print("🚀 Démarrage de l'envoi des paquets...")

    # Envoyer les paquets en séquence
    packets_sent = 0
    start_time = time.time()

    while packets_sent < PACKETS:
        # Envoyer un paquet TCP
        send(tcp_packet, count=1, verbose=False)
        packets_sent += 1

        # Envoyer un paquet UDP
        send(udp_packet, count=1, verbose=False)
        packets_sent += 1

        # Envoyer un paquet ICMP
        send(icmp_packet, count=1, verbose=False)
        packets_sent += 1

        # Afficher la progression tous les 300 paquets
        if packets_sent % 300 == 0:
            print(f"Progression: {packets_sent}/{PACKETS} paquets envoyés")

    total_time = time.time() - start_time
    print(f"✅ Envoi terminé: {packets_sent} paquets envoyés en {total_time:.2f} secondes")
    print(f"Taux d'envoi: {packets_sent / total_time:.2f} paquets/seconde")

    return total_time


send_combined_flood()
