import requests
import re
import time
import random
import csv
import socket
socket.setdefaulttimeout(10)


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
    'Cookie': '_lxsdk_cuid=165145fb438c8-0d47268e22d057-47e1039-144000-165145fb4399f; mtcdn=K; lsu=; oc=tlUYQBZnp-XDdxdlBsGWkzV9N9wP9sC-aZSJ3x3ozTkewWyg9EO4f4b_zOl7NULA5gfvVN8wo-sYcoVWWsS0L9Wh9sC6j3FLKghU-bcxqe7Awqh9n6qJYW5JjPdxhzE772E4p3NyIKOk4iuLrOIY8tVZBZFRwZGSe-GObK992oE; __utma=211559370.153165500.1533654524.1533654524.1533654524.1; __utmz=211559370.1533654524.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __mta=212646827.1533690422128.1533690422128.1533690422128.1; ci=30; rvct=30%2C20%2C45%2C10%2C62; client-id=489d60c4-58f6-4552-9d57-1e1abe750ca9; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=212646827.1533690422128.1533690422128.1533780156989.2; lat=22.762636; lng=113.851487; u=279605464; n=%E6%9E%97%E6%B8%85%E7%8C%AB%E8%80%B3; lt=_Ca4xNrg69GjapR0IImXz-fPi_YAAAAAPAYAAOSYRwfDdBn8-DllAbdJ4Fdt9re5WK33Lt7fxIUeHZWO8pcb-xS64ktX5cg5IxQV7A; token2=_Ca4xNrg69GjapR0IImXz-fPi_YAAAAAPAYAAOSYRwfDdBn8-DllAbdJ4Fdt9re5WK33Lt7fxIUeHZWO8pcb-xS64ktX5cg5IxQV7A; uuid=b99383fdbaf644978482.1533780149.2.0.1; em=bnVsbA; om=bnVsbA; unc=%E6%9E%97%E6%B8%85%E7%8C%AB%E8%80%B3; _lxsdk_s=1651c6bdf64-918-6b3-06a%7C%7C11'
}

proxies = {

}

url_base = 'http://cq.meituan.com/meishi/'    # 城市
url_fl = url_base + 'c228/' + 'pn{page}/'    # 创意菜：c228   日韩料理: c28    咖啡酒吧: c41
# page_num = num


def get_poiId_url(url):
    try:
        content = requests.get(url, headers=headers).text
        poiIds = re.findall(r'{"poiId":([0-9]+),"frontImg"', content, re.S)
        if poiIds:
            for poiId in poiIds:
                poiId_url = url_base + poiId + '/'
                yield poiId_url
        else:
            print('poiId is null')
            return None
    except TimeoutError:
        print('请求poiIds超时', url)
        return get_poiId_url(url)
    except ConnectionError:
        return get_poiId_url(url)


def parse_detail(url):
    try:
        html = requests.get(url, headers=headers).text
        text = re.findall(
            r'"poiId":([0-9]+),"name":"(.*?)","avgScore":(.*?),"address":"(.*?)","phone":"(.*?)","openTime":"(.*?)",".*?,"avgPrice":(.*?),"brand',
            html, re.S)
        # print(html)
        if text:
            return text
        else:
            print('text is null!')
    except TimeoutError:
        print('请求详情页超时', url)
        return None
    except ConnectionError:
        return None



i = 1
with open(r'C:\Users\Ph\Desktop\AntAgent\data\美团重庆创意菜.csv', 'w', newline='', encoding='utf_8_sig') as csvfile:  #文件名称
    writer = csv.writer(csvfile)
    writer.writerow(['商家编号','商家名称','平均评分','地址','联系方式','营业时间','人均消费'])
    # for i in range(1, page_num+1):
    while True:
        url_list = url_fl.format(page=i)
        i = i + 1
        print('正在爬取：', url_list)
        for url in get_poiId_url(url_list):
            data = parse_detail(url)
            if data:
                writer.writerow(data[0])
                print(data[0])
        time.sleep(4 + float(random.randint(1, 100)) / 20)
