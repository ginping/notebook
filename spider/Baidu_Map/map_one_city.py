import requests
import csv
import time
import random

url = 'https://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=spot&from=webmap&c={citycode}&wd={key_word}&wd2=&pn={page}&nn={nn}&db=0&sug=0&addr=0&pl_data_type=shopping&pl_sub_type=&pl_price_section=0%2C%2B&pl_sort_type=&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=shopping&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=12.894375&rn=50&tn=B_NORMAL_MAP&ie=utf-8'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}


def baidu_search(citycode='194', key_word='%E8%B4%AD%E7%89%A9%E4%B8%AD%E5%BF%83', page=0):
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


def main():
    with open(r'C:\Users\Ph\Desktop\AntAgent\baidu_map\test.csv', 'w', newline='', encoding='utf_8_sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['名称','地址','联系方式'])
        page_num = 2    # 爬取页数  一页50条
        for page in range(page_num):
            for data in baidu_search(page=page):
                print(data)
                writer.writerow(data)
            time.sleep(5 + float(random.randint(1, 1000))/200)


if __name__ == '__main__':
    main()
