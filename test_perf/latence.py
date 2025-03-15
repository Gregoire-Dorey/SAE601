# TEST DE LATENCE
# Le test de latence mesure le temps de réponse du switch entre l'envoi et la réception des paquets ICMP (ping) pour évaluer la performance du réseau.
from tkinter import Label, Button

from scapy.all import *
import time
from scapy.layers.inet import IP, ICMP
import utils.database as db
import utils.graph as grph


def latence(sw_name,ip,win,pg):
    # Adresse IP du switch (assume que le switch a une interface de gestion ou répond au ping)
    ip_switch = ip

    # Nombre de trames à envoyer
    num_trames = 100

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
            pg.step(0.09)
            win.update()
            print(f"Trame {i + 1}: Latence = {latency * 1000:.2f} ms")
        else:
            latencies.append(1)
            print(f"Trame {i + 1}: Pas de réponse, latence fixée à 1s ")

    # Statistiques de latence
    average_latency = sum(latencies) / len(latencies) if latencies else 0
    def graph():
        db.insert_in_base(sw_name,average_latency*1000)
        grph.bargraph(db.select_latency(),"Latence en fonctionement normal","Nom des switch","Latence (en ms)")
    label = Label(win, text=f"\nLatence moyenne: {average_latency * 1000:.2f} ms", fg="gray")
    label.place(x=200,y=180)
    button = Button(win, text="Afficher le graph", width=15, command=graph)
    button.place(x=520, y=200)
    win.update()
    print(f"\nLatence moyenne: {average_latency * 1000:.2f} ms")
    db.insert_in_base(sw_name,round(average_latency*1000,2))
    grph.bargraph(db.select_latency(),"Latence en fonctionement normal","Nom des switch","Latence (en ms)")
    #return (sw_name,round(average,2))