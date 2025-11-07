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
table  = soup.find('table', class_='standard_tabelle')

print(table)
exit()

if not table:
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
  
for tr in table.find_all("tr"):
    # 1️⃣ Si c’est une ligne de jornada
    a_tag = tr.find("a", href=True)
    if a_tag and "spieltag" in a_tag["href"]:
        text = a_tag.get_text(strip=True)
        fecha = text.replace('.', '').split()[0]
        print(f"\n🟢 Nueva jornada detectée : {fecha}\n")
        continue  # on passe à la prochaine ligne (les matchs de cette jornada)

    # 2️⃣ Si c’est une ligne de match
    if fecha:
        tds = tr.find_all("td")
        if len(tds) >= 6:
            # Local = le texte du <td align="right">
            local_td = tr.find("td", align="right")
            local = local_td.get_text(strip=True) if local_td else None

            # Visitante = le texte du <td> suivant qui contient un lien d'équipe
            visitante_td = None
            for td in tds:
                if td.find("a", href=lambda href: href and "/equipos/" in href) and td != local_td:
                    visitante_td = td
            visitante = visitante_td.get_text(strip=True) if visitante_td else None

            # Résultat = dans la colonne centrale (souvent le 6e <td>)
            resultado_td = tds[5].find("a") if len(tds) > 5 else None
            resultado_text = resultado_td.get_text(strip=True) if resultado_td else None

            if local and visitante and resultado_text:
                resultado = resultado_text.split()[0]  # garde seulement "3:1"
                print(f"Fecha: {fecha} | Local: {local} | Visitante: {visitante} | Resultado: {resultado}")
                exit()

                partido = {
                    'fecha':fecha,
                    'local': local,
                    'visitante': visitante,
                    'resultado': resultado,
                    'year': '2025-2026'
                } 
                matchDateResults.append(partido)
    
try:
    for record in matchDateResults:
        print(record)
        cursor.execute('''INSERT INTO resultados (fecha, local, visitante, resultado, year) VALUES (%s, %s, %s, %s, %s)''', 
        (record['fecha'], record['local'], record['visitante'], record['resultado'], record['year']))

    conexion.commit()
except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close()

