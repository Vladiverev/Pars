from pars_shop.items import ParsItem


import scrapy
from urllib.parse import urljoin


class PycoderSpider(scrapy.Spider):
    name = "py_pars"
    start_urls = [
        'https://hotline.ua/sr/?q=%D1%82%D0%B5%D0%BB%D0%B5%D0%B2%D0%B8%D0%B7%D0%BE%D1%80',
    ]

    visited_urls = []

    def parse(self, response):
        post_list = response.xpath('//div[@class="item-info"]/p//a/@href').extract()
        url = urljoin(response.url, post_list[0])
        yield response.follow(url, callback=self.parse_post)

    def parse_post(self, response):
        item = ParsItem()
        abcd ={}
        all_rovs = response.xpath('//div[contains(@class, "table-row")]')
        row = []
        all_data = []
        for v in all_rovs:
            name_row = v.xpath('div[@class="table-cell cell-4"]/text()').get()
            if  name_row != None and 'Размеры' in name_row:
                name_row = v.xpath('div[@class="table-cell cell-4"]/text()').get()
                data = v.xpath('div[@class="table-cell cell-8"]/p/text()').re(r"\d+")
                abcd[name_row] = data
                row.append(name_row)
                all_data.append(data)
                print(name_row, data)

        import pdb
        pdb.set_trace()
        yield item