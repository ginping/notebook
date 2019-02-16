# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem


class QuotesCnSpider(scrapy.Spider):
    name = 'quotes_cn'
    start_urls = ['http://lab.scrapyd.cn']

    def parse(self, response):
        for quote in response.css('div.quote'):
            
            item = TutorialItem()
            
            content = quote.css('span.text::text').extract_first()
            author = quote.xpath('span/small/text()').extract_first()
            
            item['内容'] = content
            item['作者'] = author
            
            yield item
        
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
