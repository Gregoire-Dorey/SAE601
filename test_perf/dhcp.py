#!/usr/bin/env python3
from scapy.all import *
import time
import argparse
import sys
import os

from scapy.arch import get_windows_if_list
from scapy.layers.dhcp import BOOTP, DHCP
from scapy.layers.inet import IP, UDP
from scapy.layers.l2 import Ether


def measure_dhcp_time(interface=None):
    """
    Mesure le temps nécessaire pour obtenir une adresse IP via DHCP sous Windows.

    Args:
        interface (str): Nom de l'interface réseau ou son index

    Returns:
        dict: Résultats contenant les temps pour chaque étape du processus DHCP
    """
    # Sous Windows, on doit utiliser une approche différente pour les interfaces
    if interface is None:
        print("Interfaces réseau disponibles:")
        for i, iface in enumerate(get_windows_if_list()):
            print(f"{i}: {iface['name']} ({iface['description']})")

        print("\nVeuillez spécifier l'index de l'interface avec l'option -i")
        return None

    # Obtenir l'interface par son index ou nom
    if interface.isdigit():
        iface_index = int(interface)
        all_ifaces = get_windows_if_list()
        if iface_index >= len(all_ifaces):
            print(f"Erreur: L'index d'interface {iface_index} est invalide")
            return None
        iface = all_ifaces[iface_index]
        iface_name = iface['name']
    else:
        iface_name = interface

    print(f"Démarrage de la mesure DHCP sur l'interface: {iface_name}")

    # Obtenir l'adresse MAC de l'interface
    try:
        mac_address = None
        for iface in get_windows_if_list():
            if iface['name'] == iface_name:
                mac_address = iface['mac']
                break

        if not mac_address:
            print(f"Erreur: Impossible de trouver l'adresse MAC pour l'interface {iface_name}")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'adresse MAC: {str(e)}")
        return None

    # Stockage des temps pour chaque étape
    timing = {
        'start': time.time(),
        'discover_sent': None,
        'offer_received': None,
        'request_sent': None,
        'ack_received': None
    }

    # Stockage des informations DHCP
    dhcp_info = {
        'offered_ip': None,
        'server_id': None,
        'final_ip': None,
        'subnet_mask': None,
        'router': None,
        'dns': None,
        'lease_time': None
    }

    # Variable pour stocker l'ID de transaction DHCP
    xid_value = random.randint(1, 0xFFFFFFFF)

    # Fonction pour gérer les paquets reçus
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

            # DHCP Offer (2)
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
                dhcp_request = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac_address) / \
                               IP(src="0.0.0.0", dst="255.255.255.255") / \
                               UDP(sport=68, dport=67) / \
                               BOOTP(chaddr=mac_address.replace(':', ''), xid=xid_value) / \
                               DHCP(options=[('message-type', 'request'),
                                             ('requested_addr', dhcp_info['offered_ip']),
                                             ('server_id', dhcp_info['server_id']),
                                             'end'])
                sendp(dhcp_request, iface=iface_name, verbose=0)
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
                        elif option[0] == 'name_server':
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
    sniff_thread = AsyncSniffer(iface=iface_name, filter=sniff_filter, prn=dhcp_callback)
    sniff_thread.start()

    # Créer un DHCP Discover avec l'adresse MAC convertie en format approprié
    mac_bytes = mac_address.replace(':', '')

    # Envoyer un DHCP Discover
    dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff", src=mac_address) / \
                    IP(src="0.0.0.0", dst="255.255.255.255") / \
                    UDP(sport=68, dport=67) / \
                    BOOTP(chaddr=mac_bytes, xid=xid_value) / \
                    DHCP(options=[('message-type', 'discover'), 'end'])

    timing['discover_sent'] = time.time()
    sendp(dhcp_discover, iface=iface_name, verbose=0)
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
    # Vérifier si on est sur Windows
    if not sys.platform.startswith('win'):
        print("Ce script est conçu pour Windows. Pour les autres systèmes, utilisez la version standard.")
        sys.exit(1)

    # Vérifier les privilèges administrateur
    try:
        is_admin = os.environ.get('ADMINISTRATOR') == '1' or os.environ.get(
            'COMPUTERNAME') is not None and ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print("Attention: Ce script nécessite des privilèges administrateur pour capturer les paquets réseau.")
            print("Veuillez relancer ce script en tant qu'administrateur.")
            sys.exit(1)
    except:
        print("Impossible de vérifier les privilèges administrateur.")
        print("Veuillez vous assurer d'exécuter ce script en tant qu'administrateur.")

    # Analyser les arguments en ligne de commande
    parser = argparse.ArgumentParser(description='Mesure du temps d\'obtention d\'une adresse IP via DHCP sous Windows')
    parser.add_argument('-i', '--interface', help='Interface réseau à utiliser (index ou nom)')
    parser.add_argument('-l', '--list', action='store_true', help='Lister les interfaces réseau disponibles')

    args = parser.parse_args()

    if args.list:
        print("Interfaces réseau disponibles:")
        for i, iface in enumerate(get_windows_if_list()):
            print(f"{i}: {iface['name']} ({iface['description']})")
        sys.exit(0)

    try:
        if args.interface:
            results = measure_dhcp_time(args.interface)

            if results and results['total_time'] is not None:
                print("\n--- Résultats ---")
                print(f"Temps total d'obtention d'une adresse IP: {results['total_time']:.4f} secondes")
                print(f"Temps entre DISCOVER et OFFER: {results['discover_to_offer']:.4f} secondes")
                print(f"Temps entre REQUEST et ACK: {results['request_to_ack']:.4f} secondes")
                print(f"Adresse IP obtenue: {results['ip_address']}")
                print(f"Masque de sous-réseau: {results['subnet_mask']}")
                print(f"Routeur: {results['router']}")
                print(f"Serveurs DNS: {results['dns']}")
                print(f"Durée du bail: {results['lease_time']} secondes")
            elif results is None:
                print("Veuillez spécifier une interface réseau avec l'option -i")
            else:
                print("Échec de l'obtention d'une adresse IP via DHCP (timeout).")
        else:
            measure_dhcp_time()  # Affichera la liste des interfaces
    except Exception as e:
        print(f"Erreur lors de l'exécution du script: {str(e)}")
        print("Note: Ce script nécessite les privilèges administrateur et la bibliothèque Scapy.")
        print("Installation: pip install scapy")
        print("Exécution: Démarrer une invite de commande en tant qu'administrateur")