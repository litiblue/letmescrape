# -*- coding: utf-8 -*-

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues
from scrapy.http import Request


class GymboreeCategorySpider(CategorySpider):
    name = "gymboree_category"
    allowed_domains = ["gymboree.com"]
    start_urls = (
        'http://www.gymboree.com/',
    )

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.title_out = JoinExcludingEmptyValues(' ')
        loader.add_xpath('title', '@title')
        loader.add_xpath('title', 'text()')
        loader.add_xpath('title', 'b/font/text()')
        loader.add_xpath('title', 'b/text()')
        loader.add_xpath('link', '@href')
        return loader

    def parse(self, response):
        for top_level_sel in response.xpath('//div[@id="top-main-menu"]/ul/li[node()]/a'):
            top_level_category_loader = self.generate_loader(top_level_sel, response)
            yield top_level_category_loader.load_item()

            url = top_level_category_loader.get_output_value('link')
            yield Request(url=url, callback=self.parse_sub, meta={
                'top_level_category_loader': top_level_category_loader
            })

    def parse_sub(self, response):
        for top_sub_category_sel in response.xpath('//div[@id="left-menu"]/h3[contains(@id,"dept")]/a/b'):
            dept_name = top_sub_category_sel.xpath('../../@id').extract()[0]
            top_sub_category_idx = int(dept_name[-1])
            top_sub_category_loader = self.generate_loader(top_sub_category_sel, response)
            top_sub_category_loader.add_value('parent_loader', response.meta['top_level_category_loader'])
            yield top_sub_category_loader.load_item()

            category_idx = 0
            for category_sel in top_sub_category_sel.xpath('../../following-sibling::ul[1]/li/a'):
                category_idx += 1
                category_loader = self.generate_loader(category_sel, response)
                category_loader.add_value('parent_loader', top_sub_category_loader)
                yield category_loader.load_item()

                for leaf_sel in category_sel.xpath(
                                '../following-sibling::ul[@id="left-submenu-ul%d%d"]/li/a' % (
                                top_sub_category_idx, category_idx)):
                    leaf_loader = self.generate_loader(leaf_sel, response)
                    leaf_loader.add_value('parent_loader', category_loader)
                    yield leaf_loader.load_item()
