from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from scapy.all import sr1
import time

from scapy.layers.inet import IP, ICMP

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    """Page d'accueil avec menu de navigation."""
    return render_template('index.html')

@app.route('/latence')
def latence_page():
    """Page pour tester la latence du switch."""
    return render_template('latence.html')

@app.route('/monitoring')
def monitoring():
    """Page de monitoring en temps réel."""
    return render_template('monitoring.html')

@socketio.on('start_monitoring')
def start_monitoring():
    """Simulation de l'envoi de paquets avec mises à jour en temps réel."""
    packet_count = 0
    while True:
        packet_count += 1
        socketio.emit('update_graph', {'packets': packet_count})
        time.sleep(1)

@app.route('/test_latence', methods=['POST'])
def test_latence():
    """Effectue un test de latence sur un switch donné."""
    ip_switch = request.json.get('ip')
    num_trames = 10
    latencies = []

    for _ in range(num_trames):
        start_time = time.time()
        response = sr1(IP(dst=ip_switch) / ICMP(), timeout=1, verbose=0)
        end_time = time.time()

        latency = (end_time - start_time) * 1000 if response else 1000
        latencies.append(latency)

    avg_latency = round(sum(latencies) / len(latencies), 2)
    return jsonify({'latence': avg_latency})

if __name__ == '__main__':
    socketio.run(app, debug=True)
