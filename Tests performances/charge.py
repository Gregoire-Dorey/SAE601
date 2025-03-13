#!/usr/bin/env python3
# TEST DE CHARGE
# Les deux PC (192.168.1.1 et 192.168.1.2) sont connectés aux ports du switch pour permettre la communication et tester la charge réseau via le switch (192.168.1.254).

from scapy.all import *
from scapy.layers.inet import IP, ICMP

# Adresse IP cible
target_ip = "192.168.111.175"

# Nombre de paquets à envoyer
num_packets = 10000

for i in range(num_packets):
    send(IP(dst=target_ip)/ICMP())
