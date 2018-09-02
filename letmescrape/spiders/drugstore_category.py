# -*- coding: utf-8 -*-
from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.utils import get_absolute_url

class DrugstoreCategorySpider(CategorySpider):
    name = "drugstore_category"
    allowed_domains = ["drugstore.com"]
    start_urls = (
        'http://www.drugstore.com/',
    )

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.add_xpath('title', 'text()')
        loader.add_xpath('title', 'h2/text()')
        loader.add_xpath('link', '@href')
        return loader

    def parse(self, response):
        for sel in response.xpath('//div[@class="webstoremenu"]/ul/li/a'):
            url = get_absolute_url(response, sel.xpath('@href').extract()[0])

            if any(map(lambda x: x in url, [
                'fsa-store', 'gnc-store', 'green-and-natural', 'the-sale'
            ])):
                continue

            top_category_loader = self.generate_loader(sel, response)
            yield top_category_loader.load_item()
            yield Request(url, callback=self.parse_sub, meta={
                'parent_loader': top_category_loader})

    def parse_sub(self, response):
        for sel in response.xpath('//div[@id="refineBycategory"]/a'):
            category_loader = self.generate_loader(sel, response)
            category_loader.add_value('parent_loader', response.meta['parent_loader'])
            yield category_loader.load_item()

            url = get_absolute_url(response, category_loader.get_output_value('link'))
            yield Request(url, callback=self.parse_sub_sub, meta={
                'parent_loader': category_loader
            })

    def parse_sub_sub(self, response):
        for sel in response.xpath('//div[@id="refineBycategory"]/a'):
            category_loader = self.generate_loader(sel, response)
            category_loader.add_value('parent_loader', response.meta['parent_loader'])
            yield category_loader.load_item()
