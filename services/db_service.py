import mysql.connector
from config import DB_CONFIG

def get_connection():
    """Crée et retourne une connexion MySQL à partir des paramètres du fichier config.py."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Erreur de connexion à MySQL : {err}")
        return None

def execute_query(query, params=None):
    """Exécute une requête SQL et retourne le résultat sous forme de liste de dictionnaires."""
    conn = get_connection()
    if conn is None:
        return []

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
    except mysql.connector.Error as err:
        print(f"⚠️ Erreur lors de l'exécution de la requête : {err}")
        return []
