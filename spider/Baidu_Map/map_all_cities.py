import requests
import csv
import time
import random
import re
from config import *


# 通过分析network找到存有json信息的url
url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&from=webmap&c={citycode}&wd={key_word}&wd2=&pn={page}&nn={nn}&db=0&sug=0&addr=0&pl_data_type=shopping&pl_sub_type=&pl_price_section=0%2C%2B&pl_sort_type=&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=shopping&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=12.894375&rn=50&tn=B_NORMAL_MAP&ie=utf-8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# 传入城市id、关键字和页码数  然后返回列表格式的数据
def baidu_search(citycode='194', key_word=KEYWORD, page=0):    # 关键字参数
    try:
        response = requests.get(url.format(citycode=citycode, key_word=key_word, page=page, nn=10*page), headers=headers) # 请求网页
        if response.status_code != 200:
            print('Get Results Error!!!')
        else:
            json = response.json()  # 将字符串json成字典结构
            # if 'content' not in json:
            #     return None
            results = json['content']
            for result in results:
                datas = []
                name = result.get('name')
                datas.append(name)
                address = result.get('addr')
                datas.append(address)
                # 如果有电话号码就添加进datas 没有就添加空值
                if 'tel' in result:
                    telephone = result.get('tel')
                else:
                    telephone = ''
                datas.append(telephone)
                # 添加省份、城市、区县信息到datas
                address_norm = result.get('address_norm')
                info = re.findall('\[(.*?)\(', str(address_norm))
                if len(info) > 0:
                    datas.append(info[0])
                if len(info) > 1:
                    datas.append(info[1])
                if len(info) > 2:
                    datas.append(info[2])
                yield datas
    except Exception as e:
        print(e)
        return None


def main(city_code_list=None, city_name_list=None):
    citycodelist = city_code_list if city_code_list else []
    citynamelist = city_name_list if city_name_list else []
    check = []  # 存储数据比对去重
    # 打开一个csv文件保存数据  name参数是csv文件名
    with open(r'{name}.csv'.format(name=CSVNAME), 'w', newline='', encoding='utf_8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['名称','地址','联系方式','省份','城市','区县'])
        for num in range(len(citycodelist)):
            print('\n\n\n', citynamelist[num], '\n\n\n')
            page_num = PAGE_NUMBER_LESS    # 爬取页数参数
            for page in range(page_num):
                datas = baidu_search(citycode=citycodelist[num], page=page)
                # if not datas:
                #     break
                for data in datas:
                    if data:
                        if data not in check:
                            print(data)
                            check.append(data)
                            writer.writerow(data)
            #  加入随机延时防止ip被封
                time.sleep(4 + float(random.randint(1, 800))/200)
                print('\n', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '\n')
            time.sleep(4 + float(random.randint(1, 1200))/200)
            print('\n', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '\n')


if __name__ == '__main__':
    start = time.time()
    with open(r'BaiduMap_CityCode.txt', 'r', encoding='utf_8_sig') as f:
        lines = f.readlines()
        code = []
        name = []
        for line in lines[1:]:
            citycode = re.findall('([0-9]+)', line, re.S)
            cityname = re.findall(',(.*?)\n', line, re.S)
            code.append(citycode[0])
            name.append(cityname[0])
    main(code, name)
    end = time.time()
    spend = end - start
    hour = spend//3600
    minu = (spend - 3600*hour)//60
    sec = spend - 3600*hour - 60*minu
    print('一共花费了{hour}小时{minu}分钟{sec}秒'.format(hour=hour, minu=minu, sec=sec))
