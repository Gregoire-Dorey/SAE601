import matplotlib.pyplot as plt
import database as db

def bargraph(data,nom="",nom_x="",nom_y=""):
    x=[]
    y=[]
    for i in data:
        x.append(i[0])
        y.append(i[1])

    # Création du diagramme en barres
    plt.figure(figsize=(8, 5))
    plt.bar(x, y, color='dodgerblue')

    # Ajouter des labels et un titre
    plt.xlabel(nom_x)
    plt.ylabel(nom_y)
    plt.title(nom)

    # Afficher le graphique
    plt.show()

data = db.select_latency()
bargraph(data,"Latence en fonctionement normal","Nom du switch","Latence (en ms)")
