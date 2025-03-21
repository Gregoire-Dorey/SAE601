# --------------------
# TEST DE LATENCE STP
# --------------------

# Importation des modules nécessaires
from scapy.all import *
import time
import statistics
import os
import psutil  # Utilisation de psutil pour obtenir des noms d'interfaces lisibles
from scapy.layers.inet import IP, ICMP
from scapy.layers.l2 import Ether, LLC, STP
import database as db

# Paramètres du test
TARGET_IP = "192.168.99.203"  # L'adresse IP de votre switch cible
COUNT = 1000  # Nombre de BPDU à envoyer
TIMEOUT = 2  # Timeout en secondes
SW_NAME = "2960X-POE"

# Fonction pour obtenir les interafces réseaux
def get_readable_interfaces():
    interfaces = psutil.net_if_addrs()
    readable_interfaces = [iface for iface in interfaces if iface != "lo"]  # Exclure l'interface 'lo' (loopback)
    return readable_interfaces

class STPTest:
    # Fonction pour initialiser les paramètres de la classe STPTest
    def __init__(self, target_ip, count=1000, timeout=2, iface="eth0"):
        self.target_ip = target_ip
        self.count = count
        self.timeout = timeout
        self.latencies = []
        self.iface = iface

        # Vérifier que l'interface spécifiée existe
        if self.iface not in get_readable_interfaces():
            raise ValueError(f"L'interface {self.iface} n'existe pas. Veuillez vérifier.")
        else:
            print(f"Utilisation de l'interface: {self.iface}")

    # Fonction pour créer un paquet BPDU STP standard
    def create_bpdu(self):
        # Création d'un BPDU STP standard
        eth = Ether(dst="01:80:c2:00:00:00")  # Adresse MAC STP multicast
        llc = LLC(dsap=0x42, ssap=0x42, ctrl=3)
        stp = STP(
            proto=0,  # Protocol ID (0 pour STP)
            version=0,  # Version (0 pour STP)
            bpdutype=0,  # BPDU Type (0 pour Configuration BPDU)
            bpduflags=0,  # Flags (0 pour root bridge)
            rootid=0x8001,  # Root Bridge Priority + ID
            rootmac="00:11:22:33:44:55",
            pathcost=0,  # Root Path Cost
            bridgeid=0x8002,  # Bridge Priority + ID
            bridgemac="00:11:22:33:44:66",
            portid=0x8003,  # Port ID
            age=0,  # Message Age (en secondes)
            maxage=20,  # Max Age (en secondes)
            hellotime=2,  # Hello Time (en secondes)
            fwddelay=15  # Forward Delay (en secondes)
        )
        return eth / llc / stp

    # Fonction pour envoyer le BPDU et mesurer le temps de latence ICMP (ping)
    def send_bpdu_and_measure(self, i):
        # Envoie un BPDU et mesure le temps de réponse
        bpdu_packet = self.create_bpdu()

        # Ajouter ICMP Echo Request pour mesurer la latence
        ip = IP(dst=self.target_ip)
        icmp = ICMP(type=8, code=0, id=i)
        data = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 2
        ping_packet = ip / icmp / data
        # Marque le début du temps de test
        start_time = time.time()

        try:
            # Envoyer d'abord le BPDU pour ajouter de la charge
            sendp(bpdu_packet, iface=self.iface, verbose=0)  # Envoi du BPDU sur l'interface spécifiée
            # Puis mesurer la latence avec ICMP
            reply = sr1(ping_packet, timeout=self.timeout, iface=self.iface, verbose=0)  # ICMP Echo
            # Marque la fin du temps de test
            end_time = time.time()
            # Si une réponse est reçue, on mesure la latence
            if reply is not None and reply.haslayer(ICMP) and reply[ICMP].type == 0:
                latency = (end_time - start_time) * 1000  # en ms
                return latency
        except Exception as e:
            print(f"Erreur lors de l'envoi du paquet {i}: {e}")
            return None

        return None

    # Fonction pour lancer le test de charge STP
    def run_test(self):
        print(f"Test de charge STP sur {self.target_ip}")
        print(f"Envoi de {self.count} BPDU séquentiellement avec un délai de {self.timeout} secondes")
        print(f"Utilisation de l'interface: {self.iface}")

        # Envoi des BPDUs séquentiellement et mesure la latence
        for i in range(self.count):
            latency = self.send_bpdu_and_measure(i)
            if latency is not None:
                self.latencies.append(latency)
                print(f"Latence pour BPDU {i + 1}: {latency:.2f} ms")
            else:
                print(f"Aucune réponse pour BPDU {i + 1}.")

        # Filtrer les None (timeouts)
        successful_responses = len(self.latencies)

        # Calculer les statistiques
        if successful_responses > 0:
            min_latency = min(self.latencies)
            max_latency = max(self.latencies)
            avg_latency = sum(self.latencies) / successful_responses
            median_latency = statistics.median(self.latencies)
            stddev_latency = statistics.stdev(self.latencies) if successful_responses > 1 else 0
            # Affichage des résultats du test
            print("\nRésultats du test:")
            print(f"Paquets envoyés: {self.count}")
            print(f"Réponses reçues: {successful_responses} ({successful_responses / self.count * 100:.2f}%)")
            print(f"Latence minimale: {min_latency:.2f} ms")
            print(f"Latence maximale: {max_latency:.2f} ms")
            print(f"Latence moyenne: {avg_latency:.2f} ms")
            print(f"Latence médiane: {median_latency:.2f} ms")
            print(f"Écart-type: {stddev_latency:.2f} ms")
            db.insert_in_base(SW_NAME,avg_latency,"stp_latence")

            # Sauvegarder les résultats dans un fichier
            with open(f"stp_test_{self.target_ip.replace('.', '_')}.csv", "w") as f:
                f.write("index,latency_ms\n")
                for i, latency in enumerate(self.latencies):
                    f.write(f"{i},{latency:.2f}\n")

            print(f"\nRésultats détaillés sauvegardés dans stp_test_{self.target_ip.replace('.', '_')}.csv")
        else:
            print("Aucune réponse reçue pendant le test.")

# Fonction permettant de sélectionner l'interface réseau
def select_interface():
    # Liste des interfaces réseau avec des noms lisibles comme eth0, wlan0
    interfaces = get_readable_interfaces()  # Utilisation de psutil pour obtenir des interfaces réseau lisibles
    if not interfaces:
        print("Aucune interface réseau disponible.")
        exit()

    print("Sélectionnez l'interface réseau:")
    for index, iface in enumerate(interfaces):
        print(f"{index + 1}. {iface}")

    choice = int(input(f"Entrez le numéro de l'interface (1-{len(interfaces)}): "))
    if 1 <= choice <= len(interfaces):
        return interfaces[choice - 1]
    else:
        print("Choix invalide. Le script va maintenant se fermer.")
        exit()

if __name__ == "__main__":
    print("Démarrage du test de charge STP...")

    try:
        # Sélection de l'interface par l'utilisateur
        iface = select_interface()

        test = STPTest(
            target_ip=TARGET_IP,
            count=COUNT,
            timeout=TIMEOUT,
            iface=iface
        )

        test.run_test()

    except KeyboardInterrupt:
        print("\nTest interrompu par l'utilisateur.")
    except Exception as e:
        print(f"\nErreur lors de l'exécution du test: {e}")

        if os.name == 'nt':
            print("\nSur Windows, assurez-vous que:")
            print("1. Vous exécutez le script en tant qu'administrateur")
            print("2. Npcap est correctement installé (https://npcap.com)")
