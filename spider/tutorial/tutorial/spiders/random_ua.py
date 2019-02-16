# 设置随机ua
import scrapy


class RandomUaSpider(scrapy.Spider):
    name = 'random_ua'

    def __init__(self):
        self.test_url = 'http://httpbin.org/get'

    def start_requests(self):
        yield scrapy.Request(self.test_url, callback=self.parse)

    def parse(self, response):
        print('\n')
        print(response.request.headers['User-Agent'], '\n')
