# -*- coding: utf-8 -*-
from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues

class CartersCategorySpider(CategorySpider):
    name = "carters_category"
    allowed_domains = ["carters.com"]
    start_urls = (
        'http://www.carters.com/',
    )

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.title_out = JoinExcludingEmptyValues(' ')
        loader.add_xpath('title', 'text()')
        loader.add_xpath('title', 'a/text()')
        loader.add_xpath('title', 'a/span/text()')
        loader.add_xpath('link', '@href')
        loader.add_xpath('link', 'a/@href')
        return loader

    def parse(self, response):

        for top_level_sel in response.xpath('//li[contains(@class, "topCat") and not(contains(@class, "mobilevisible"))]/a[@href]'):
            top_level_category_loader = self.generate_loader(top_level_sel, response)
            parent_category_loader = top_level_category_loader
            yield top_level_category_loader.load_item()

            for column_sel in top_level_sel.xpath('../div[@class="subnav"]/div[@class="subnav-categories"]/div[contains(@class, "column") and not(contains(@class, "desktopvisible"))]'):
                i = 1
                if len(column_sel.xpath('h3')) > 0:
                    for category_sel in column_sel.xpath('h3'):
                        category_loader = self.generate_loader(category_sel, response)
                        category_loader.add_value('parent_loader', parent_category_loader)
                        yield category_loader.load_item()

                        for leaf_sel in column_sel.xpath('ul[%d]/li[not(contains(@class, "mobilevisible"))]' % i):
                            leaf_loader = self.generate_loader(leaf_sel, response)
                            if 'oshkosh' in leaf_loader.get_output_value('title').lower():
                                continue
                            leaf_loader.add_value('parent_loader', category_loader)
                            yield leaf_loader.load_item()
                            yield Request(leaf_sel.xpath('a/@href').extract()[0],
                                          callback=self.parse_sub, meta={'parent_loader': leaf_loader})
                        i += 1
                else:
                    for leaf_sel in column_sel.xpath('ul[%d]/li[not(contains(@class, "mobilevisible"))]' % i):
                        leaf_loader = self.generate_loader(leaf_sel, response)
                        leaf_loader.add_value('parent_loader', parent_category_loader)
                        yield leaf_loader.load_item()
                        yield Request(leaf_sel.xpath('a/@href').extract()[0],
                                      callback=self.parse_sub, meta={'parent_loader': leaf_loader})

    def parse_sub(self, response):
        for category_sel in response.xpath('//div[contains(@class, "Style clearfix")]/ul/li/a'):
            category_loader = self.generate_loader(category_sel, response)
            category_loader.add_value('parent_loader', response.meta['parent_loader'])
            yield category_loader.load_item()
