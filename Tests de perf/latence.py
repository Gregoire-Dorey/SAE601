#!/usr/bin/env python3
# TEST DE LATENCE
# Le test de latence mesure le temps de réponse du switch entre l'envoi et la réception des paquets ICMP (ping) pour évaluer la performance du réseau.

from scapy.all import *
import time
from utils import database

from scapy.layers.inet import IP, ICMP

def latence(sw_name,ip):
    # Adresse IP du switch (assume que le switch a une interface de gestion ou répond au ping)
    ip_switch = ip

    # Nombre de trames à envoyer
    num_trames = 1000

    # Liste pour stocker les temps de réponse
    latencies = []

    for i in range(num_trames):
        # Envoi d'une trame et mesure du temps
        start_time = time.time()
        response = sr1(IP(dst=ip_switch) / ICMP(), timeout=1, verbose=0)  # ICMP est le ping
        end_time = time.time()

        if response:
            latency = end_time - start_time
            latencies.append(latency)
            print(f"Trame {i + 1}: Latence = {latency * 1000:.2f} ms")
        else:
            print(f"Trame {i + 1}: Pas de réponse")

    # Statistiques de latence
    average_latency = sum(latencies) / len(latencies) if latencies else 0
    print(f"\nLatence moyenne: {average_latency * 1000:.2f} ms")
    average = average_latency*1000
    return (average,sw_name)

latency = latence("2960","192.168.1.254")
database.insert_in_base(latency[0],latency[1])
