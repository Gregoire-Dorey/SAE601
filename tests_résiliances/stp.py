#!/usr/bin/env python3
# TEST DE STP
# Récupération des informations relatives au protocole STP en exécutant la commande "show spanning-tree" toutes les secondes // détecte tout changement dans la topologie réseau et mesure le temps de convergence du réseau après une déconnexion ou une reconnexion de câble.

import serial
import time

# Configuration du port série pour la connexion console
ser = serial.Serial(
    port='/dev/ttyUSB0',  # Changez avec le port série approprié (ex. 'COM1' pour Windows ou '/dev/ttyUSB0' pour Linux)
    baudrate=9600,        # Vitesse de transmission (en bauds)
    timeout=1              # Timeout pour les lectures (en secondes)
)

# Fonction pour envoyer une commande au switch et obtenir la sortie
def send_command(command):
    ser.write((command + '\n').encode())  # Envoie la commande
    time.sleep(1)  # Attente pour la réponse
    output = ser.read(ser.in_waiting).decode()  # Lire la réponse
    return output

# Fonction pour récupérer les informations de STP
def get_stp_info():
    command = "show spanning-tree"  # Commande à exécuter sur le switch
    return send_command(command)

# Fonction pour analyser la sortie STP
def parse_stp_output(output):
    lines = output.splitlines()
    root_bridge = None
    root_port = None
    blocked_ports = []

    for line in lines:
        if "Root ID" in line:
            root_bridge = line.split("Address")[1].strip()
        if "Root Port" in line:
            root_port = line.split(":")[1].strip()
        if "Designated Port" in line:
            blocked_ports.append(line.strip())

    return root_bridge, root_port, blocked_ports

# Fonction pour surveiller STP en temps réel
def monitor_stp():
    last_root_bridge = None
    last_root_port = None
    last_blocked_ports = None

    while True:
        # Récupérer la sortie de STP
        stp_info = get_stp_info()

        # Analyser les informations STP
        root_bridge, root_port, blocked_ports = parse_stp_output(stp_info)

        # Comparer les nouvelles valeurs avec les anciennes
        if root_bridge != last_root_bridge or root_port != last_root_port or blocked_ports != last_blocked_ports:
            print("Changement de topologie détecté:")
            print(f"Root Bridge: {root_bridge}")
            print(f"Root Port: {root_port}")
            print(f"Blocked Ports: {blocked_ports}")

        # Mettre à jour les anciennes valeurs
        last_root_bridge = root_bridge
        last_root_port = root_port
        last_blocked_ports = blocked_ports

        # Attendre avant de refaire une requête
        time.sleep(1)

# Lancer la surveillance STP
monitor_stp()

# N'oublie pas de fermer la connexion série lorsque tu as terminé
ser.close()

