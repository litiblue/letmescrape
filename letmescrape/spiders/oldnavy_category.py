# -*- coding: utf-8 -*-
from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues
from letmescrape.utils import get_absolute_url

class OldnavyCategorySpider(CategorySpider):
    name = "oldnavy_category"
    allowed_domains = ["oldnavy.gap.com"]
    start_urls = (
        'http://oldnavy.gap.com/',
    )

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.title_out = JoinExcludingEmptyValues(' ')
        loader.add_xpath('title', 'text()')
        loader.add_xpath('title', 'a/text()')
        loader.add_xpath('title', 'img/@alt')
        loader.add_xpath('link', '@href')
        loader.add_xpath('link', 'a/@href')
        return loader

    def is_head(self, selector):
        return selector.xpath('self::node()[contains(@class,"header")]')

    def is_category(self, selector):
        return selector.xpath('self::node()[contains(@class,"category")]')

    def parse(self, response):
        for top_level_sel in response.xpath('//div[@id="divisionContainer"]/ul/li[@class="division"]/a'):
            top_level_category_loader = self.generate_loader(top_level_sel, response)
            url = get_absolute_url(response, top_level_sel.xpath('@href').extract()[0])
            request = Request(url, callback=self.parse_sub)
            request.meta['top_level_category_loader'] = top_level_category_loader
            yield request

    def parse_sub(self, response):
        top_level_category_loader = response.meta['top_level_category_loader']
        parent_category_loader = top_level_category_loader
        yield top_level_category_loader.load_item()

        for category_sel in response.xpath('//div[@id="sideNavCategories"]/ul[@class="category"]/li'):
            category_loader = self.generate_loader(category_sel, response)
            if self.is_head(category_sel):
                category_loader.add_value('parent_loader', top_level_category_loader)
                yield category_loader.load_item()
                parent_category_loader = category_loader
            elif self.is_category(category_sel):
                if category_sel.xpath('a/text()').extract()[0] != 'GiftCards':
                    category_loader.add_value('parent_loader', parent_category_loader)
                    yield category_loader.load_item()
