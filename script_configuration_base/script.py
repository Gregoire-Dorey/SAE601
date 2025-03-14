import time
import serial


def configure_switch_clear_startup_and_vlan(port, baudrate, timeout):
    try:
        # Initialisation de la connexion série
        connection = serial.Serial(port, baudrate, timeout=timeout)
        print(f"Connexion établie sur le port {port}.")

        # Indiquer à l'utilisateur d'appuyer sur le bouton reset si nécessaire
        print(
            "Si le switch est verrouillé ou nécessite une réinitialisation physique, appuyez maintenant sur le bouton RESET.")
        time.sleep(10)  # Temps pour l'utilisateur d'appuyer sur le bouton RESET

        # Suppression de la startup-config
        send_command(connection, "\n")  # Réveiller la console
        send_command(connection, "enable")  # Mode privilégié
        send_command(connection, "write erase")  # Effacer la configuration
        print("Startup-config supprimée avec succès.")

        # Suppression du fichier/dossier vlan.dat
        send_command(connection, "delete flash:vlan.dat")  # Supprimer le fichier vlan.dat
        time.sleep(2)
        send_command(connection, "\n")  # Valider la confirmation de suppression
        print("Fichier vlan.dat supprimé avec succès.")

        # Redémarrage du switch pour appliquer les changements
        send_command(connection, "reload")  # Redémarrer le switch
        time.sleep(2)  # Attente pour la confirmation
        send_command(connection, "\n")  # Valider la confirmation de redémarrage
        print("Redémarrage en cours...")
        time.sleep(60)  # Temps d'attente pour le redémarrage

        # Application d'une nouvelle configuration
        send_command(connection, "\n")  # Réveiller la console après redémarrage
        send_command(connection, "enable")  # Mode privilégié
        send_command(connection, "configure terminal")  # Mode configuration globale

        # Configuration écrite en dur
        configuration_commands = [
            "hostname Switch-Test",
            "interface vlan 1",
            "ip address 192.168.1.1 255.255.255.0",
            "no shutdown",
            "exit",
            "ip default-gateway 192.168.1.254",
            "line console 0",
            "logging synchronous",
            "exit",
        ]
        for command in configuration_commands:
            send_command(connection, command)

        send_command(connection, "end")  # Quitter le mode configuration
        send_command(connection, "write memory")  # Sauvegarder la nouvelle configuration
        print("Nouvelle configuration appliquée avec succès.")

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

    configure_switch_clear_startup_and_vlan(serial_port, baud_rate, timeout)
