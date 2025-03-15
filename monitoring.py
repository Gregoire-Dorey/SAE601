from database import get_recent_latencies
import time


def get_monitoring_data(limit=20):
    """
    Récupère les données de monitoring pour les afficher sur le graphique.

    Args:
        limit (int): Nombre maximum d'enregistrements à récupérer

    Returns:
        dict: Données structurées pour le graphique
    """
    recent_latencies = get_recent_latencies(limit)

    # Préparation des données pour le graphique
    data = {
        'timestamps': [],
        'latencies': [],
        'devices': []
    }

    for entry in reversed(recent_latencies):
        data['timestamps'].append(entry['timestamp'])
        data['latencies'].append(entry['latency'])
        data['devices'].append(f"{entry['name']} ({entry['ip']})")

    return data