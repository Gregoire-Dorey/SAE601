# --------------------
# TEST DE LATENCE DHCP
# --------------------

# Importation des modules nécessaires
import binascii
from scapy.all import *
import time
import argparse
import sys
import os
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether

# Fonction qui mesure le temps nécessaire pour obtenir une adresse IP via DHCP
def measure_dhcp_time(interface=None):

    # Vérifier si l'interface existe
    if interface is None:
        print("Interfaces réseau disponibles:")
        for iface in get_if_list():

            # Ignore l'interface loopback
            if iface != "lo":
                print(f"- {iface}")
        print("\nVeuillez spécifier une interface avec l'option -i")
        return None

    # Vérifier si l'interface spécifiée existe
    if interface not in get_if_list():
        print(f"Erreur: L'interface {interface} n'existe pas")
        return None

    print(f"Démarrage de la mesure DHCP sur l'interface {interface}")

    # Obtenir l'adresse MAC de l'interface
    mac_address = get_if_hwaddr(interface)
    print(f"Adresse MAC de l'interface: {mac_address}")

    # Convertir l'adresse MAC en format brut pour le champ BOOTP
    mac_raw = mac_address.replace(':', '')

    # Stockage des temps pour chaque étape  du processus DHCP
    timing = {
        'start': time.time(),
        'discover_sent': None,
        'offer_received': None,
        'request_sent': None,
        'ack_received': None
    }

    # Stockage des informations DHCP obtenues
    dhcp_info = {
        'offered_ip': None,
        'server_id': None,
        'final_ip': None,
        'subnet_mask': None,
        'router': None,
        'dns': None,
        'lease_time': None
    }

    # Générer un identifiant de transaction aléatoire pour le DHCP
    xid_value = random.randint(1, 0xFFFFFFFF)

    # Fonction pour gérer les paquets DHCP reçus
    def dhcp_callback(packet):
        if DHCP in packet and packet[BOOTP].xid == xid_value:
            # Extraire le type de message DHCP
            message_type = None
            for option in packet[DHCP].options:
                if isinstance(option, tuple) and option[0] == 'message-type':
                    message_type = option[1]
                    break

            if message_type is None:
                return

            # Réception d'un DHCP Offer
            if message_type == 2 and timing['offer_received'] is None:
                timing['offer_received'] = time.time()
                dhcp_info['offered_ip'] = packet[BOOTP].yiaddr

                # Extraire le server identifier
                for option in packet[DHCP].options:
                    if isinstance(option, tuple) and option[0] == 'server_id':
                        dhcp_info['server_id'] = option[1]
                        break

                print(f"DHCP OFFER reçu après {timing['offer_received'] - timing['discover_sent']:.4f} secondes")
                print(f"Adresse IP proposée: {dhcp_info['offered_ip']}")

                # Envoi d'un DHCP Request
                timing['request_sent'] = time.time()

                # Transformer l'adresse MAC en format binaire pour le champ chaddr
                mac_bytes = binascii.unhexlify(mac_raw)

                dhcp_request = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac_address) / \
                               IP(src="0.0.0.0", dst="255.255.255.255") / \
                               UDP(sport=68, dport=67) / \
                               BOOTP(chaddr=mac_bytes, xid=xid_value, flags=0x8000) / \
                               DHCP(options=[('message-type', 'request'),
                                             ('requested_addr', dhcp_info['offered_ip']),
                                             ('server_id', dhcp_info['server_id']),
                                             'end'])
                sendp(dhcp_request, iface=interface, verbose=0)
                print(f"DHCP REQUEST envoyé pour {dhcp_info['offered_ip']}")

            # DHCP ACK (5)
            elif message_type == 5:
                timing['ack_received'] = time.time()
                dhcp_info['final_ip'] = packet[BOOTP].yiaddr

                # Extraire d'autres informations utiles
                for option in packet[DHCP].options:
                    if isinstance(option, tuple):
                        if option[0] == 'subnet_mask':
                            dhcp_info['subnet_mask'] = option[1]
                        elif option[0] == 'router':
                            dhcp_info['router'] = option[1]
                        elif option[0] == 'name_server' or option[0] == 'domain_name_server':
                            dhcp_info['dns'] = option[1]
                        elif option[0] == 'lease_time':
                            dhcp_info['lease_time'] = option[1]

                print(f"DHCP ACK reçu après {timing['ack_received'] - timing['request_sent']:.4f} secondes")
                print(f"Adresse IP confirmée: {dhcp_info['final_ip']}")
                print(f"Temps total d'obtention: {timing['ack_received'] - timing['start']:.4f} secondes")

                # Arrêter la capture
                return True

    # Démarrer l'écoute en arrière-plan
    sniff_filter = "udp and (port 67 or port 68)"
    sniff_thread = AsyncSniffer(iface=interface, filter=sniff_filter, prn=dhcp_callback)
    sniff_thread.start()

    # Transformation de l'adresse MAC en format binaire pour le champ chaddr
    mac_bytes = binascii.unhexlify(mac_raw)

    # Envoyer un DHCP Discover
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac_address) / \
                    IP(src="0.0.0.0", dst="255.255.255.255") / \
                    UDP(sport=68, dport=67) / \
                    BOOTP(chaddr=mac_bytes, xid=xid_value, flags=0x8000) / \
                    DHCP(options=[('message-type', 'discover'), 'end'])

    timing['discover_sent'] = time.time()
    sendp(dhcp_discover, iface=interface, verbose=0)
    print("DHCP DISCOVER envoyé")

    # Attendre la fin du processus DHCP (max 30 secondes)
    timeout = 30
    start_time = time.time()
    while time.time() - start_time < timeout:
        if timing['ack_received'] is not None:
            break
        time.sleep(0.1)

    # Arrêter la capture si pas terminée
    sniff_thread.stop()

    # Vérifier si le processus a été interrompu
    if timing['ack_received'] is None:
        print(f"Aucune réponse DHCP reçue après {timeout} secondes")
        return None

    # Calculer les temps et préparer le rapport
    results = {
        'total_time': timing['ack_received'] - timing['start'] if timing['ack_received'] else None,
        'discover_to_offer': timing['offer_received'] - timing['discover_sent'] if timing['offer_received'] else None,
        'request_to_ack': timing['ack_received'] - timing['request_sent'] if timing['ack_received'] else None,
        'ip_address': dhcp_info['final_ip'],
        'subnet_mask': dhcp_info['subnet_mask'],
        'router': dhcp_info['router'],
        'dns': dhcp_info['dns'],
        'lease_time': dhcp_info['lease_time']
    }

    return results


