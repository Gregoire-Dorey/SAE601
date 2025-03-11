#!/usr/bin/env python3
# TEST DE CHARGE
# Les deux PC sont connectés aux ports du switch pour permettre la communication et tester la charge réseau via le switch.

from scapy.all import *

# Adresse IP cible
target_ip = "192.168.1.1"

# Nombre de paquets à envoyer
num_packets = 10000

for i in range(num_packets):
    send(IP(dst=target_ip)/ICMP())
