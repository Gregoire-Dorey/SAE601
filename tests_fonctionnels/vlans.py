#!/usr/bin/env python3
# TEST DE VLANs
# 

import os

vlan_id = 10  # Remplace par le VLAN que tu veux tester
interface = "eth0"
vlan_interface = f"{interface}.{vlan_id}"

# Créer une interface VLAN
os.system(f"sudo ip link add link {interface} name {vlan_interface} type vlan id {vlan_id}")
os.system(f"sudo ip link set {vlan_interface} up")

# Demander une IP via DHCP (si un serveur DHCP est sur ce VLAN)
os.system(f"sudo dhclient {vlan_interface}")

# Tester la connectivité (remplace 8.8.8.8 par une IP de test sur ton réseau)
response = os.system(f"ping -c 4 -I {vlan_interface} 8.8.8.8")
if response == 0:
    print(f"Le VLAN {vlan_id} est accessible !")
else:
    print(f"Impossible d'accéder au réseau sur le VLAN {vlan_id}")

# Nettoyage après le test
os.system(f"sudo ip link delete {vlan_interface}")
