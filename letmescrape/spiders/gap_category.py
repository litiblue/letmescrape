# -*- coding: utf-8 -*-
from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues
from letmescrape.utils import get_absolute_url


class GapCategorySpider(CategorySpider):
    name = "gap_category"
    allowed_domains = ["gap.com"]
    start_urls = (
        'http://www.gap.com/',
    )

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.title_out = JoinExcludingEmptyValues(' ')
        loader.add_xpath('title', 'text()')
        loader.add_xpath('title', 'a/text()')
        loader.add_xpath('link', '@href')
        loader.add_xpath('link', 'a/@href')
        return loader

    def is_head(self, selector):
        return selector.xpath('self::node()[contains(@class,"header")]')

    def is_category(self, selector):
        return selector.xpath('self::node()[contains(@class,"category")]')

    def parse(self, response):
        for top_level_sel in response.xpath('//div[@id="mainNavGOL"]/ul[@class="gpnavigation"]/li[not(@id)]'):
            top_level_category_loader = self.generate_loader(top_level_sel, response)
            url = get_absolute_url(response, top_level_sel.xpath('a/@href').extract()[0])
            request = Request(url, callback=self.parse_sub)
            request.meta['top_level_category_loader'] = top_level_category_loader
            yield request

    def parse_sub(self, response):
        top_level_category_loader = response.meta['top_level_category_loader']
        parent_category_loader = top_level_category_loader

        for category_sel in response.xpath('//div[@id="sideNavCategories"]/ul[@class="category"]/li'):
            category_loader = self.generate_loader(category_sel, response)
            if self.is_head(category_sel):
                if parent_category_loader is not top_level_category_loader:
                        top_level_category_loader.add_value('sub_categories', parent_category_loader.load_item())
                parent_category_loader = category_loader
            elif self.is_category(category_sel):
                parent_category_loader.add_value('sub_categories', category_loader.load_item())
        else:
            if parent_category_loader is not top_level_category_loader:
                top_level_category_loader.add_value('sub_categories', parent_category_loader.load_item())

        yield top_level_category_loader.load_item()