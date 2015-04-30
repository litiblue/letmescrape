# -*- coding: utf-8 -*-
from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues


class CartersCategorySpider(CategorySpider):
    name = "carters_category"
    allowed_domains = ["carters.com"]
    start_urls = (
        'http://www.carters.com/',
    )

    def parse(self, response):
        def _generate_loader(selector):
            loader = CategoryLoader(selector=selector, response=response)
            loader.title_out = JoinExcludingEmptyValues(' ')
            loader.add_xpath('title', 'text()')
            loader.add_xpath('title', 'a/text()')
            loader.add_xpath('title', 'a/span/text()')
            loader.add_xpath('link', '@href')
            loader.add_xpath('link', 'a/@href')
            return loader

        for top_level_sel in response.xpath('//li[contains(@class, "topCat") and not(contains(@class, "mobilevisible"))]/a[@href]'):
            top_level_category_loader = _generate_loader(top_level_sel)
            parent_category_loader = top_level_category_loader

            for column_sel in top_level_sel.xpath('../div[@class="subnav"]/div[@class="subnav-categories"]/div[contains(@class, "column") and not(contains(@class, "desktopvisible"))]'):
                i = 1
                if len(column_sel.xpath('h3')) > 0:
                    for category_sel in column_sel.xpath('h3'):
                        category_loader = _generate_loader(category_sel)

                        for leaf_sel in column_sel.xpath('ul[%d]/li[not(contains(@class, "mobilevisible"))]' % i):
                            leaf_loader = _generate_loader(leaf_sel)
                            category_loader.add_value('sub_categories', leaf_loader.load_item())

                        parent_category_loader.add_value('sub_categories', category_loader.load_item())
                        i += 1
                else:
                    for leaf_sel in column_sel.xpath('ul[%d]/li[not(contains(@class, "mobilevisible"))]' % i):
                        leaf_loader = _generate_loader(leaf_sel)
                        parent_category_loader.add_value('sub_categories', leaf_loader.load_item())

            yield top_level_category_loader.load_item()