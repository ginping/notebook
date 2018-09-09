import re
import csv
import time
import random
import requests
from pyquery import PyQuery as pq
from multiprocessing.dummy import Pool

url_base = 'http://www.dianping.com/shop/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    'Cookie': '__mta=245634619.1536160252045.1536160252045.1536160434810.2; _lxsdk_cuid=165a29c7ba4c8-07e63548b75855-9393265-144000-165a29c7ba4c8; _lxsdk=165a29c7ba4c8-07e63548b75855-9393265-144000-165a29c7ba4c8; _hc.v=3f9d95cf-359d-bf59-9ad8-192316f743e0.1536031489; s_ViewType=10; ctu=bb1ea26276669ed59b2b94fee9d8141b73a5ae7e95a2b1558b34fbda8553c6b9; uamo=18629646293; cityInfo=%7B%22cityId%22%3A2%2C%22cityEnName%22%3A%22beijing%22%2C%22cityName%22%3A%22%E5%8C%97%E4%BA%AC%22%7D; selectLevel=%7B%22level1%22%3A%221%22%2C%22level2%22%3A%220%22%7D; ua=18629646293; cy=4; cye=guangzhou; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; lgtoken=0b13378a2-63a0-43a5-aad9-c831d472bc22; dper=e62e27e62b5dd9a8142bfc051f5352a4425deef47718350c76db17b90bdcea8948263b3dc2457e5ce265fe66c25d64f356973ec4a3bd6cc61edd3abe174703a9afa628bf2bb943483184601be860e667c390eecf33f40bbf12e512cdf4e504e6; ll=7fd06e815b796be3df069dec7836c3df; _lxsdk_s=165b7d1b07e-73b-81f-e55%7C%7C632'
}
# 加密数字的数字span标签映射关系
list_map = ['<span class="fn-urRy"/>', str(1), '<span class="fn-FJy9"/>', '<span class="fn-huhQ"/>',
            '<span class="fn-3Ywa"/>',
            '<span class="fn-Ws1o"/>', '<span class="fn-xfkY"/>', '<span class="fn-zpQd"/>', '<span class="fn-0lrK"/>',
            '<span class="fn-04ho"/>']
list_map2 = ['<span class="fn-BARz"/>', str(1), '<span class="fn-mcun"/>', '<span class="fn-SbXU"/>',
            '<span class="fn-xBtZ"/>',
            '<span class="fn-kiQs"/>', '<span class="fn-PV9m"/>', '<span class="fn-QQA6"/>', '<span class="fn-YSfV"/>',
            '<span class="fn-Gypm"/>']


