import subprocess
import time
import os

TARGET_IP = "192.168.99.228"
PING_INTERVAL = 1  # secondes

latencies = []

def get_ping_latency(ip):
    try:
        if os.name == "nt":  # Windows
            command = ["ping", "-n", "1", ip]
        else:  # Linux/Mac
            command = ["ping", "-c", "1", ip]

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            output = result.stdout
            if "time=" in output:
                latency = output.split("time=")[1].split(" ")[0]
                return float(latency)
            elif "temps=" in output:
                latency = output.split("temps=")[1].split(" ")[0]
                return float(latency)
        else:
            print(f"Erreur dans la commande ping : {result.stderr.strip()}")
    except Exception as e:
        print(f"Erreur : {e}")
    return None

if __name__ == "__main__":
    print(f"Mesure de latence vers {TARGET_IP} toutes les {PING_INTERVAL}s. Appuyez sur Ctrl+C pour arrêter.")
    try:
        while True:
            latency = get_ping_latency(TARGET_IP)
            if latency is not None:
                latencies.append(latency)
                print(f"Latence : {latency} ms")
            else:
                print("Pas de réponse.")
            time.sleep(PING_INTERVAL)
    except KeyboardInterrupt:
        print("\nArrêt du programme.")
        if latencies:
            moyenne = sum(latencies) / len(latencies)
            print(f"\nNombre de mesures valides : {len(latencies)}")
            print(f"Moyenne des latences : {moyenne:.2f} ms")
        else:
            print("Aucune latence valide n’a été mesurée.")
