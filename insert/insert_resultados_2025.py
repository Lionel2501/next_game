import cloudscraper
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
url = 'https://www.livefutbol.com/todos_partidos/esp-primera-division-2025-2026/'
response = requests.get(url, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, 'lxml')
main_div = soup.find('div', class_='module-gameplan')

if not main_div :
    print("Aucune table trouvée.")
    exit()


matchDateResults = []
teamsVersusResults = []
scoreResult = []
partido = {
    'fecha': '',
    'local': '',
    'visitante': '',
    'resultado': ''
}

matchDateResults = []  # n'oublie pas d'initialiser ta liste avant la boucle
counter = 0  # compteur de matchs
fecha = None

for div in main_div.find_all("div"):
    classes = div.get("class", [])

    # 1️⃣ Nouvelle journée détectée
    if "round-head" in classes:
        text = div.get_text(strip=True)
        fecha = text.replace('.', '').split()[0]
        print(f"\n🟢 Nouvelle jornada détectée : {fecha}\n")

    # 2️⃣ Match trouvé dans la journée en cours
    elif fecha and "match" in classes:
        # Récupération des trois valeurs importantes
        local_tag = div.find("div", class_="team-name-home")
        visitante_tag = div.find("div", class_="team-name-away")
        resultado_tag = div.find("div", class_="match-result")

        local = local_tag.find("a").get_text(strip=True) if local_tag and local_tag.find("a") else None
        visitante = visitante_tag.find("a").get_text(strip=True) if visitante_tag and visitante_tag.find("a") else None
        resultado = resultado_tag.find("a").get_text(strip=True) if resultado_tag and resultado_tag.find("a") else None

        if local and visitante:
            partido = {
                'fecha': fecha,
                'local': local,
                'visitante': visitante,
                'resultado': resultado,
                'year': '2025-2026'
            }
            matchDateResults.append(partido)

            # 🔢 Incrémenter et vérifier la limite
            counter += 1
            """ if counter >= 30:
                print("\n⛔ Limite de 30 matchs atteinte, arrêt du script.\n")
                break """

    
try:
    for record in matchDateResults:
        print(record)
        cursor.execute('''INSERT INTO liga_test_insert (fecha, local, visitante, resultado, year) VALUES (%s, %s, %s, %s, %s)''', 
        (record['fecha'], record['local'], record['visitante'], record['resultado'], record['year']))

    conexion.commit()
except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close()

