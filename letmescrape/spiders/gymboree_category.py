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

    def _generate_loader(self, selector, response, title, link):
            loader = CategoryLoader(selector=selector, response=response)
            loader.title_out = JoinExcludingEmptyValues(' ')

            loader.add_value('title', title)
            if link is not None:
                link = str(link).split('\'')[1].split('&')[0]
                loader.add_value('link', link)

            return loader

    def parse(self, response):
        for top_level_sel in response.xpath('//div[@id="top-main-menu"]/ul/li[node()]/a'):
            title = top_level_sel.xpath('@title').extract()
            link = top_level_sel.xpath('@href').extract()

            top_level_category_loader = self._generate_loader(top_level_sel, response, title, link)

            request = Request(url=link[0], callback=self.parse_category)
            request.meta['loader'] = top_level_category_loader

            yield request


    def parse_category(self, response):

        top_level_category_loader = response.meta['loader']
        i = 1
        for top_level_sub_column_sel in response.xpath('//div[@id="left-menu"]/h3[contains(@id,"dept")]/a/b'):
            title = top_level_sub_column_sel.xpath('text()').extract()
            link = None
            top_level_sub_column_sel_loader = self._generate_loader(top_level_sub_column_sel, response, title, link)

            sub_category = response.selector.xpath('//div[contains(@id,"left-menu")]/ul[@id="left-menu-ul%d"]/li[node()]/a' % i).extract()

            if len(sub_category) == 0:
                i += 1
            j = 1

            for column_sel in response.xpath('//div[contains(@id,"left-menu")]/ul[@id="left-menu-ul%d"]/li[node()]/a' % i):
                title = column_sel.xpath('text()').extract()
                sale_title = column_sel.xpath('b/font/text()').extract()

                link = column_sel.xpath('@href').extract()

                if len(title) != 0:
                    column_sel_loader = self._generate_loader(column_sel, response, title, link)
                elif len(sale_title) != 0:
                    column_sel_loader = self._generate_loader(column_sel, response, sale_title, link)

                for leaf_sel in response.xpath('//div[@id="left-menu"]/ul[@id="left-menu-ul%d"]/ul[@id="left-submenu-ul%d%d"]/li[node()]/a' % (i, i, j)):
                    title = leaf_sel.xpath('text()').extract()
                    up_title = leaf_sel.xpath('b/font/text()').extract()
                    link = leaf_sel.xpath('@href').extract()

                    if len(title) != 0:
                        leaf_sel_loader = self._generate_loader(leaf_sel, response, title, link)
                    elif len(up_title) != 0:
                        leaf_sel_loader = self._generate_loader(leaf_sel, response, up_title, link)

                    column_sel_loader.add_value('sub_categories', leaf_sel_loader.load_item())

                top_level_sub_column_sel_loader.add_value('sub_categories', column_sel_loader.load_item())
                j += 1

            top_level_category_loader.add_value('sub_categories', top_level_sub_column_sel_loader.load_item())
            i += 1


        yield top_level_category_loader.load_item()


