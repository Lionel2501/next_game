import requests 
from bs4 import BeautifulSoup
import mysql.connector
import json


def getData():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    cookies = {'cookie_name': 'cookie_value'}

    jornada = {
        'fecha': '',
        'equipoLocal': '',
        'equipoLocalPosicion': '',
        'equipoVisitante': '',
        'equipoVisitantePosicion': ''
    }
    result = []

    url = 'https://www.abc.es/deportes/futbol/liga-primera/2023-2024/jornada-14/clasificacion-resultados.html'
    response = requests.get(url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'lxml')

    articles = soup.find_all('article', class_='sd_blocks_group')
    tbody = articles[1].find('tbody')
    row = tbody.find_all('td', class_='sd_tbh_rb sd_al sd_tbh_team')

    for r in row:
        pos = r.find('strong', class_='sd_tbh_team_pos')
        pos = pos.text.strip()
        equipo = r.find('span')
        equipo = equipo.text.strip()
        jornada = {
            'fecha': '',
            'equipoLocal': '',
            'equipoLocalPosicion': '',
            'equipoVisitante': '',
            'equipoVisitantePosicion': ''
        }
        print(jornada)
        result.append(jornada)

try:
    response = getData()
except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close() 