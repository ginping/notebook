import re
import pymysql
import requests
from pyquery import PyQuery as pq
from databases.pymysql_test import *


headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}

def get_html(num):
    url_base = 'http://www.qdaily.com/articles/{}.html'
    url = url_base.format(num)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        else: 
            print('Error code: ', response.status_code)
            return None
    except Exception as e:
        print("Get html Error: ", e)
        return None

def parse(html):
    doc = pq(html)
    titles = doc('title').text()
    if titles: title = titles[:-10]
    qtype = re.findall('_(.*?)_', titles, re.S)
    if qtype: qtype = qtype[0]
    created_at = doc('.date.smart-date').attr['data-origindate'][:-6]
    image = doc('.article-detail-hd img').attr['data-src']
    author = doc('.name').text()
    items = doc('.detail p').items()
    content = []
    # view_count = 0
    # is_valid = 1
    for item in items:
        content.append(item.text())
    contents = '\n'.join(content[:-4])
    data = (title, contents, qtype, created_at, image, author)
    return data


def save_to_mysql(data, num):
    obj = MysqlSearch()
    if data: 
        obj.add_one(data)
        print('save one data to mysql! id: %d' %num)
    else: print('data is empty!')


def main():
    for num in range(40003, 56537):
        html = get_html(num)
        if html: 
            data = parse(html)
            save_to_mysql(data, num)
        else:
        	continue


if __name__ == '__main__':
    main()