import requests 
from bs4 import BeautifulSoup
import mysql.connector
import json

""" url = 'https://www.abc.es/deportes/futbol/liga-primera/2018-2019/jornada-12/clasificacion-resultados.html' """


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
result = []
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

for i in range(1, 16):
    num_string = str(i)
    """ url = 'https://www.abc.es/deportes/futbol/liga-primera/' + y + '/jornada-' + num_string + '/clasificacion-resultados.html' """
    """ url = 'https://www.abc.es/deportes/futbol/liga-primera/jornada-' + num_string + '/clasificacion-resultados.html' """
    
    url = 'https://www.abc.es/deportes/futbol/liga-primera/jornada-15/clasificacion-resultados.html'
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
            'fecha': i,
            'equipo': equipo.strip(),
            'posicion': pos.strip(),
            'year': '2023-2024'
        } 
        print(jornada)
        result.append(jornada)

try:
    for v in result:
        print(v)
        cursor.execute('''INSERT INTO posiciones (fecha, equipo, posicion, year) VALUES (%s, %s, %s, %s)''', 
        (v['fecha'], v['equipo'], v['posicion'], v['year']))
    conexion.commit()
    print("Save success")
except mysql.connector.Error as err:
    print("Error de MySQL: {err}")
finally:
    cursor.close()
    conexion.close() 