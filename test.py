import cloudscraper
import requests 
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
cookies = {'cookie_name': 'cookie_value'}
""" url = 'https://www.abc.es/deportes/futbol/liga-primera/2018-2019/jornada-12/clasificacion-resultados.html' """
url = 'https://www.abc.es/deportes/futbol/liga-primera/2018-2019/calendario.html'
response = requests.get(url, headers=headers, cookies=cookies)
years = ["2018-2019", "2019-2020", "2020-2021"]
""" scraper = cloudscraper.create_scraper()
response = scraper.get(url)
if response.status_code == 200 : 
    print('entro') """


""" response = requests.get(url) """
soup = BeautifulSoup(response.text, 'lxml')
table = soup.findAll('table')
print(table)
""" table = soup.findAll('table') """

for jornada in table.find_all('tr')
    rows = jornada

    
