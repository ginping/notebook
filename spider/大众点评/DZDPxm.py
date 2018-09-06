import re
import csv
import time
import random
import requests
from pyquery import PyQuery as pq

url_base = 'http://www.dianping.com/shop/'
url = 'http://www.dianping.com/xiamen/ch10/g4473'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Cookie': '_lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=165a29c7ba4c8-07e63548b75855-9393265-144000-165a29c7ba4c8; _lxsdk=165a29c7ba4c8-07e63548b75855-9393265-144000-165a29c7ba4c8; _hc.v=3f9d95cf-359d-bf59-9ad8-192316f743e0.1536031489; s_ViewType=10; cy=2; cye=beijing; lgtoken=0c5f8c8ba-6670-4eb0-8800-c8f51a2373d0; dper=e62e27e62b5dd9a8142bfc051f5352a4daeb399a966146fa2f7d858cd528fc18818e5a6abbc76fef9e7847f2cb1e66e7c64a2c1ff83258361ac5baaa2c8b458cf38d044c50ccc902dad1bc6caea725f188bfb1ec81312b2be9fae633c576cd4b; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_1782343882; ctu=bb1ea26276669ed59b2b94fee9d8141b73a5ae7e95a2b1558b34fbda8553c6b9; uamo=18629646293; _lxsdk_s=165a29c7ba4-39-4e0-43c%7C%7C428'
}
list_map = ['<span class="fn-urRy"/>', str(1), '<span class="fn-FJy9"/>', '<span class="fn-huhQ"/>',
            '<span class="fn-3Ywa"/>',
            '<span class="fn-Ws1o"/>', '<span class="fn-xfkY"/>', '<span class="fn-zpQd"/>', '<span class="fn-0lrK"/>',
            '<span class="fn-04ho"/>']


def get_html(url):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print('请求网页源代码失败, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        print('获取当前url的网页源代码失败！')
        time.sleep(4 + float(random.randint(1, 800)) / 200)
        return None


def get_page_num(html):
    try:
        doc = pq(html)
        items = doc('.page a').items()
        page_num = []
        for item in items:
            page_num.append(item.text())
        page = int(page_num[-2])
        return page
    except Exception as e:
        print(e)
        print('获取当前索引页的页码数失败！')
        time.sleep(4 + float(random.randint(1, 800)) / 200)
        return None


def get_index_urls(html):
    try:
        doc = pq(html)
        items = doc('#classfy a').items()
        for item in items:
            url = item.attr['href']
            html = get_html(url)
            doc = pq(html)
            sub = doc('#classfy-sub a')
            if not str(sub):
                yield url
            else:
                items_sub = sub.items()
                for item_sub in items_sub:
                    uri = item_sub.attr['href']
                    yield uri
    except Exception as e:
        print(e)
        print('获取当前品类的索引页urls失败！')
        time.sleep(4 + float(random.randint(1, 800)) / 200)
        return None


def get_detail_urls(html):
    try:
        shopids = re.findall('"shop_img_click" data-shopid="([0-9]+)"', str(html), re.S)
        for shopid in shopids:
            url = url_base + shopid
            yield url
    except Exception as e:
        print(e)
        print('获取当前索引页的详情页urls失败！')
        time.sleep(4 + float(random.randint(1, 800)) / 200)
        return None


def parse_detail(html):
    try:
        doc = pq(html)
        data = []
        infos = re.findall(
            'shopName: "(.*?)", address: "(.*?)", publicTransit: .*?cityName: "(.*?)", cityEnName.*?shopPower:([0-9]+), voteTotal.*?mainCategoryName:"(.*?)", categor',
            html, re.S)
        for info in infos[0]:
            if info:
                data.append(info)
            else:
                data.append(' ')
        tel = str(doc('.expand-info.tel span'))[35:]
        for i in range(10):
            tel = tel.replace(list_map[i], str(i))
        tele = "；".join(tel.split())
        if tele:
            data.append(tele)
        else:
            data.append(' ')
        category = doc('.breadcrumb').text()
        if category:
            data.append(category)
        else:
            data.append(' ')
        info_str = str(doc('.brief-info span'))
        for i in range(10):
            info_str = info_str.replace(list_map[i], str(i))
        info = pq(info_str)
        rank = info('.mid-rank-stars').attr.title
        if rank:
            data.append(rank)
        else:
            data.append(' ')
        count = info('#reviewCount').text()
        if count:
            data.append(count)
        else:
            data.append(' ')
        avgprice = info('#avgPriceTitle').text()
        if avgprice:
            data.append(avgprice)
        else:
            data.append(' ')
        items = info('#comment_score .item')
        infos = re.findall(
            '<span class="item">口味: (.+?) </span> <span class="item">环境: (.+?) </span> <span class="item">服务: (.+?) </span> ',
            str(items), re.S)
        for info in infos[0]:
            if info:
                data.append(info)
            else:
                data.append(' ')
        return data
    except Exception as e:
        print(e)
        print('获取该详情页内的数据失败！')
        print('快点开上面这条url滑动一下验证码！！！（如果有验证码的话）')
        time.sleep(20 + float(random.randint(1, 2000)) / 200)
        return None


# 店名  地址  城市  评分  类别  联系方式  定位  评级  评论数  人均价格  口味  环境  服务
def main():
    html = get_html(url)
    with open(r'C:\Users\Ph\Desktop\AntAgent\大众点评\厦门\美食.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['店名', '地址', '城市', '评分', '类别', '联系方式', '定位', '评级', '评论数', '人均价格', '口味', '环境', '服务'])
        check = []
        for urindex in get_index_urls(html):
            print(f'正在爬取：{urindex}', '\n')
            html = get_html(urindex)
            page = get_page_num(html)
            print(f'一共有{page}页', '\n')
            i = 1
            if not page:    # 如果该品类只有一页，page会返回None，需要手动定义为1页否则会报错
                page = int(1)
            while i <= page:
                # time.sleep(3 + float(random.randint(1, 600))/200)
                url_page = urindex + 'p' + str(i)
                html = get_html(url_page)
                print('\n', f'正在爬取第{i}页：{url_page}', '\n')
                i += 1
                for uri in get_detail_urls(html):
                    print(f'正在爬取详情页：{uri}')
                    html = get_html(uri)
                    data = parse_detail(html)
                    if data:
                        if data not in check:
                            check.append(data)
                            writer.writerow(data)
                            print(data)
                        else:
                            print('该详情页信息已存在')
                    else:
                        print('请求该详情页信息失败！')


if __name__ == '__main__':
    main()
