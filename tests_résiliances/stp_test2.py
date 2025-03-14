import paramiko
import time
import re
from datetime import datetime


def get_switch_stp(ip, username, password, enable_password=None):
    # Création d'un client SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connexion au switch
        ssh_client.connect(ip, username=username, password=password)

        # Ouvrir un shell interactif pour exécuter des commandes
        remote_conn = ssh_client.invoke_shell()
        time.sleep(1)

        # Passer en mode privilégié (enable), si un mot de passe est fourni
        if enable_password:
            remote_conn.send('enable\n')
            time.sleep(1)
            remote_conn.send(f'{enable_password}\n')
            time.sleep(1)

        # Exécuter la commande pour récupérer les informations du STP
        remote_conn.send('show spanning-tree vlan 1\n')
        time.sleep(1)

        # Lire la sortie initiale
        initial_output = ""
        while True:
            output_chunk = remote_conn.recv(5000).decode('utf-8')
            initial_output += output_chunk

            # Si la sortie contient '--More--', envoyer un espace pour continuer
            if '--More--' in output_chunk:
                remote_conn.send(' ')
                time.sleep(1)
            else:
                break

        # Vérifier le nombre de lignes sous "Interface"
        initial_lines = re.findall(r'Interface\s+(\S+)', initial_output)

        print("Initial STP configuration:")
        print(initial_output)  # Affichage complet de la sortie initiale
        print(f"\nLignes sous 'Interface' au début:")
        print(initial_lines)  # Affichage des interfaces détectées initialement

        if len(initial_lines) == 3:
            print("\nInitial STP configuration looks good. Monitoring for changes...")
        else:
            print("\nInitial STP configuration seems problematic. Monitoring for changes...")

        # Début de l'observation
        start_time = datetime.now()
        last_lines = len(initial_lines)

        while True:
            remote_conn.send('show spanning-tree vlan 1\n')
            time.sleep(1)

            # Lire la nouvelle sortie
            new_output = ""
            while True:
                output_chunk = remote_conn.recv(5000).decode('utf-8')
                new_output += output_chunk

                if '--More--' in output_chunk:
                    remote_conn.send(' ')
                    time.sleep(1)
                else:
                    break

            # Vérifier le nombre de lignes sous "Interface"
            new_lines = re.findall(r'Interface\s+(\S+)', new_output)

            print("\nNouvelles informations STP:")
            print(new_output)  # Affichage complet des nouvelles données STP
            print(f"\nLignes sous 'Interface' après changement:")
            print(new_lines)  # Affichage des interfaces détectées après changement

            # Si le nombre de lignes change, on mesure le temps écoulé
            if len(new_lines) != last_lines:
                end_time = datetime.now()
                time_diff = (end_time - start_time).total_seconds()
                print(f"\nSTP topology change detected! Time taken: {time_diff} seconds.")
                break  # Quitter la boucle après avoir détecté le changement

            last_lines = len(new_lines)  # Mettre à jour la dernière observation

    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")

    finally:
        # Fermeture de la connexion SSH
        ssh_client.close()


# Exemple d'utilisation
ip_switch = '192.168.111.26'  # Remplacer par l'adresse IP de ton switch
username = 'login'  # Remplacer par ton nom d'utilisateur
password = 'password'  # Remplacer par ton mot de passe
enable_password = 'password'  # Remplacer par ton mot de passe enable, si nécessaire

get_switch_stp(ip_switch, username, password, enable_password)
