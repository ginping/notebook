import requests
from pyquery import PyQuery as pq
import csv
import time
import random
import re


# 子索引页url基本构成
url_base = r'http://www.maigoo.com/ajaxstream/loadblock/?str=brand%3Asearch_BrandPY%3A%2Ccatid%3A{catid}-{level}-0%2Cnum%3A{num}%2Cpage%3A{page}'
# 父索引页url基本构成
url_index_base = r'http://www.maigoo.com/brand/list_{list}.html'


# 获取行业页面下网页源代码并提示错误信息
def get_industry_html(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print('get industry html Error!')
    except Exception as e:
        print(e)
        return None


# 获取行业子目录下索引页网页源代码并提示错误信息
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


# 获取品牌详情页源代码并提示错误信息
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


# 获取公司详情页源代码并提示错误信息
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


# 获取行业子目录下索引页一页的所有品牌详情页url
def get_list_urls(url):
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


def main(list, indus):
    html = get_industry_html(url_index_base.format(list=list))  # 获取行业页面源代码        只需要改这里的list
    doc = pq(html)  # 解析行业页面
    items = doc('#catsearchbox > dl.category.secondcat > dd > a').items()  # 定位行业页面子目录信息
    for item in items:
        content = item.attr.href
        listid = re.findall(r'om/brand/list_([0-9]+).html', content, re.S)  # 用正则匹配行业页面子目录索引页id
        name_dir = item.text().replace('/', '_')  # 拿行业页面子目录索引页名字并把 '/' 换成 '_' ; 因为 '/' 会导致打开文件时目录错误
        if listid:  # 索引页id第一个 '不限' 是空的  用if跳过
            print('\n\n\n', listid[0], name_dir, '\n\n\n')  # 打印准备爬取的索引页id和名字
            html = get_index_html(url_index_base.format(list=listid[0]))  # 获取索引页源代码
            doc = pq(html)  # 解析索引页面
            items = doc('#catsearchbox > dl.category.thirdcat > dd > a').items()  # 定位索引页面子目录信息
            for item in items:
                content = item.attr.href
                catid = re.findall(r'om/brand/list_([0-9]+).html', content, re.S)  # 用正则匹配索引页面子目录具体分类页id
                name_csv = item.text().replace('/', '_')  # 拿索引页面子目录具体分类页名字并把 '/' 换成 '_' ; 因为 '/' 会导致打开文件时目录错误
                if catid:  # 具体分类页id第一个 '不限' 是空的  用if跳过
                    print('\n\n\n', catid[0], name_csv, '\n\n\n')  # 打印准备爬取的具体分类页id和名字
                    i = 1  # 设置页面序号  并同时当作退出while循环的条件
                    # 打开准备写入数据的csv文件  由于只能创建File文件不能创建Directory文件夹  这里的dir文件夹要自己提前创建好
                    with open(r'C:\Users\Ph\Desktop\AntAgent\maigoo\{indus}\{dir}\{name}.csv'.format(indus=indus, dir=name_dir, name=name_csv), 'w', newline='', encoding='utf_8_sig') as csvfile:
                        writer = csv.writer(csvfile)
                        # 第一行写入信息类型
                        writer.writerow(['品牌名称','公司名称','信用评分','联系方式','企业官网','企业地址','企业邮箱','企业传真'])
                        while True:
                            print('\n----------------------------------------------------------正在爬取第{page_num}页----------------------------------------------------------\n'.format(page_num=i))
                            # num: 一页爬多少个  page: 正在爬取的页面序号  catid: 分类编号  level: 品牌等级  0 = All
                            url_index = url_base.format(num=50, page=i, catid=catid[0], level=0)  # 构成子索引页url
                            i = i + 1  # 子索引页自动翻页
                            # time.sleep(2 + float(random.randint(1, 40))/20)   一开始防封ip设置的随机延时  后面发现这网站没设置反爬注释掉了
                            urls = get_list_urls(url_index)  # 获取每一个详情页的url
                            if get_index_html(url_index) == '':
                                break  # # 设置退出while循环的条件  翻页到空页面时会返回空的html
                            for url in urls:  # 遍历每一个详情页
                                print('detail url:', url)  # 打印正在爬取的详情页url
                                data = []  # 建立一个存数据的列表
                                html = get_detail_html(url)  # 请求详情页返回详情页源代码
                                # 如果有详情页就解析并定位品牌名字  否则输出错误信息并结束当前循环进入下一个循环  即爬取下一个详情页
                                if html:
                                    doc = pq(html)
                                    name = doc('#brandinfo > div.info > ul > li:nth-child(1) > span').text()
                                else:
                                    print('get detail html is None!')
                                    continue
                                # 如果品牌名字有就存入列表data否则存入一个空格
                                if name:
                                    data.append(name)
                                else:
                                    data.append(' ')
                                company_url = doc('#brandinfo > div.info > ul > li:nth-child(1) > a').attr.href  # 定位并获取公司url
                                html = get_company_html(company_url)  # 请求并返回公司详情页源代码
                                # 如果该品牌有公司详情页就解析公司详情页  否则直接解析品牌详情页  并解析定位需要的具体信息infos
                                if html:
                                    doc = pq(html)
                                    #  有公司网站的品牌从公司页面获取信息
                                    infos = doc('ul.c666 li').items()
                                else:
                                    #  没有公司网站的品牌从品牌页获取信息
                                    infos = doc('ul.c666 li').items()
                                count = 0  # 设置计数变量  用于去除 '联系方式:' 等前缀
                                for info in infos:  # 遍历具体信息infos  并逐条存入data
                                    count = count + 1
                                    if count == 1 and info:
                                        data.append(info.text())
                                    elif count == 2 and info:
                                        data.append(info.text())
                                    elif count > 2 and info:
                                        data.append(info.text()[6:])
                                    else:
                                        data.append('')
                                writer.writerow(data)  # 将一个品牌的所有信息写入一行csv文件
                                print(data)  # 输出打印写入csv文件的品牌信息
                            # time.sleep(4 + float(random.randint(1, 80))/20)  一开始防封ip设置的随机延时  后面发现这网站没设置反爬注释掉了


listname = ['建材家居', '电器办公', '穿着打扮', '饮食特产', '汽车工具', '日用品母婴', '服务保健']
listid = [7, 1, 4, 8, 9, 5, 10]

if __name__ == "__main__":
    for i in range(7):
        main(listid[i], listname[i])
