import requests
import time
import json
import random


def get_one_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    data = json.loads(html)['cmts']
    for item in data:
        yield {
            'comment': item['content'],
            'date': item['time'].split(' ')[0],
            'rate': item['score'],
            'city': item['cityName'],
            'nickname': item['nickName']
        }


def save_to_txt():
    for i in range(1, 1001):
        url = 'http://m.maoyan.com/mmdb/comments/movie/248566.json?_v_=yes&offset=' + str(i)
        html = get_one_page(url)
        print('正在保存第%d页。' % i)
        for item in parse_one_page(html):
            with open('xie_zheng.txt', 'a', encoding='utf-8') as f:
                f.write(item['date'] + ',' + item['nickname'] + ',' + item['city'] + ',' + str(item['rate']) + ',' + item['comment'] + '\n')
        time.sleep(4 + float(random.randint(1, 100))/20)


if __name__ == '__main__':
    save_to_txt()
