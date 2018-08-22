import re
import requests
import csv
import time
import random
from config import *


url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&from=webmap&c={citycode}&wd={key_word}&wd2=&pn={page}&nn={nn}&db=0&sug=0&addr=0&pl_data_type=shopping&pl_sub_type=&pl_price_section=0%2C%2B&pl_sort_type=&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=shopping&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=12.894375&rn=50&tn=B_NORMAL_MAP&ie=utf-8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

# 关键字参数
def baidu_search(citycode='194', key_word=KEYWORD, page=0):
    try:
        response = requests.get(url.format(citycode=citycode, key_word=key_word, page=page, nn=10*page), headers=headers)
        if response.status_code != 200:
            print('Get Results Error!!!')
        else:
            json = response.json()
            results = json['content']
            for result in results:
                datas = []
                name = result.get('name')
                datas.append(name)
                address = result.get('addr')
                datas.append(address)
                if 'tel' in result:
                    telephone = result.get('tel')
                else:
                    telephone = ''
                datas.append(telephone)
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
    check = []
    # csv文件名参数name
    with open(r'C:\Users\Ph\Desktop\AntAgent\baidu_map\{name}.csv'.format(name=CSVNAME), 'w', newline='', encoding='utf_8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['名称','地址','联系方式','省份','城市','区县'])
        for num in range(len(citycodelist)):
            print('\n\n\n', citynamelist[num], '\n\n\n')
            page_num = PAGE_NUMBER_MORE    # 爬取页数参数
            for page in range(page_num):
                datas = baidu_search(citycode=citycodelist[num], page=page)
                for data in datas:
                    if data:
                        if data not in check:
                            print(data)
                            check.append(data)
                            writer.writerow(data)
                time.sleep(4 + float(random.randint(1, 800))/200)
                print('\n', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '\n')
        time.sleep(4 + float(random.randint(1, 1200))/200)
        print('\n', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), '\n')


if __name__ == '__main__':
    start = time.time()
    main([131, 289, 132, 48, 53, 58, 321, 150, 92, 36, 66, 233, 360, 268, 288, 176, 127, 158, 218, 315, 75, 146,
          104, 261, 100, 179, 163, 257, 300, 125, 194, 340, 140],
         ['北京市', '上海市', '天津市', '重庆市', '哈尔滨市', '长春市', '沈阳市', '呼和浩特市', '石家庄市',
          '乌鲁木齐市', '兰州市', '西宁市', '西安市', '银川市', '郑州市', '济南市', '太原市', '合肥市',
          '长沙市', '武汉市', '南京市', '成都市', '贵阳市', '昆明市', '南宁市', '拉萨市', '杭州市', '南昌市',
          '广州市', '福州市', '海口市', '厦门市', '深圳市', '珠海市'])
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu
    print('一共花费了{hour}小时{minu}分钟{sec}秒'.format(hour=hour, minu=minu, sec=sec))
