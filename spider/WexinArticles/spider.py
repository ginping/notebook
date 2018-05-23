import re
from urllib.parse import urlencode
from lxml.etree import XMLSyntaxError
from requests.exceptions import ConnectionError
import requests
from pyquery import PyQuery as pq
import pymongo
from config import *


client = pymongo.MongoClient(MONGO_URL)  # 连接信息， 链接
db = client[MONGO_DB]

base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'SUV=00655546718C0B785AD97D8AB31B6885; IPLOC=CN6101; SUID=060B8C712213940A000000005ADDE3BF; wuid=AAGPsGWpHwAAAAqGCmLvLwoAGwY=; CXID=EE3FB03ACE1E19E6007FD39468447F48; ad=0n4bSZllll2zTWqSlllllVrr3zlllllltYZaxkllll9llllllZlll5@@@@@@@@@@; ABTEST=1|1526834763|v1; weixinIndexVisited=1; JSESSIONID=aaaiCplby5ZKe8YbT9jnw; ppinf=5|1526835065|1528044665|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTYlOUUlOTclRTYlQjglODUlRTclOEMlQUIlRTglODAlQjN8Y3J0OjEwOjE1MjY4MzUwNjV8cmVmbmljazozNjolRTYlOUUlOTclRTYlQjglODUlRTclOEMlQUIlRTglODAlQjN8dXNlcmlkOjQ0Om85dDJsdVA4eFBSUUY1NUl6QUdjOTQwbk13T3dAd2VpeGluLnNvaHUuY29tfA; pprdig=kG1CM-ebP6-6R-eZVsKAFjm5gltWp-rDp1VsnNA4WpNrynPPOOnGHtV3rnBiPjJfr7zatapmkXdXw7CAierYpe4RTcrWAisTL_za8WEET9hsJfkE92jkO3dV7z8Y7QmwQ4lMaYrji6Jfh0U7mARjXkq43Wykpcdmm7yDrZykQmI; sgid=27-35160721-AVsBp3nNMBwFjSZJUQK32nk; PHPSESSID=kupbil4in0den39hnla50l4rk4; SUIR=D4D95EA3D2D7BE76396E5EEED30401D4; ppmdig=1526847252000000892b85711b39644002224b119efbfbb9; SNUID=4F41C63B494F25E29DDEDC244A4D7570; seccodeRight=success; successCount=1|Sun, 20 May 2018 20:19:17 GMT; sct=8',
    'Host': 'weixin.sogou.com',
    # 'Referer': 'http://weixin.sogou.com/weixin?query=Python&type=2&page=77&ie=utf8',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
}
proxy = None

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('Crawling', url)
    print('Trying Count', count)
    global proxy
    if count >= MAX_COUNT:
        print('Tried Too Many Counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': 'http://' + proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy', proxy)
                # count += 1
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error Occured', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')


def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None


def parse_detail(html):
    try:
        doc = pq(html)
        title = doc('.rich_media_title').text()
        content = doc('.rich_media_content').text()
        # date = doc('#publish_time').text()
        nickname = doc('#js_profile_qrcode > div > strong').text()
        wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
        pattern = re.compile("<span class='rich_media_title_ios'>(.*?)</span>", re.S)
        title = re.search(pattern, title).group(1)
        return {
            'title' : title,
            'content' : content,
            # 'date' : date,
            'nickname' : nickname,
            'wechat' : wechat
        }
    except XMLSyntaxError:
        return None
    except AttributeError:
        return None


def save_to_mongo(data):
    if db['articles'].update({'title': data['title']}, {'$set': data}, True):
        # upsert : 可选，这个参数的意思是，如果不存在update的记录，是否插入objNew,true为插入，默认是false，不插入。
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])

def main():
    for page in range(1, 40):
        html = get_index(KEYWORD, page)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    print(article_data)
                    if article_data:
                        save_to_mongo(article_data)


if __name__ == '__main__':
    main()