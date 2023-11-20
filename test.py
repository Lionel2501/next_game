import cloudscraper
import requests 
from bs4 import BeautifulSoup
import mysql.connector

""" url = 'https://www.abc.es/deportes/futbol/liga-primera/2018-2019/jornada-12/clasificacion-resultados.html' """
""" years = ["2018-2019", "2019-2020", "2020-2021"] """

conexion = mysql.connector.connect(
    host="localhost",
    user="lione",
    password="root",
    database="Next_Game"
)

cursor = conexion.cursor()

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
cookies = {'cookie_name': 'cookie_value'}
url = 'https://www.abc.es/deportes/futbol/liga-primera/2018-2019/calendario.html'
response = requests.get(url, headers=headers, cookies=cookies)
soup = BeautifulSoup(response.text, 'lxml')
dataMain = soup.find('div', class_='sd_phase sd_phase_liga')
matchDayData = dataMain.find_all('article', class_='sd_block sd_shields futbol')

matchDateResults = []
teamsVersusResults = []
scoreResult = []

if matchDayData:
    for matchDay in matchDayData:
        matchDate = matchDay.find('h2', class_='title sd_dot_title')
        spanElement = matchDate.find('span')
        spanElement.decompose()
        matchDayClear = matchDate.text.strip()
        matchDateResults.append(matchDayClear)

        teamsVersus = matchDay.find_all('a', class_='sd_txt_black')

        if teamsVersus:
            for teams in teamsVersus:
                teamsTitle = teams.get('title')
                href_value = teams.get('href')
                contenido = teams.text.strip()
                matchDateResults.append(teamsTitle + ' ' + contenido) 

consulta_insert = "INSERT INTO last_result (resultdo) VALUES (%s)"


for result in matchDateResults:
    cursor.execute(consulta_insert, result)
    print(result)

# Confirmar los cambios
conexion.commit()

# Cerrar el cursor y la conexión
cursor.close()
conexion.close()