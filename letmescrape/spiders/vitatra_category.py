# -*- coding: utf-8 -*-
from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues
from letmescrape.utils import get_absolute_url


class VitatraCategorySpider(CategorySpider):
    name = "vitatra_category"
    allowed_domains = ["vitatra.com"]
    start_urls = (
        'http://www.vitatra.com/',
    )

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.title_out = JoinExcludingEmptyValues(' ')
        loader.add_xpath('title', 'text()')
        loader.add_xpath('title', 'a/text()')
        loader.add_xpath('title', 'span/text()')
        loader.add_xpath('link', '@href')
        loader.add_xpath('link', 'a/@href')
        return loader

    def parse(self, response):
        for top_level_sel in response.xpath('//div[@class="category"]/div[@class="category_static"]/ul/li/a'):
            top_level_category_loader = self.generate_loader(top_level_sel, response)
            url = get_absolute_url(response, top_level_sel.xpath('@href').extract()[0])
            request = Request(url, callback=self.parse_sub)
            request.meta['top_level_category_loader'] = top_level_category_loader
            yield request

    def parse_sub(self, response):
        top_level_category_loader = response.meta['top_level_category_loader']
        parent_category_loader = top_level_category_loader

        for category_sel in response.xpath('//div[@class="lnb"]/div/ul/li/a'):
            category_loader = self.generate_loader(category_sel, response)
            parent_category_loader.add_value('sub_categories', category_loader.load_item())

        yield top_level_category_loader.load_item()