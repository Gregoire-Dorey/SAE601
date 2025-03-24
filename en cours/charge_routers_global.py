# --------------------
# TEST DE CHARGE ROUTEUR CISCO
# --------------------

from scapy.all import *
import time
from scapy.layers.inet import TCP, UDP, ICMP, IP

# Paramètres du test
TARGET_IP = "192.168.99.228"  # Adresse IP du routeur Cisco
PORT = 12345  # Port arbitraire, le routeur ne l'écoute pas forcément, on vise l'interface
PACKETS = 10000  # Nombre total de paquets à envoyer

# Fonction pour envoyer différents types de paquets vers le routeur
def send_router_flood():
    # Création de paquets de test
    tcp_packet = IP(dst=TARGET_IP) / TCP(dport=PORT, flags="S") / Raw(load="ROUTER TCP FLOOD")
    udp_packet = IP(dst=TARGET_IP) / UDP(dport=PORT) / Raw(load="ROUTER UDP FLOOD")
    icmp_packet = IP(dst=TARGET_IP) / ICMP(type=8) / Raw(load="ROUTER ICMP FLOOD")  # Echo Request

    print("🚀 Envoi de paquets vers le routeur en cours...")

    packets_sent = 0
    start_time = time.time()

    while packets_sent < PACKETS:
        send(tcp_packet, count=1, verbose=False)
        packets_sent += 1

        send(udp_packet, count=1, verbose=False)
        packets_sent += 1

        send(icmp_packet, count=1, verbose=False)
        packets_sent += 1

        if packets_sent % 300 == 0:
            print(f"Progression: {packets_sent}/{PACKETS} paquets envoyés")

    total_time = time.time() - start_time
    print(f"✅ Envoi terminé: {packets_sent} paquets envoyés en {total_time:.2f} secondes")
    print(f"Taux d'envoi: {packets_sent / total_time:.2f} paquets/seconde")

    return total_time


send_router_flood()
