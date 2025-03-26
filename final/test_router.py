# scp_transfer.py

import time
from paramiko import SSHClient, AutoAddPolicy
from scp import SCPClient
import datetime as dt

date = dt.datetime.now()
date = date.strftime("%d-%m-%Y-%H-%M-%S")

def scp_transfer_with_eta(host, port, username, password, local_path, remote_path):
    
    """
    Transfère un fichier via SCP et affiche une ETA.
    :param host: Adresse IP ou nom d'hôte du serveur distant.
    :param port: Port SSH (souvent 22).
    :param username: Nom d'utilisateur SSH.
    :param password: Mot de passe SSH.
    :param local_path: Chemin du fichier local.
    :param remote_path: Chemin de destination sur le serveur.
    """

    def progress(filename, size, sent):
        now = time.time()
        if not hasattr(progress, "start_time"):
            progress.start_time = now
        elapsed = now - progress.start_time
        if sent == 0:
            return
        rate = sent / elapsed
        eta = (size - sent) / rate if rate > 0 else 0
        percent = (sent / size) * 100
        print(f"\r{filename} - {percent:.1f}% - ETA: {int(eta)}s", end='')

    try:
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password)

        with SCPClient(ssh.get_transport(), progress=progress) as scp:
            progress.start_time = time.time()
            scp.put(local_path, remote_path=remote_path)
            print(f"\nTransfert de {local_path} terminé.")
    except Exception as e:
        print(f"Erreur lors du transfert : {e}")


scp_transfer_with_eta("192.168.99.230",22,"adminetu","Adminetu1","/home/adminetu/charge/bigfile.txt",f"/home/adminetu/test-rtr/bigfile-transfered{date}.txt")
