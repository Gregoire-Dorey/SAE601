# TEST DE LATENCE
# Le test de latence mesure le temps de réponse du switch entre l'envoi et la réception des paquets ICMP (ping) pour évaluer la performance du réseau.

from scapy.all import *
import time
from scapy.layers.inet import IP, ICMP
from tkinter import *
import database as db
import graph as grph

def latence(sw_name, ip, win, pg):
    # Adresse IP du switch (assume que le switch a une interface de gestion ou répond au ping)
    ip_switch = ip

    # Nombre de trames à envoyer
    num_trames = 1000

    # Liste pour stocker les temps de réponse
    latencies = []
    no_response_count = 0  # Compteur pour les "pas de réponse"

    for i in range(num_trames):
        # Envoi d'une trame et mesure du temps
        start_time = time.time()
        response = sr1(IP(dst=ip_switch) / ICMP(), timeout=1, verbose=0)  # ICMP est le ping
        end_time = time.time()

        if response:
            latency = end_time - start_time
            latencies.append(latency)
            pg.step(0.09)
            win.update()
            print(f"Trame {i + 1}: Latence = {latency * 1000:.2f} ms")
        else:
            print(f"Trame {i + 1}: Pas de réponse")
            no_response_count += 1
            latencies.append(None)  # On ajoute None pour les "pas de réponse"

    # Calcul de la latence moyenne en excluant les "pas de réponse"
    valid_latencies = [latency for latency in latencies if latency is not None]
    average_latency = sum(valid_latencies) / len(valid_latencies) if valid_latencies else 0

    # Affichage des résultats
    def graph():
        db.insert_in_base(sw_name, average_latency * 1000)  # Enregistrement de la latence dans la base
        grph.bargraph(db.select_latency(), "Latence en fonctionnement normal", "Nom des switch", "Latence (en ms)")

    label = Label(win, text=f"\nLatence moyenne: {average_latency * 1000:.2f} ms", fg="gray")
    label.place(x=200, y=180)
    button = Button(win, text="Afficher le graph", width=15, command=graph)
    button.place(x=520, y=200)
    win.update()

    # Affichage du nombre de "pas de réponse"
    print(f"\nNombre de 'pas de réponse' : {no_response_count}")
    label_no_response = Label(win, text=f"Pas de réponse : {no_response_count}", fg="red")
    label_no_response.place(x=200, y=220)

