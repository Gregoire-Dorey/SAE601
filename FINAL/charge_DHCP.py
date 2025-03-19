import argparse
import psutil
import threading
import time
from scapy.all import *
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether


# Fonction pour afficher la liste des interfaces réseau disponibles
def list_network_interfaces():
    interfaces = psutil.net_if_addrs()
    print("Interfaces réseau disponibles :")
    for interface in interfaces:
        print(f"- {interface}")


# Fonction pour envoyer une requête DHCP DISCOVER
def send_dhcp_discover(iface, server_ip):
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(src="0.0.0.0", dst=server_ip) / UDP(sport=68, dport=67) / BOOTP(
        op=1, chaddr=RandMAC()) / DHCP(options=[("message-type", "discover"), "end"])
    sendp(dhcp_discover, iface=iface, verbose=False)
    print(f"Requête DHCP DISCOVER envoyée via {iface} à {server_ip}")


# Fonction pour envoyer des requêtes en parallèle pendant une durée donnée
def send_bulk_dhcp_requests(iface, server_ip, num_requests):
    # Durée du test définie directement ici, par exemple 100 secondes
    duration = 100  # **Change cette valeur pour ajuster la durée du test**

    start_time = time.time()
    threads = []

    while time.time() - start_time < duration:
        for _ in range(num_requests):
            thread = threading.Thread(target=send_dhcp_discover, args=(iface, server_ip))
            threads.append(thread)
            thread.start()

        # Attendre que toutes les requêtes soient envoyées
        for thread in threads:
            thread.join()

        # Repartir pour la prochaine boucle, envoyer à nouveau les requêtes
        threads = []  # Reset des threads après chaque envoi

    print(f"Envoi de {num_requests} requêtes DHCP terminé après {duration} secondes.")


# Programme principal
if __name__ == "__main__":
    # Création du parser d'arguments
    parser = argparse.ArgumentParser(description="Envoi de requêtes DHCP DISCOVER pour test de charge")
    parser.add_argument("--server", required=True, help="Adresse IP du serveur DHCP à tester")
    parser.add_argument("--clients", type=int, default=100, help="Nombre de requêtes DHCP à envoyer à chaque itération")
    parser.add_argument("--iface", help="Interface réseau à utiliser pour envoyer les requêtes")
    parser.add_argument("--list-interfaces", action="store_true",
                        help="Afficher la liste des interfaces réseau disponibles")

    args = parser.parse_args()

    # Si l'argument --list-interfaces est passé, afficher la liste des interfaces
    if args.list_interfaces:
        list_network_interfaces()

    # Si l'argument --iface est spécifié, utiliser cette interface
    elif args.iface:
        send_bulk_dhcp_requests(args.iface, args.server, args.clients)

    # Si l'argument --iface n'est pas spécifié, demander à l'utilisateur de spécifier l'interface
    else:
        print(
            "Aucune interface spécifiée, veuillez utiliser l'argument --iface ou --list-interfaces pour sélectionner l'interface.")
