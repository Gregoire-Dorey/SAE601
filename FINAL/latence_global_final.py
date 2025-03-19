# ______________________
# TEST DE LATENCE GLOBAL
# ______________________

# Importation des modules nécessaires
from tkinter import Label, Button
from scapy.all import *
import time
from scapy.layers.inet import IP, ICMP
import utils.database as db
import utils.graph as grph

# Fonction pour mesurer la latence moyenne
def latence(sw_name,ip,win,pg):
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
            pg.step(0.09)
            win.update()
            print(f"Trame {i + 1}: Latence = {latency * 1000:.2f} ms")
        # Si aucune réponse, on considère une latence par défaut de 1 seconde
        else:
            latencies.append(1)
            print(f"Trame {i + 1}: Pas de réponse, latence fixée à 1s ")

    # Calcul de la latence moyenne à partir des latences collectées
    average_latency = sum(latencies) / len(latencies) if latencies else 0

    # Fonction pour afficher le graphique des latences et enregistrer dans la base de données
    def graph():
        db.insert_in_base(sw_name,average_latency*1000)
        grph.bargraph(db.select_latency(),"Latence en fonctionement normal","Nom des switch","Latence (en ms)")

    # Affichage de la latence moyenne dans l'interface graphique tkinter
    label = Label(win, text=f"\nLatence moyenne: {average_latency * 1000:.2f} ms", fg="gray")
    label.place(x=200,y=180)
    # Création d'un bouton pour afficher le graphique des latences
    button = Button(win, text="Afficher le graph", width=15, command=graph)
    button.place(x=520, y=200)
    # Mise à jour de la fenêtre après ajout du label et du bouton
    win.update()
    # Affichage de la latence moyenne dans la console
    print(f"\nLatence moyenne: {average_latency * 1000:.2f} ms")
    # Enregistrement de la latence moyenne dans la base de données
    db.insert_in_base(sw_name,round(average_latency*1000,2))
    # Affichage du graphique avec les latences dans l'interface graphique
    grph.bargraph(db.select_latency(),"Latence en fonctionement normal","Nom des switch","Latence (en ms)")
    # Retourner les résultats
    #return (sw_name,round(average,2))
