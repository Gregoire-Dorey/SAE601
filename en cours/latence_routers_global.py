import subprocess
import time

TARGET_IP = "192.168.99.228"
PING_INTERVAL = 1  # secondes

def get_ping_latency(ip):
    try:
        # pour Windows, remplace '-c' par '-n'
        result = subprocess.run(["ping", "-c", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
        if "time=" in output:
            latency = output.split("time=")[1].split(" ")[0]
            return float(latency)
    except Exception as e:
        print(f"Erreur : {e}")
    return None

if __name__ == "__main__":
    print(f"Mesure de latence vers {TARGET_IP} toutes les {PING_INTERVAL}s")
    while True:
        latency = get_ping_latency(TARGET_IP)
        if latency is not None:
            print(f"Latence : {latency} ms")
        else:
            print("Pas de réponse.")
        time.sleep(PING_INTERVAL)
