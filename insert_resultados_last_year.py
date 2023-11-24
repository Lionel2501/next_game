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

matchDateResults = []
teamsVersusResults = []
scoreResult = []
partido = {
    'fecha': '',
    'local': '',
    'visitante': '',
    'resultado': ''
}


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
cookies = {'cookie_name': 'cookie_value'}
url = 'https://www.abc.es/deportes/futbol/liga-primera/2023-2024/calendario.html'
response = requests.get(url, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, 'lxml')
dataMain = soup.find('div', class_='sd_phase sd_phase_liga')
matchDayData = []
if dataMain:    
    matchDayData = dataMain.find_all('article', class_='sd_block sd_shields futbol')

if matchDayData:
    for matchDay in matchDayData:
        matchDate = matchDay.find('h2', class_='title sd_dot_title')
        spanElement = matchDate.find('span')
        spanElement.decompose()
        fecha = matchDate.text.strip()
        fecha = fecha.split('Jornada ')
        matchDayClear = fecha[1]

        teamsVersus = matchDay.find_all('a', class_='sd_txt_black')

        if teamsVersus:
            for teams in teamsVersus:
                teamsTitle = teams.get('title')
                valores = teamsTitle.split(' - ')
                local = valores[0]
                visitante = valores[1]
                resultado = teams.text.strip()
                partido = {
                    'fecha': matchDayClear.strip(),
                    'local': local.strip(),
                    'visitante': visitante.strip(),
                    'resultado': resultado,
                    'year': '2023-2024'
                } 
                matchDateResults.append(partido)
        else: 
            trs = matchDay.find_all('tr')
            for t in trs:
                tds = t.find_all('td')
                span = t.find_all('span', class_="sd_team_name")
                equipoLocal = span[0].text.strip()
                equipoVisitante = span[1].text.strip()
                partido = {
                    'fecha': matchDayClear.strip(),
                    'local': equipoLocal.strip(),
                    'visitante': equipoVisitante.strip(),
                    'resultado': '',
                    'year': '2023-2024'
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