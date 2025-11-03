import cloudscraper
import requests 
from bs4 import BeautifulSoup
import mysql.connector
import json

""" url = 'https://www.abc.es/deportes/futbol/liga-primera/2018-2019/jornada-12/clasificacion-resultados.html' """
""" years = ["2018-2019", "2019-2020", "2020-2021"] """

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

years = [
    '2010-2011',
    '2011-2012',
    '2012-2013',
    '2013-2014',
    '2014-2015',
    '2015-2016',
    '2016-2017',
    '2017-2018',
    '2018-2019',
    '2019-2020',
    '2020-2021',
    '2021-2022',
    '2022-2023',
]

for y in years:
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    cookies = {'cookie_name': 'cookie_value'}
    url = 'https://www.abc.es/deportes/futbol/liga-primera/' + y + '/calendario.html'
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'lxml')
    dataMain = soup.find('div', class_='sd_phase sd_phase_liga')
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
                        'year': y
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

