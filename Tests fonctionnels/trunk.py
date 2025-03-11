import scapy.all
from scapy.layers.l2 import Dot1Q


def detect_vlan(packet):
    if packet.haslayer(Dot1Q):  # Vérifie si une trame VLAN est détectée
        print(f"VLAN détecté ! ID: {packet[Dot1Q].vlan}")

# Capture les paquets sur l'interface Ethernet (à adapter selon ton OS)
scapy.all.sniff(iface="eth0", prn=detect_vlan, store=False)
