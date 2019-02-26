# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class ParsShopPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        # use 'accession' as name for the image when it's downloaded
        return [scrapy.Request(x, meta={'image_name': item["name"]})
                for x in item.get('image_urls', [])]

    # write in current folder using the name we chose before
    def file_path(self, request, response=None, info=None):
        return '%s.jpg' % request.meta['image_name']
