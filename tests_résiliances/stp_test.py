import paramiko
import time


def get_switch_config(ip, username, password, enable_password=None):
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

        # Exécuter la commande pour récupérer la configuration
        remote_conn.send('show running-config\n')
        time.sleep(2)

        # Récupérer le résultat de la commande
        output = remote_conn.recv(5000).decode('utf-8')

        # Affichage de la configuration
        print(output)

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

get_switch_config(ip_switch, username, password, enable_password)
