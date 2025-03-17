#!/usr/bin/env python3
# TEST DE STP

from scapy.all import *
from scapy.layers.l2 import Ether, Dot3


# Fonction pour créer une trame BPDU
def create_bpdu(src_mac, dest_mac, vlan_id):
    # Construction d'une trame Ethernet
    eth = Ether(src=src_mac, dst=dest_mac)

    # Création de la trame STP (BPDU)
    bpdu = Dot3(type=0x0000) / Raw(load=b'\x00' * 35)  # La structure minimale d'un BPDU

    # Combinaison des deux
    packet = eth / bpdu
    return packet

# Paramètres de test
src_mac = "00:11:22:33:44:55"  # Adresse MAC source (peut être changée)
dest_mac = "01:80:C2:00:00:00"  # Adresse MAC destination (adresse multicast STP)
vlan_id = 1  # Identifiant VLAN (optionnel, en fonction de ton scénario)

# Envoi de 1000 BPDUs à une fréquence de 1 seconde
for i in range(1000):
    packet = create_bpdu(src_mac, dest_mac, vlan_id)
    sendp(packet, iface="eth0", verbose=False)  # Assure-toi de spécifier l'interface réseau correcte
    time.sleep(0.01)  # Envoie un BPDU toutes les 10ms pour tester sous charge
