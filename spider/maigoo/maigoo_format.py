import csv
import re
import requests
from pyquery import  PyQuery as pq


url_index_base = r'http://www.maigoo.com/brand/list_{list}.html'
url_base = r'http://www.maigoo.com/ajaxstream/loadblock/?str=brand%3Asearch_BrandPY%3A%2Ccatid%3A{catid}-{level}-0%2Cnum%3A{num}%2Cpage%3A{page}'


def format_csv(ddir, dir_name, csv_name):
    with open(r'C:\Users\Ph\Desktop\AntAgent\maigoo\{ddir}\{dir}\{name}.csv'.format(ddir=ddir, dir=dir_name, name=csv_name), newline='', encoding='utf-8') as readfile:
        with open(r'C:\Users\Ph\Desktop\AntAgent\maigoo_format\{ddir}\{dir}\{name}.csv'.format(ddir=ddir, dir=dir_name, name=csv_name), 'w', newline='', encoding='utf-8-sig') as writefile:
            reader = csv.reader(readfile)
            writer = csv.writer(writefile)
            writer.writerow(['品牌名称', '公司名称', '信用评分', '联系方式', '企业官网', '企业地址', '企业邮箱', '企业传真'])
            for i, row in enumerate(reader):
                if i > 0:
                    if len(row) > 1:
                        if row[1] not in row[0]:
                            row[0] = row[0] + ' （' + row[1] + '）'
                        if row[3]:
                            row[3] = row[3].replace(',', '；')
                            row[3] = row[3].replace('，', '；')
                            row[3] = row[3].replace('/', '；')
                        else:
                            row[3] = '10000000'
                        print(row)
                        writer.writerow(row)


def crawl_name(list, ddir):
    html = requests.get(url_index_base.format(list=list)).text
    doc = pq(html)
    items = doc('#catsearchbox > dl.category.secondcat > dd > a').items()
    for item in items:
        content = item.attr.href
        listid = re.findall(r'om/brand/list_([0-9]+).html', content, re.S)
        name_dir = item.text().replace('/', '_')
        # print(listid)
        # print(name_dir)
        if listid:
            # print(listid[0])
            print('\n', name_dir, '\n')
            html = requests.get(url_index_base.format(list=listid[0])).text
            doc = pq(html)
            items = doc('#catsearchbox > dl.category.thirdcat > dd > a').items()
            for item in items:
                content = item.attr.href
                catid = re.findall(r'om/brand/list_([0-9]+).html', content, re.S)
                name_csv = item.text().replace('/', '_')
                # print(name_csv)
                if catid:
                    print(name_csv)
                    format_csv(ddir, name_dir, name_csv)


listname = ['建材家居', '电器办公', '穿着打扮', '饮食特产', '汽车工具', '日用品母婴', '服务保健']
listid = [7, 1, 4, 8, 9, 5, 10]


def main():
    for i in range(7):
        ddir = listname[i]
        liid = listid[i]
        crawl_name(liid, ddir)


if __name__ == '__main__':
    main()
