from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import time
from database import init_db, get_recent_latencies
from latence import test_switch_latency
from monitoring import get_monitoring_data

# Initialisation de l'application
app = Flask(__name__)
socketio = SocketIO(app)

# Initialiser la base de données au démarrage
init_db()


# Routes principales
@app.route('/')
def home():
    """Page d'accueil avec menu de navigation."""
    return render_template('index.html')


@app.route('/latence')
def latence_page():
    """Page pour tester la latence du switch."""
    return render_template('latence.html')


@app.route('/monitoring')
def monitoring_page():
    """Page de monitoring des données de latence."""
    return render_template('monitoring.html')


# API pour le test de latence
@app.route('/api/test_latence', methods=['POST'])
def api_test_latence():
    """API pour effectuer un test de latence."""
    data = request.json
    ip_switch = data.get('ip')
    device_name = data.get('name', 'Switch')
    num_trames = data.get('num_trames', 10)

    result = test_switch_latency(ip_switch, num_trames, device_name)

    # Envoyer les nouvelles données au monitoring
    socketio.emit('new_latency_data', result)

    return jsonify(result)


# API pour récupérer l'historique des données de latence
@app.route('/api/latency_history', methods=['GET'])
def api_latency_history():
    """API pour récupérer l'historique des données de latence."""
    limit = request.args.get('limit', 20, type=int)
    data = get_monitoring_data(limit)
    return jsonify(data)


# Gestion du monitoring en temps réel avec SocketIO
@socketio.on('connect')
def handle_connect():
    """Gestion des connexions SocketIO."""
    print("Client connecté")


@socketio.on('request_monitoring_data')
def handle_monitoring_data():
    """Envoie les données de monitoring actuelles."""
    data = get_monitoring_data()
    socketio.emit('monitoring_data', data)


if __name__ == '__main__':
    socketio.run(app, debug=True)