from scapy.all import *
import time

# Adresse IP du switch (assume que le switch a une interface de gestion ou répond au ping)
ip_switch = "192.168.1.1"

# Nombre de trames à envoyer
num_trames = 100

# Liste pour stocker les temps de réponse
latencies = []

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

# Statistiques de latence
average_latency = sum(latencies) / len(latencies) if latencies else 0
print(f"\nLatence moyenne: {average_latency * 1000:.2f} ms")