# 请求url并返回网页源代码函数
def get_html(url):
    try:
        session = requests.session()
        response = session.get(url, headers=headers, timeout=8)
        if response.status_code == 200:
            return response.text
        else:
            print('请求网页源代码失败, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        print('获取当前url的网页源代码失败！')
        time.sleep(2 + float(random.randint(1, 400)) / 200)
        return None


def get_detail_html(url):
    try:
        session = requests.session()
        response = session.get(url, headers=headers, timeout=8)
        # time.sleep(float(random.randint(1, 1000))/1000)
        if response.status_code == 200:
            return response.text
        else:
            print('请求商家详情页网页源代码失败, 错误状态码：', response.status_code)
        if response.status_code == 403:
            time.sleep(12)
            return None
    except Exception as e:
        print(e)
        print('获取商家详情页的网页源代码失败！')
        time.sleep(2 + float(random.randint(1, 400)) / 200)
        return None


def get_index_html(url):
    try:
        session = requests.session()
        response = session.get(url, headers=headers, timeout=8)
        if response.status_code == 200:
            return response.text
        else:
            print('请求索引页网页源代码失败, 错误状态码：', response.status_code)
    except Exception as e:
        print(e)
        print('获取索引页的网页源代码失败！')
        time.sleep(2 + float(random.randint(1, 400)) / 200)
        return None


# 获取当前品类下的页码数
def get_page_num(html):
    try:
        doc = pq(html)
        items = doc('.page a').items()
        page_num = []
        for item in items:
            page_num.append(item.text())
        if len(page_num) > 0:
            page = int(page_num[-2])
            return page
        else:
            print('这个品类大概只有一页吧...或者有字母验证码哦！快打开确认下如果有验证码赶紧输给你24秒！')
            time.sleep(24 + float(random.randint(1, 800)) / 200)
            return int(1)
    except Exception as e:
        print('\n', e)
        time.sleep(2 + float(random.randint(1, 400)) / 200)
        return None


# 获取当前城市导航下的所有品类url
def get_index_urls(html):
    try:
        doc = pq(html)
        items = doc('#classfy a').items()
        for item in items:
            url = item.attr['href']
            html = get_html(url)
            doc = pq(html)
            sub = doc('#classfy-sub a')
            if not str(sub):  # 如果没有小分类就返回大分类url
                yield url
            else:  # 如果有小分类就依次返回小分类url
                items_sub = sub.items()
                for item_sub in items_sub:
                    uri = item_sub.attr['href']
                    if uri == url:  # 小分类第一条url和大分类是一样的 去重
                        continue
                    yield uri
    except Exception as e:
        print(e)
        print('获取当前品类的索引页urls失败！')
        time.sleep(4 + float(random.randint(1, 800)) / 200)
        return None


# 获取当前索引页下所有商家详情页的url
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


# 解析并获取商家详情页内所有所需维度的信息
def parse_detail(html):
    try:
        if not html:
            print('糟糕，要解析的这条商家详情页居然是空的！下一条！')
            # time.sleep(4 + float(random.randint(1, 800)) / 200)
            return None
        doc = pq(html)
        data = []
        infos = re.findall(
            'shopName: "(.*?)", address: "(.*?)", publicTransit: .*?cityName: "(.*?)", cityEnName.*?shopPower:([0-9]+),.*?mainCategoryName:"(.*?)", categor',
            html, re.S)
        if infos:
            for info in infos[0]:
                data.append(info)
        else:
            # for i in range(5):
            #     data.append('')
            print('未能获取正常的店名地址城市等信息，得是遇见滑动验证码了，快去滑一下快快快快快！')
            time.sleep(12 + float(random.randint(1, 1600)) / 200)  # 延迟10-20秒，利用这段时间来滑动详情页验证码
            return None
        tel = str(doc('.expand-info.tel span'))[35:]
        for i in range(10):
            tel = tel.replace(list_map[i], str(i))
            tel = tel.replace(list_map2[i], str(i))# 简单解密联系方式
        tele = "；".join(tel.split())    # 去除多个联系方式之间的空符号并改为用；连接
        if tele:
            data.append(tele)
            if tele == '无':
                print('哼，这种连电话号码都没有的商家信息要来有啥用，下一条！')
                return None
        else:
            # data.append('')
            print('未能获取正常的联系方式！')
        category = doc('.breadcrumb').text()
        if category:
            data.append(category)
        else:
            # data.append('')
            print('未能获取正常的分类信息！')
        info_str = str(doc('.brief-info span'))
        if info_str:
            for i in range(10):
                info_str = info_str.replace(list_map[i], str(i))
                info_str = info_str.replace(list_map2[i], str(i))
            info = pq(info_str)
            rank = info('.mid-rank-stars').attr.title
            data.append(rank)
            count = info('#reviewCount').text()
            data.append(count)
            avgprice = info('#avgPriceTitle').text()
            data.append(avgprice)
            items = info('#comment_score .item')
            infos = re.findall(
                '<span class="item">口味: (.+?) </span> <span class="item">环境: (.+?) </span> <span class="item">服务: (.+?) </span> ',
                str(items), re.S)
            if infos:
                for info in infos[0]:
                    data.append(info)
        else:
            # for i in range(6):
                # data.append('')
            print('获取评级均价评论数口味环境服务信息失败！')
        return data
    except Exception as e:
        print('糟糕，遇见Bug了，Bug详情见下面：\n', e)
        # print('获取该详情页内的数据失败！快点开上面这条url滑动一下验证码！！！（如果有验证码的话）')
        # time.sleep(10 + float(random.randint(1, 2000)) / 200)  # 延迟10-20秒，利用这段时间来滑动详情页验证码
        return None


# 店名  地址  城市  评分  类别  联系方式  定位  评级  评论数  人均价格  口味  环境  服务
def main():
    # 采集城市导航下的所有品类url
    # url = 'http://www.dianping.com/guangzhou/ch10/g4473'    # 填入所要爬的城市初始url
    # html = get_html(url)
    # urls = []    # 先获取一个城市导航下的所有品类url填入列表urls
    # for urindex in get_index_urls(html):
    #     if urindex not in urls:
    #         urls.append(urindex)
    #         print('正在采集品类索引url：' + urindex)
    # print('\n', f'品类索引url采集完成！  一共有{len(urls)}条品类索引url！ \n')
    with open('URLS/北京美食urls.txt', 'r') as f:
        urls = f.readlines()
    with open(r'C:\Users\Ph\Desktop\AntAgent_Data\大众点评\北京美食2.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['店名', '地址', '城市', '评分', '类别', '联系方式', '定位', '评级', '评论数', '人均价格', '口味', '环境', '服务'])
        check = []
        for index, urlindex in enumerate(urls):
            urlindex = urlindex.strip()
            print('\n', f'开始爬取第{index}个品类：{urlindex}，一共有{len(urls)}个品类', '\n')
            html = get_index_html(urlindex)
            page = get_page_num(html)
            if not page:    # 如果该品类只有一页，page会返回None，需要手动定义为1页否则会报错
                page = int(1)
            print(f'该品类 {urlindex} 一共有 {page} 页', '\n')
            i = 1
            while i <= page:
                # time.sleep(3 + float(random.randint(1, 600))/200)
                url_page = urlindex + 'p' + str(i)  # 拼接不同页数的索引页url
                print('\n', f'开始爬取第{i}页：{url_page}', '\n')
                html = get_index_html(url_page)
                uris = []
                for uri in get_detail_urls(html):
                    if uri not in uris:
                        uris.append(uri)
                i += 1
                if not uris:
                    print('见鬼，很可能是遇上了索引页字母验证码，给你一分钟，快去验证下！！！')
                    time.sleep(60 + float(random.randint(1, 1000))/200)
                    continue
                for uri in uris:
                    print(f'开始爬取详情页：{uri}')
                pool = Pool(4)    # 使用多进程提速，数字填入自己电脑cpu核数
                htmls = pool.map(get_detail_html, uris)
                # datas = pool.map(parse_detail, htmls)
                pool.close()
                pool.join()
                for html in htmls:
                    data = parse_detail(html)
                    if data:
                        if data not in check:
                            check.append(data)    # 检测去重
                            writer.writerow(data)    # 将爬取到的详情页信息写入csv
                            print(f'已写入CSV：{data}')
                        else:
                            print('该详情页信息已存在')
                    # else:
                        # print('没有爬取到任何信息呜呜呜，   或者也可能爬到垃圾信息啦！跳过跳过！')
                        # time.sleep(4 + float(random.randint(1, 600))/100)


if __name__ == '__main__':
    start = time.time()
    main()
    print('Complete!!!!!!!!!!')
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu
    print(f'一共花费了{hour}小时{minu}分钟{sec}秒')
