#!/usr/bin/env python3
# TEST DE DEBIT

# Serveur (192.168.1.1) qui écoute et reçoit des paquets de 500 Mo pendant 5 minutes, mesure la quantité de données reçues, et calcule la bande passante en Mbps.
import socket
import time

# Paramètres serveur
host = '0.0.0.0'  # Accepter les connexions depuis n'importe quelle interface
port = 5000        # Port d'écoute

# Créer un socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(1)

print(f"Serveur en attente de connexion sur {host}:{port}...")

# Accepter la connexion du client
connection, client_address = server_socket.accept()
print(f"Connexion acceptée depuis {client_address}")

# Mesurer le temps et la quantité de données reçues pendant 5 minutes
start_time = time.time()
bytes_received = 0
duration = 300  # Test de 5 minutes (300 secondes)

while time.time() - start_time < duration:
    data = connection.recv(1024 * 1024)  # Lire les données envoyées par le client (ici 1 Mo par paquet)
    if not data:
        break
    bytes_received += len(data)

# Calculer la bande passante en Mbps
end_time = time.time()
elapsed_time = end_time - start_time
bandwidth = bytes_received / elapsed_time / 1024 / 1024  # Convertir en Mbps

print(f"Bande passante reçue : {bandwidth:.2f} Mbps")
connection.close()
server_socket.close()

# ----------------------------------------------------------------------------------------------------------

# Client (192.168.1.2) qui envoie des paquets de 500 Mo à un serveur pendant 5 minutes pour tester la bande passante.
import socket
import time

# Paramètres client
server_ip = '192.168.1.1'  # L'IP du serveur (celui qui écoute)
server_port = 5000         # Le port d'écoute du serveur

# Créer un socket TCP/IP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

# Taille des paquets (500 Mo)
packet_size = 500 * 1024 * 1024  # 500 Mo
duration = 300  # Test de 5 minutes (300 secondes)
start_time = time.time()

# Envoyer des paquets de 500 Mo pendant 5 minutes
while time.time() - start_time < duration:
    client_socket.send(b"A" * packet_size)  # Envoyer un paquet de 500 Mo

client_socket.close()
