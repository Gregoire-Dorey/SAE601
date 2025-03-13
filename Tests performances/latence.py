#!/usr/bin/env python3
# TEST DE LATENCE
# Le test de latence mesure le temps de réponse du switch entre l'envoi et la réception des paquets ICMP (ping) pour évaluer la performance du réseau.

from scapy.all import *
import time

# Adresse IP du switch (assume que le switch a une interface de gestion ou répond au ping)
ip_switch = "192.168.1.254"

# Nombre de trames à envoyer
num_trames = 1000

# Liste pour stocker les temps de réponse
latencies = []
no_response_count = 0  # Compteur pour les "pas de réponse"

for i in range(num_trames):
    # Envoi d'une trame et mesure du temps
    start_time = time.time()
    response = sr1(IP(dst=ip_switch)/ICMP(), timeout=1, verbose=0)  # ICMP est le ping
    end_time = time.time()

    if response:
        latency = end_time - start_time
        latencies.append(latency)
        print(f"Trame {i+1}: Latence = {latency * 1000:.2f} ms")
    else:
        print(f"Trame {i+1}: Pas de réponse")
        no_response_count += 1
        latencies.append(None)  # On ajoute None ou un autre indicateur pour les "pas de réponse"

# Calcul de la latence moyenne en excluant les "pas de réponse"
valid_latencies = [latency for latency in latencies if latency is not None]
average_latency = sum(valid_latencies) / len(valid_latencies) if valid_latencies else 0

# Affichage des résultats
print(f"\nLatence moyenne (sans 'pas de réponse') : {average_latency * 1000:.2f} ms")
print(f"Nombre de 'pas de réponse' : {no_response_count}")
