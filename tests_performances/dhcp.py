#!/usr/bin/env python3
# TEST DE DHCP

from scapy.all import *
import time
import random

from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether


# Fonction pour générer une adresse MAC aléatoire
def generate_mac():
    # Générer une adresse MAC aléatoire (commençant par 00:11:22 pour la simulation)
    mac = [0x00, 0x11, 0x22, random.randint(0x00, 0x7f), random.randint(0x00, 0x7f), random.randint(0x00, 0x7f)]
    return ':'.join(map(lambda x: format(x, '02x'), mac))


# Fonction pour créer une demande DHCP Discover avec une adresse MAC unique
def create_dhcp_discover(src_mac):
    # Création de la trame Ethernet (broadcast)
    eth = Ether(src=src_mac, dst="ff:ff:ff:ff:ff:ff")  # Broadcast en MAC

    # Création de la trame IP (pour un paquet DHCP)
    ip = IP(src="0.0.0.0", dst="255.255.255.255")  # Adresse IP source à 0.0.0.0, destination en broadcast

    # Création de la trame UDP (port DHCP)
    udp = UDP(sport=68, dport=67)  # DHCP utilise les ports UDP 67 (serveur) et 68 (client)

    # Création du paquet DHCP Discover
    dhcp = BOOTP(op=1, chaddr=src_mac.replace(":", "")[:6], xid=RandInt()) / DHCP(
        options=[("message-type", "discover"), "end"])

    # Combinaison de tous les champs pour créer la demande DHCP
    packet = eth / ip / udp / dhcp
    return packet


# Paramètres de test
# Tu peux commencer avec une adresse MAC de base, mais elle changera à chaque itération
base_mac = "00:11:22:33:44:55"

# Envoi de 1000 demandes DHCP avec des adresses MAC uniques
for i in range(1000):
    # Générer une nouvelle adresse MAC à chaque envoi
    src_mac = generate_mac()

    # Créer la demande DHCP avec la nouvelle adresse MAC
    packet = create_dhcp_discover(src_mac)

    # Afficher ce que l'on envoie (adresse MAC et le paquet)
    print(f"Envoi de la demande DHCP avec l'adresse MAC {src_mac} ({i+1}/1000):")
    packet.show()  # Affiche le paquet Scapy pour vérifier sa structure

    # Envoyer le paquet
    sendp(packet, iface="eth0")  # On retire "verbose=False" pour voir ce que fait Scapy

    time.sleep(0.01)  # Envoie un paquet toutes les 10ms pour tester sous charge

print("Test terminé : 1000 demandes DHCP envoyées.")
