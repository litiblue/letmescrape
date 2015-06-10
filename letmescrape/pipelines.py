# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
from scrapy import signals

from letmescrape.spiders.base import ProductSpider, CategorySpider
from letmescrape.exports import LetMeShopApiCategoriesExporter, LetMeShopApiProductExporter
from letmescrape.items import ProductItem


class PricePipeline(object):
    def process_item(self, item, spider=None):
        if isinstance(item, ProductItem):
            if item.get('original_price', None) is None:
                item['original_price'] = item['sale_price']

            if item['sale_price'] > item['original_price']:
                raise DropItem("sale price should not be greater then original price")

        return item


class RequiredFieldsPipeline(object):
    def process_item(self, item, spider=None):
        for field_name, options in item.fields.items():
            if options.get('required', False) and field_name not in item:
                raise DropItem("%s is required.", field_name)
        else:
            return item


class ExporterProxy(object):
    def __init__(self, exporter=None, enabled=False):
        if enabled and exporter is None:
            raise TypeError('exporters is not given.')
        else:
            self.__exporter = exporter
            self.__enabled = enabled

    def __getattr__(self, name):
        if self.__enabled:
            return getattr(self.__exporter, name)
        else:
            return lambda *args, **kwargs: None


class LetMeShopApiPipeline(object):
    exporter = None

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def set_exporter(self, spider, api_base_url, auth_token, enabled):
        exporter = None
        if enabled:
            if isinstance(spider, CategorySpider):
                exporter = LetMeShopApiCategoriesExporter(spider.site_id, api_base_url, auth_token)
            elif isinstance(spider, ProductSpider):
                exporter = LetMeShopApiProductExporter(spider.site_category_id, spider.job_id, api_base_url, auth_token)
            else:
                raise TypeError('Unknown spider')

        self.exporter = ExporterProxy(exporter, enabled)

    def spider_opened(self, spider):
        enabled = spider.settings['LETMESHOP_API_PIPELINE_ENABLED']
        api_base_url = spider.settings['LETMESHOP_API_BASE_URL']
        auth_token = spider.settings['LETMESHOP_API_AUTH_TOKEN']

        self.set_exporter(spider, api_base_url, auth_token, enabled)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item