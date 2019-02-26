import json
import os.path as path
from pars_shop.items import ParsItem
import scrapy
from urllib.parse import urljoin


class PycoderSpider(scrapy.Spider):
    name = "py_pars"

    def start_requests(self):
        file = path.abspath(path.join('items.json'))

        with open(file) as f:
            data = json.load(f)

        start_urls = ['https://hotline.ua/sr/?q=' + x for x in data['item']]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        post_list = response.xpath('//div[@class="item-info"]/p//a/@href').extract()
        url = urljoin(response.url, post_list[0])

        yield response.follow(url, callback=self.parse_post)

    def parse_post(self, response):
        item = ParsItem()
        item['name'] = response.xpath('//div[@class="heading"]/h1/text()').re(r'\w+')
        item['image_urls'] = [response.xpath('//div[@class="resume-photo cell-3 cell-sm"]/div/img/@src').get()]
        abcd = {}
        all_rovs = response.xpath('//div[contains(@class, "table-row")]')

        for v in all_rovs:
            name_row = v.xpath('div[@class="table-cell cell-4"]/text()').get()

            if name_row != None and 'Размер' in name_row:
                data = v.xpath('div[@class="table-cell cell-8"]/p/text()').get()
                abcd[name_row] = data
                item['length'] = v.xpath('div[@class="table-cell cell-8"]/p/text()').re(r"\d+[,.]*\d*")

        yield item
