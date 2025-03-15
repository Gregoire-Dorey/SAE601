from scapy.all import sr1
from scapy.layers.inet import IP, ICMP
import time
from database import insert_latency


def test_switch_latency(ip_switch, num_trames=10, device_name="Switch"):
    """
    Effectue un test de latence sur un switch et stocke les résultats.

    Args:
        ip_switch (str): Adresse IP du switch
        num_trames (int): Nombre de trames ICMP à envoyer
        device_name (str): Nom du dispositif testé

    Returns:
        dict: Informations sur la latence (moyenne, min, max)
    """
    latencies = []

    for _ in range(num_trames):
        start_time = time.time()
        response = sr1(IP(dst=ip_switch) / ICMP(), timeout=1, verbose=0)
        end_time = time.time()

        latency = (end_time - start_time) * 1000 if response else 1000
        latencies.append(latency)

    # Calculer les statistiques
    avg_latency = round(sum(latencies) / len(latencies), 2)
    min_latency = round(min(latencies), 2)
    max_latency = round(max(latencies), 2)

    # Enregistrer dans la base de données
    insert_latency(device_name, ip_switch, avg_latency)

    return {
        'latence': avg_latency,
        'min': min_latency,
        'max': max_latency,
        'ip': ip_switch,
        'name': device_name
    }