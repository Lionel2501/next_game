import requests 
from bs4 import BeautifulSoup
import mysql.connector
import json

conexion = mysql.connector.connect(
    user='root', 
    password='root', 
    host='localhost', 
    database='next_game', 
    port='3306'
)

cursor = conexion.cursor()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
cookies = {'cookie_name': 'cookie_value'}

jornada = {
    'fecha': '',
    'equipo': '',
    'posicion': '',
    'year': ''
}

results = []

for i in range(1, 13):
    url = f'https://www.livefutbol.com/competition/co97/espana-primera-division/se96657/2025-2026/ro267177/jornada/md{i}/results-and-standings/'
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'lxml')

    main_div = soup.find('div', class_='module-standing')
    if not main_div:
        print(f"⚠️ Aucune section trouvée pour jornada {i}")
        continue

    all_rows = main_div.find_all('tr')[1:]  # saute l’en-tête
    last_posicion = None  # valeur de secours pour la jornada courante

    for tr in all_rows:
        rank_tag = tr.find('td', class_='standing-rank')
        team_tag = tr.find('td', class_='team-name')

        if not team_tag:
            continue

        # 🟢 Si une nouvelle position est trouvée, on la garde
        if rank_tag and rank_tag.get_text(strip=True):
            last_posicion = rank_tag.get_text(strip=True)

        # 🟡 Sinon, on garde la précédente (last_posicion)
        posicion = last_posicion

        # Récupérer le nom de l’équipe
        team_a = team_tag.find('a')
        team = team_a.get_text(strip=True) if team_a else team_tag.get_text(strip=True)

        # Stocker dans la liste
        results.append({
            'fecha': i + 1,
            'team': team,
            'posicion': posicion,
            'year': '2025-2026'
        })

        print(f"Fecha: {i} | Team: {team} | Posición: {posicion}")



try:
    for v in results:
        fecha = v['fecha']
        equipo = v['team']      # (ou v['equipo'] si tu as gardé ce nom)
        posicion = v['posicion']
        year = '2025-2026'      # adapte selon ton contexte

        # 1️⃣ Met à jour la position de l’équipe locale si elle correspond
        cursor.execute("""
            UPDATE liga_test_insert 
            SET local_posicion = %s
            WHERE fecha = %s AND local = %s
        """, (posicion, fecha, equipo))

        # 2️⃣ Met à jour la position de l’équipe visiteuse si elle correspond
        cursor.execute("""
            UPDATE liga_test_insert 
            SET visitante_posicion = %s
            WHERE fecha = %s AND visitante = %s
        """, (posicion, fecha, equipo))

    conexion.commit()
    print("✅ Mise à jour des positions terminée avec succès.")

except mysql.connector.Error as err:
    print(f"❌ Erreur MySQL: {err}")

finally:
    cursor.close()
    conexion.close()
