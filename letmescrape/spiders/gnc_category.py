# -*- coding: utf-8 -*-
from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues


class GncCategorySpider(CategorySpider):
    name = "gnc_category"
    allowed_domains = ["gnc.com"]
    start_urls = (
        'http://www.gnc.com/',
    )

    def parse(self, response):
        def _generate_loader(selector):
            loader = CategoryLoader(selector=selector, response=response)
            loader.title_out = JoinExcludingEmptyValues(' ')
            loader.add_xpath('title', 'text()')
            loader.add_xpath('title', 'span/text()')
            loader.add_xpath('title', 'a/@title')
            loader.add_xpath('link', '@href')
            loader.add_xpath('link', 'a/@href')
            return loader

        for top_level_sel in response.xpath('//table[@id="mainNav"]//td[@class="mainNavItem"]'):
            top_level_category_loader = _generate_loader(top_level_sel)
            yield top_level_category_loader.load_item()
            parent_category_loader = top_level_category_loader

            for column_sel in top_level_sel.xpath('div[@class="mainNavSubContainer"]/ul[contains(@class, "mainNavSub")]/li[contains(@class, "subCats")]'):
                category_loader = _generate_loader(column_sel.xpath('ul/li[@class="title"]'))
                category_loader.add_value('parent_loader', parent_category_loader)
                yield category_loader.load_item()

                for leaf_sel in column_sel.xpath('ul/li[contains(@class, "subCat")]'):
                    leaf_loader = _generate_loader(leaf_sel)
                    leaf_loader.add_value('parent_loader', category_loader)
                    yield leaf_loader.load_item()
