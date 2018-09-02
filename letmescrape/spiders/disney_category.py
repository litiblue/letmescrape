# -*- coding: utf-8 -*-
from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues

class DisneyCategorySpider(CategorySpider):
    name = "disney_category"
    allowed_domains = ["disneystore.com"]
    start_urls = (
        'http://www.disneystore.com/',
    )

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.title_out = JoinExcludingEmptyValues(' ')
        loader.add_xpath('title', 'text()')
        loader.add_xpath('title', 'font/text()')
        loader.add_xpath('title', 'a//text()')
        loader.add_xpath('link', '@href')
        loader.add_xpath('link', 'a/@href')
        return loader

    def parse(self, response):

        def _is_head(selector):
            return selector.xpath('self::node()[@class="flyHead"]')

        for top_level_sel in response.css('#mainNav li.navTab > a'):
            top_level_category_loader = self.generate_loader(top_level_sel, response)
            parent_category_loader = top_level_category_loader
            yield top_level_category_loader.load_item()

            for category_sel in top_level_sel.xpath('../section//ul[@class="folColumn"]/li[normalize-space()]'):
                category_loader = self.generate_loader(category_sel, response)

                if _is_head(category_sel):
                    if parent_category_loader is not top_level_category_loader:
                        parent_category_loader.add_value('parent_loader', top_level_category_loader)
                        yield parent_category_loader.load_item()
                    parent_category_loader = category_loader
                else:
                    category_title = category_loader.get_output_value('title')
                    category_link = category_loader.get_output_value('link')

                    is_contained = True
                    if 'See All' in category_title:
                        is_contained = False
                        yield Request(category_link, callback=self.parse_sub,
                                      meta={'parent_loader': parent_category_loader})
                    elif 'Dressing Baby' in category_title:
                        yield Request(category_link, callback=self.parse_sub,
                                      meta={'parent_loader': category_loader})

                    if is_contained:
                        category_loader.add_value('parent_loader', parent_category_loader)
                        yield category_loader.load_item()
            else:
                if parent_category_loader is not top_level_category_loader:
                    parent_category_loader.add_value('parent_loader', top_level_category_loader)
                    yield parent_category_loader.load_item()

    def parse_sub(self, response):
        for category_sel in response.xpath('//nav[@class="leftNav"]/ul[@class="navList"]/li/a'):
            category_loader = self.generate_loader(category_sel, response)
            category_loader.add_value('parent_loader', response.meta['parent_loader'])
            yield category_loader.load_item()