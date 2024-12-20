import time
import serial

def configure_switch_via_console(port, baudrate, timeout):
    try:
        # Initialisation de la connexion série
        connection = serial.Serial(port, baudrate, timeout=timeout)
        print(f"Connexion établie sur le port {port}.")

        # Réinitialisation du switch
        send_command(connection, "\n")  # Réveiller la console
        send_command(connection, "enable")  # Mode privilégié
        send_command(connection, "write erase")  # Effacer la configuration
        send_command(connection, "reload")  # Redémarrer le switch
        time.sleep(2)  # Attente pour la confirmation
        send_command(connection, "\n")  # Valider la confirmation de redémarrage
        print("Réinitialisation effectuée. Attente du redémarrage...")
        time.sleep(60)  # Temps d'attente pour le redémarrage

        # Configuration de base après redémarrage
        send_command(connection, "\n")  # Réveiller la console après redémarrage
        send_command(connection, "enable")  # Mode privilégié
        send_command(connection, "configure terminal")  # Mode configuration globale
        send_command(connection, "interface vlan 1")
        send_command(connection, "ip address 192.168.1.1 255.255.255.0")
        send_command(connection, "no shutdown")
        send_command(connection, "exit")
        send_command(connection, "ip default-gateway 192.168.1.254")
        send_command(connection, "end")  # Quitter le mode configuration
        send_command(connection, "write memory")  # Sauvegarder la configuration
        print("Configuration de base appliquée avec succès.")

        # Fermeture de la connexion
        connection.close()
        print("Connexion série fermée.")
    except Exception as e:
        print(f"Erreur : {e}")

def send_command(connection, command, delay=1):
    """Envoie une commande au switch via la connexion série."""
    connection.write((command + "\n").encode())
    time.sleep(delay)  # Attendre que la commande soit exécutée
    output = connection.read_all().decode()
    print(output)  # Afficher la sortie (utile pour le débogage)

if __name__ == "__main__":
    # Paramètres de la connexion série
    serial_port = input("Entrez le port série (ex. COM3 ou /dev/ttyS0) : ")
    baud_rate = 9600  # Vitesse par défaut pour la plupart des switchs
    timeout = 1  # Temps d'attente pour la lecture des données

    configure_switch_via_console(serial_port, baud_rate, timeout)
