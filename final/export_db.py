import sqlite3
from tabulate import tabulate

# Connexion à la base de données (ici un fichier SQLite)
conn = sqlite3.connect("db-metrics.db")
cursor = conn.cursor()


# Récupération des données
cursor.execute("SELECT * FROM mt_latence;")
rows = cursor.fetchall()
headers = [description[0] for description in cursor.description]

# Affichage des données sous forme de tableau
print(tabulate(rows, headers=headers, tablefmt="fancy_grid"))

# Fermeture de la connexion
conn.close()
