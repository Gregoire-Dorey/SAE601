import subprocess
import time
import os

TARGET_IP = "192.168.99.228"
PING_INTERVAL = 1  # seconds


def get_ping_latency(ip):
    try:
        # Determine the command based on the OS
        if os.name == "nt":  # Windows
            command = ["ping", "-n", "1", ip]
        else:  # Unix-based (Linux/Mac)
            command = ["ping", "-c", "1", ip]

        # Run the ping command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:  # Ping successful
            output = result.stdout
            # Extract the latency from the output
            if "time=" in output:  # Common in English ping output
                latency = output.split("time=")[1].split(" ")[0]
                return float(latency)
            elif "temps=" in output:  # French locale
                latency = output.split("temps=")[1].split(" ")[0]
                return float(latency)
        else:
            print(f"Erreur dans l'exécution de la commande ping: {result.stderr.strip()}")
    except Exception as e:
        print(f"Erreur : {e}")
    return None


if __name__ == "__main__":
    print(f"Mesure de latence vers {TARGET_IP} toutes les {PING_INTERVAL}s. Appuyez sur Ctrl+C pour arrêter.")
    try:
        while True:
            latency = get_ping_latency(TARGET_IP)
            if latency is not None:
                print(f"Latence : {latency} ms")
            else:
                print("Pas de réponse.")
            time.sleep(PING_INTERVAL)
    except KeyboardInterrupt:
        print("\nArrêt du programme.")
