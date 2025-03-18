#!/usr/bin/env python3
# TEST DE STP via une adresse IP
# Envoie un grand nombre de BPDUs via des paquets IP pour tester la réactivité du protocole STP sous charge

from scapy.all import *
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Dot3


# Fonction pour créer un paquet BPDU encapsulé dans un paquet IP
def create_bpdu(src_mac, dest_ip, dest_mac, vlan_id):
    # Construction de l'en-tête Ethernet
    eth = Ether(src=src_mac, dst=dest_mac)

    # Création d'un paquet IP encapsulant les BPDUs
    ip = IP(src="0.0.0.0", dst=dest_ip)  # Adresse source 0.0.0.0 (source inconnue en DHCP, typique des BPDUs)

    # Création de la trame STP (BPDU) encapsulée dans un paquet Dot3
    bpdu = Dot3(type=0x0000) / Raw(load=b'\x00' * 35)  # Structure minimale du BPDU (charge utile de 35 octets)

    # Combinaison des trois : Ethernet, IP, et le BPDU
    packet = eth / ip / bpdu
    return packet


# Paramètres de test
src_mac = "00:11:22:33:44:55"  # Adresse MAC source (peut être changée)
dest_ip = "192.168.1.1"  # Adresse IP du switch (exemple : changer avec l'adresse de ton switch)
dest_mac = "01:80:C2:00:00:00"  # Adresse MAC de destination pour les BPDUs STP (adresse multicast STP)
vlan_id = 1  # Identifiant VLAN (optionnel, en fonction du scénario)

# Envoi de 1000 BPDUs à une fréquence de 1 seconde
for i in range(1000):
    packet = create_bpdu(src_mac, dest_ip, dest_mac, vlan_id)
    sendp(packet, iface="eth0", verbose=False)  # Assure-toi de spécifier l'interface réseau correcte
    time.sleep(0.01)  # Envoie un BPDU toutes les 10ms pour tester sous charge
