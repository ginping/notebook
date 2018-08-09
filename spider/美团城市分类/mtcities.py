import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq


url = 'http://www.meituan.com/changecity/'

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}


def get_city(url, headers):
	html = requests.get(url, headers=headers).text
	doc = pq(html)
	# soup = BeautifulSoup(html, 'lxml')
	hot_cities = doc('span.cities > a.link.city.sa-city').items()
	cities = doc('span.cities > a.link.city').items()
	for hot_city in hot_cities:
		city_url = hot_city.attr('href')
		city_name = hot_city.text()
		infomation = 'http:'+city_url+' '+city_name+'\n'
		save_cities(infomation)

	with open(r'C:\Users\Ph\Desktop\AntAgent\cities.txt', 'a') as f:
		f.write('\n\n\n')

	for city in cities:
		city_url = city.attr('href')
		city_name = city.text()
		infomation = 'http:'+city_url+' '+city_name+'\n'
		save_cities(infomation)


def save_cities(cities):
	with open(r'C:\Users\Ph\Desktop\AntAgent\cities.txt', 'a') as f:
		f.write(cities)


get_city(url, headers)