import sqlite3
import os

DB_PATH = "db-metrics.db"


def init_db():
    """Initialise la base de données si elle n'existe pas déjà."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Créer la table pour stocker les données de latence
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS latence (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ip TEXT NOT NULL,
        latency REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    conn.commit()
    conn.close()
    print(f"Base de données initialisée : {DB_PATH}")


def insert_latency(name, ip, latency):
    """Insère une nouvelle mesure de latence dans la base de données."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO latence (name, ip, latency) VALUES (?, ?, ?)",
        (name, ip, latency)
    )

    conn.commit()
    conn.close()
    return cursor.lastrowid


def get_recent_latencies(limit=20):
    """Récupère les données de latence les plus récentes."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM latence ORDER BY timestamp DESC LIMIT ?",
        (limit,)
    )

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results