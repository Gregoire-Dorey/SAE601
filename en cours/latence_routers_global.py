import subprocess
import time
import os
import socket

TARGET_IP = "192.168.99.228"
TCP_PORT = 80
UDP_PORT = 5005
PING_INTERVAL = 1  # secondes

latencies_icmp = []
latencies_tcp = []
latencies_udp = []

# --------- ICMP Ping ---------
def get_ping_latency(ip):
    try:
        if os.name == "nt":  # Windows
            command = ["ping", "-n", "1", "-w", "1000", ip]
        else:  # Linux/Mac
            command = ["ping", "-c", "1", "-W", "1", ip]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            output = result.stdout
            if "time=" in output:
                latency = output.split("time=")[1].split(" ")[0]
                return float(latency)
            elif "temps=" in output:
                latency = output.split("temps=")[1].split(" ")[0]
                return float(latency)
    except Exception as e:
        print(f"Erreur ICMP : {e}")
    return None

# --------- TCP Connect ---------
def get_tcp_latency(ip, port):
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        sock.connect((ip, port))
        sock.close()
        return (time.time() - start) * 1000
    except:
        return None

# --------- UDP RTT (nécessite un serveur UDP echo côté cible) ---------
def get_udp_latency(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        message = b"ping"
        start = time.time()
        sock.sendto(message, (ip, port))
        data, _ = sock.recvfrom(1024)
        end = time.time()
        return (end - start) * 1000
    except:
        return None
    finally:
        sock.close()

# --------- Main ---------
if __name__ == "__main__":
    print(f"Mesure de latence vers {TARGET_IP} toutes les {PING_INTERVAL}s. Ctrl+C pour arrêter.")
    try:
        while True:
            print("----")
            # ICMP
            latency_icmp = get_ping_latency(TARGET_IP)
            if latency_icmp is not None:
                latencies_icmp.append(latency_icmp)
                print(f"ICMP ping     : {latency_icmp:.2f} ms")
            else:
                print("ICMP ping     : No response")

            # TCP
            latency_tcp = get_tcp_latency(TARGET_IP, TCP_PORT)
            if latency_tcp is not None:
                latencies_tcp.append(latency_tcp)
                print(f"TCP connect   : {latency_tcp:.2f} ms")
            else:
                print("TCP connect   : Failed/Timeout")

            # UDP
            latency_udp = get_udp_latency(TARGET_IP, UDP_PORT)
            if latency_udp is not None:
                latencies_udp.append(latency_udp)
                print(f"UDP RTT       : {latency_udp:.2f} ms")
            else:
                print("UDP RTT       : No response")

            time.sleep(PING_INTERVAL)

    except KeyboardInterrupt:
        print("\nArrêt du programme.")
        if latencies_icmp:
            avg_icmp = sum(latencies_icmp) / len(latencies_icmp)
            print(f"Moyenne ICMP : {avg_icmp:.2f} ms ({len(latencies_icmp)} mesures)")
        if latencies_tcp:
            avg_tcp = sum(latencies_tcp) / len(latencies_tcp)
            print(f"Moyenne TCP  : {avg_tcp:.2f} ms ({len(latencies_tcp)} mesures)")
        if latencies_udp:
            avg_udp = sum(latencies_udp) / len(latencies_udp)
            print(f"Moyenne UDP  : {avg_udp:.2f} ms ({len(latencies_udp)} mesures)")
