# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from Mycrawl.items import MaoyanItem


class MaoyanSpider(scrapy.Spider):
    name = 'maoyan3'
    # allowed_domains = ['maoyan.com']
    # start_urls = ['http://maoyan.com/board/6']
    url = 'http://maoyan.com/board/6'

    def start_requests(self):
        # url = 'http://maoyan.com/board/4'
        yield Request(self.url, callback=self.parse)

    def parse(self, response):
        item = MaoyanItem()
        selector = Selector(response)
        active = selector.xpath('//ul[@class="navbar"]/li/a[@class="active"]/text()').extract()
        tops = selector.xpath('//dd/i/text()').extract()
        movies = selector.xpath('//div[@class="movie-item-info"]')
        for i, content in enumerate(movies):
            title = content.xpath('p[@class="name"]/a/text()').extract()
            star = content.xpath('p[2]/text()').extract()
            releasetime = content.xpath('p[3]/text()').extract()

            item['top'] = active[-1] + '第' + tops[i]
            item['title'] = title[0]
            item['star'] = star[0].replace(' ', '').replace('\n', '')
            if releasetime:
                item['releasetime'] = releasetime[0].replace(' ', '').replace('\n', '')
            else:
                item['releasetime'] = ''
            yield item

        nextpage = selector.xpath('//ul[@class="list-pager"]/li/a//@href').extract()
        if nextpage:
            nextpage = nextpage[-1]

            yield Request(self.url + str(nextpage), callback=self.parse)
