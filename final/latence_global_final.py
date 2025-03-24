# --------------------
# TEST DE LATENCE GLOBAL
# --------------------

# Importation des modules nécessaires
from scapy.all import *
from scapy.layers.inet import IP, ICMP

import database as db


# Fonction pour mesurer la latence moyenne
def latence(sw_name,ip):
    # Adresse IP du switch (assume que le switch a une interface de gestion ou répond au ping)
    ip_switch = ip
    # Nombre de trames à envoyer
    num_trames = 100
    # Liste pour stocker les temps de réponse
    latencies = []
    # Envoi de 100 trames ICMP (ping)
    for i in range(num_trames):
        # Envoi d'une trame et mesure du temps
        start_time = time.time()
        response = sr1(IP(dst=ip_switch) / ICMP(), timeout=1, verbose=0)  # ICMP est le ping
        end_time = time.time()
        # Si on a une réponse, calcule de la latence
        if response:
            latency = end_time - start_time
            latencies.append(latency)
            print(f"Trame {i + 1}: Latence = {latency * 1000:.2f} ms")
        # Si aucune réponse, on considère une latence par défaut de 1 seconde
        else:
            latencies.append(1)
            print(f"Trame {i + 1}: Pas de réponse, latence fixée à 1s ")

    # Calcul de la latence moyenne à partir des latences collectées
    average_latency = sum(latencies) / len(latencies) if latencies else 0
    # Affichage de la latence moyenne dans la console
    print(f"\nLatence moyenne: {average_latency * 1000:.2f} ms")
    # Enregistrement de la latence moyenne dans la base de données
    db.insert_in_base(sw_name,round(average_latency*1000,2),"mt_latence")

latence("9300","192.168.99.5")