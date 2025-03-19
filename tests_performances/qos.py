#!/usr/bin/env python3
# TEST DE QOS
# Ce script mesure la QoS (Quality of Service) en évaluant la latence, la perte de paquets et le débit d'un flux vidéo entre deux machines sur un réseau.


import time
import subprocess
import scapy.all as scapy

# Fonction pour mesurer la latence avec ping
def mesurer_latence(ip):
    # Ping l'adresse IP cible et capture le temps de réponse
    response = subprocess.run(['ping', '-c', '4', ip], stdout=subprocess.PIPE)
    output = response.stdout.decode()
    # Extraire la latence
    if 'time=' in output:
        latence = output.split('time=')[1].split(' ms')[0]
        return float(latence)
    else:
        return None

# Fonction pour mesurer la perte de paquets avec scapy
def mesurer_perte_paquets(ip, count=10):
    packets_sent = count
    packets_received = 0
    
    for _ in range(count):
        # Envoie un paquet ICMP pour tester la perte de paquets
        packet = scapy.IP(dst=ip)/scapy.ICMP()
        response = scapy.sr1(packet, timeout=1, verbose=False)
        if response:
            packets_received += 1

    # Calcul de la perte de paquets
    packet_loss = (packets_sent - packets_received) / packets_sent * 100
    return packet_loss

# Fonction pour mesurer le débit en envoyant des paquets
def mesurer_debit(ip, duration=60, packet_size=500):
    # Mesure du débit pendant un certain temps
    start_time = time.time()
    packets_sent = 0

    while time.time() - start_time < duration:
        packet = scapy.IP(dst=ip)/scapy.ICMP()/'X' * packet_size
        scapy.send(packet, verbose=False)
        packets_sent += 1

    # Calcul du débit
    elapsed_time = time.time() - start_time
    # Taille du paquet en bits
    packet_size_bits = packet_size * 8
    total_data_sent = packets_sent * packet_size_bits
    debit = total_data_sent / elapsed_time / 1e6  # Débit en Mbps
    return debit

# Exemple d'utilisation pour tester la QoS
ip_target = '192.168.1.2'  # Adresse IP du client vidéo

print("Mesure de la latence...")
latence = mesurer_latence(ip_target)
if latence is not None:
    print(f"Latence moyenne: {latence} ms")
else:
    print("Impossible de mesurer la latence.")

print("Mesure de la perte de paquets...")
packet_loss = mesurer_perte_paquets(ip_target)
print(f"Perte de paquets: {packet_loss}%")

print("Mesure du débit...")
debit = mesurer_debit(ip_target, duration=60, packet_size=500)  # 60 secondes, taille de paquet 500 octets
print(f"Débit moyen: {debit:.2f} Mbps")
