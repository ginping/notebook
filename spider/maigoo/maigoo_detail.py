import requests
from pyquery import PyQuery as pq
import csv
import time
import random

url_base = r'http://www.maigoo.com/ajaxstream/loadblock/?str=brand%3Asearch_BrandPY%3A%2Ccatid%3A{catid}-{level}-0%2Cnum%3A{num}%2Cpage%3A{page}'


def get_index_html(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print('get index html Error!')
    except Exception as e:
        print(e)
        # time.sleep(3)
        return None


def get_detail_html(url):
    try:
        if url:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print('get detail html Error!')
        else:
            print('get detail url is None!')
            return None
    except Exception as e:
        print(e)
        # time.sleep(3)
        return None


def get_company_html(url):
    try:
        if url:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print('get company html Error!')
        else:
            print('get company url is None!')
            return None
    except Exception as e:
        print(e)
        # time.sleep(3)
        return None


def get_index_urls(url):
    try:
        html = get_index_html(url)
        doc = pq(html)
        items = doc('a.c3f6799.b').items()
        for item in items:
            url = item.attr.href
            yield url
    except Exception as e:
        print(e)
        # time.sleep(3)
        return None


def main():
    i = 1
    with open(r'C:\Users\Ph\Desktop\AntAgent\maigoo\name.csv', 'w', newline='', encoding='utf_8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['品牌名称','公司名称','信用评分','联系方式','企业官网','企业地址','企业邮箱','企业传真'])
        while True:
            print('\n----------------------------------------------------------正在爬取第{page_num}页----------------------------------------------------------\n'.format(page_num=i))
            # num: 一页爬多少个  catid: 分类编号  level: 品牌等级  0 = All
            url_index = url_base.format(num=50, page=i, catid=1860, level=0)
            # print('正在爬取： '+url_index)
            i = i + 1
            # time.sleep(2 + float(random.randint(1, 40))/20)
            urls = get_index_urls(url_index)
            if get_index_html(url_index) == '':
                break
            for url in urls:
                print('detail url:', url)
                data = []
                html = get_detail_html(url)
                if html:
                    doc = pq(html)
                    name = doc('#brandinfo > div.info > ul > li:nth-child(1) > span').text()
                else:
                    print('get detail html is None!')
                    continue
                if name:
                    data.append(name)
                else:
                    data.append(' ')
                company_url = doc('#brandinfo > div.info > ul > li:nth-child(1) > a').attr.href
                html = get_company_html(company_url)
                if html:
                    doc = pq(html)
                    infos = doc('ul.c666 li').items()
                else:
                    #  没有公司网站的品牌从品牌页获取信息
                    infos = doc('ul.c666 li').items()
                    count_0 = 1
                    for info in infos:
                        count_0 = count_0 + 1
                        if info and count_0 == 1:
                            data.append(info.text())
                        elif info and count_0 == 2:
                            data.append(info.text())
                        elif info and count_0 > 2:
                            data.append(info.text()[6:])
                        else:
                            data.append(' ')
                    writer.writerow(data)
                    print(data)
                    continue
                count_1 = 0
                for info in infos:
                    count_1 = count_1 + 1
                    if count_1 == 1 and info:
                        data.append(info.text())
                    elif count_1 == 2 and info:
                        data.append(info.text())
                    elif count_1 > 2 and info:
                        data.append(info.text()[6:])
                    else:
                        data.append(' ')
                writer.writerow(data)
                print(data)
            # time.sleep(4 + float(random.randint(1, 80))/20)


if __name__ == "__main__":
    main()
