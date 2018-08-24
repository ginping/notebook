import csv
import re
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq


uri = 'http://www.huangye88.com/search.html?kw={key_word}&type=company'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)


def search(key_word):
    print('正在搜索')
    try:
        browser.get(uri.format(key_word=key_word))
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#hs_3'))
        )
        submit.click()
        index = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#search_btn > input'))
        )
        index.click()
        for info in get_infos():
            # print(info)
            yield info
    except TimeoutException:
        print('TimeoutException Error!')
        return search()


def next_page(page_number, num):
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#pagenum'))
        )
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'body > div.middle > div.mid-cont > div.content > div.pages > a:nth-child({num})'.format(num=num))))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        for info in get_infos():
            # print(info)
            yield info
    except TimeoutException:
        print('TimeoutException Error!')
        return None
    except Exception as e:
        print(e)
        return None


def get_infos():
    html = browser.page_source
    doc = pq(html)
    items = doc('.p-title')
    urls = re.findall(r'<a href="(.*?)" title', str(items), re.S)
    for url in urls:
        url_detail = url + 'company_contact.html'
        yield parse_detail(url_detail)


def parse_detail(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print('get detail page Error!')
            time.sleep(2)
            return None
        html = response.text
        doc = pq(html)
        items = doc('.con-txt li').items()
        data = []
        for item in items:
            data.append(item.text())
        # print(data)
        return data
    except TimeoutException:
        print('TimeoutException Error!')
        return None
    except Exception as e:
        print(e)
        return None


def main(key_word, page_num):
    with open(r'C:\Users\Ph\Desktop\AntAgent\88黄页网\{key_word}公司.csv'.format(key_word=key_word), 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        for data in search(key_word):
            if data:
                print(data)
                writer.writerow(data)
        for i in range(2, page_num + 1):
            if i == 2:
                j = 12
            elif i in range(3, 6):
                j = 13
            else:
                j = 15
            for data in next_page(i, j):
                if data:
                    print(data)
                    writer.writerow(data)


if __name__ == '__main__':
    main('广告', 555)    # '广告' 555 / '传媒' 381 / '营销' 555 / '策划' 555 / '增强现实' 3 / 'VR' 6 / 'AR' 6
