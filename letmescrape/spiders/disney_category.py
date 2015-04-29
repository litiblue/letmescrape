# -*- coding: utf-8 -*-
from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues


class DisneyCategorySpider(CategorySpider):
    name = "disney_category"
    allowed_domains = ["disneystore.com"]
    start_urls = (
        'http://www.disneystore.com/',
    )

    def parse(self, response):
        def _generate_loader(selector):
            loader = CategoryLoader(selector=selector, response=response)
            loader.title_out = JoinExcludingEmptyValues(' ')
            loader.add_xpath('title', 'text()')
            loader.add_xpath('title', 'font/text()')
            loader.add_xpath('title', 'a//text()')
            loader.add_xpath('link', '@href')
            loader.add_xpath('link', 'a/@href')
            return loader

        def _is_head(selector):
            return selector.xpath('self::node()[@class="flyHead"]')

        for top_level_sel in response.css('#mainNav li.navTab > a'):
            top_level_category_loader = _generate_loader(top_level_sel)
            parent_category_loader = top_level_category_loader

            for category_sel in top_level_sel.xpath('../section//ul[@class="folColumn"]/li'):
                category_loader = _generate_loader(category_sel)

                if _is_head(category_sel):
                    if parent_category_loader is not top_level_category_loader:
                        top_level_category_loader.add_value('sub_categories', parent_category_loader.load_item())
                    parent_category_loader = category_loader
                else:
                    parent_category_loader.add_value('sub_categories', category_loader.load_item())
            else:
                if parent_category_loader is not top_level_category_loader:
                        top_level_category_loader.add_value('sub_categories', parent_category_loader.load_item())

            yield top_level_category_loader.load_item()