if __name__ == "__main__":
    # Vérifier si on est sous Linux
    if not sys.platform.startswith('linux'):
        print("Ce script est conçu pour Linux. Pour les autres systèmes, utilisez la version appropriée.")
        sys.exit(1)

    # Vérifier les privilèges root
    if os.geteuid() != 0:
        print("Ce script nécessite des privilèges root pour capturer les paquets réseau.")
        print("Veuillez relancer avec sudo.")
        sys.exit(1)

    # Analyser les arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Mesure du temps d\'obtention d\'une adresse IP via DHCP sous Linux')
    parser.add_argument('-i', '--interface', help='Interface réseau à utiliser (ex: eth0, wlan0)')
    parser.add_argument('-l', '--list', action='store_true', help='Lister les interfaces réseau disponibles')

    args = parser.parse_args()

    if args.list:
        print("Interfaces réseau disponibles:")
        for iface in get_if_list():
            if iface != "lo":  # Ignorer l'interface loopback
                print(f"- {iface}")
        sys.exit(0)

    try:
        results = measure_dhcp_time(args.interface)

        if results:
            print("\n--- Résultats de la mesure DHCP ---")
            print(f"Temps total d'obtention d'une adresse IP: {results['total_time']:.4f} secondes")
            print(f"Temps entre DISCOVER et OFFER: {results['discover_to_offer']:.4f} secondes")
            print(f"Temps entre REQUEST et ACK: {results['request_to_ack']:.4f} secondes")
            print("\n--- Informations de configuration réseau ---")
            print(f"Adresse IP obtenue: {results['ip_address']}")
            print(f"Masque de sous-réseau: {results['subnet_mask']}")
            print(f"Routeur: {results['router']}")
            print(f"Serveurs DNS: {results['dns']}")
            print(f"Durée du bail: {results['lease_time']} secondes")
    except Exception as e:
        print(f"Erreur lors de l'exécution du script: {str(e)}")
        print("Des problèmes courants peuvent être:")
        print("- Permissions insuffisantes (utilisez sudo)")
        print("- Interface réseau non disponible")
        print("- Problèmes de drivers réseau")
        print("- Bibliothèque Scapy mal installée")