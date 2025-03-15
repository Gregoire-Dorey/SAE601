#!/usr/bin/env python3
"""
Script de démarrage pour l'application de test de latence réseau.
Exécutez ce fichier pour démarrer l'application.
"""

import os
from main import app, socketio, init_db

if __name__ == "__main__":
    # S'assurer que la base de données est initialisée
    init_db()

    # Déterminer le port (utiliser la variable d'environnement PORT si disponible)
    port = int(os.environ.get("PORT", 5000))

    print(f"Démarrage de l'application sur le port {port}...")
    print("Ouvrez votre navigateur à l'adresse: http://localhost:{port}")

    # Démarrer l'application
    socketio.run(app, host='0.0.0.0', port=port, debug=True)