# -*- coding: utf-8 -*-
from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues
from letmescrape.utils import get_absolute_url
from letmescrape.scripts import make_lua_script

class GapCategorySpider(CategorySpider):
    custom_settings = {
        'DOWNLOAD_DELAY': 1
    }
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
        loader.add_xpath('title', '@title')
        loader.add_xpath('link', '@href')
        loader.add_xpath('link', 'a/@href')

        url = get_absolute_url(response, '')
        style_id = selector.xpath('@value').extract()
        if style_id:
            loader.add_value('link', '%s#style=%s' % (url, style_id[0]))

        return loader

    def is_head(self, selector):
        return selector.xpath('self::node()[contains(@class,"header")]')

    def is_category(self, selector):
        return selector.xpath('self::node()[contains(@class,"category")]')

    def parse(self, response):
        for category_sel in response.xpath('//div[@id="mainNavGOL"]/ul[@class="gpnavigation"]/li[not(@id)]'):
            category_loader = self.generate_loader(category_sel, response)
            yield category_loader.load_item()

            url = get_absolute_url(response, category_sel.xpath('a/@href').extract()[0])
            request = Request(url, callback=self.parse_sub, meta={
                'parent_loader': category_loader
            })
            yield request

    def parse_sub(self, response):
        parent_loader = response.meta['parent_loader']

        for category_sel in response.xpath('//div[@id="sideNavCategories"]/ul[@class="category"]/li'):
            category_loader = self.generate_loader(category_sel, response)
            if self.is_head(category_sel):
                category_loader.add_value('parent_loader', parent_loader)
                last_head_loader = category_loader
            elif self.is_category(category_sel):
                category_loader.add_value('parent_loader', last_head_loader)
            yield category_loader.load_item()

            splash_selector_list = ["#sideNavCategories", "#sideNavFacets", ".style-option"]
            script = make_lua_script(splash_selector_list, '&&')

            urls = category_sel.xpath('a/@href').extract()
            if not urls:
                continue
            url = get_absolute_url(response, urls[0])

            request = Request(url, callback=self.parse_sub_sub, meta={
                'parent_loader': category_loader,
                'splash': {
                    'endpoint': 'execute',
                    'args': {'lua_source': script}
                }
            })
            yield request

    def parse_sub_sub(self, response):
        parent_loader = response.meta['parent_loader']

        if response.xpath('//div[@id="lrCategoryNameHeader"]/text()').extract():
            for category_sel in response.xpath('//li[@class="style-option "]/input'):
                category_loader = self.generate_loader(category_sel, response)
                category_loader.add_value('parent_loader', parent_loader)
                item = category_loader.load_item()
                yield item

        else:  # If the result is an error page, request again.
            splash_selector_list = ["#sideNavCategories", "#sideNavFacets", ".style-option"]
            script = make_lua_script(splash_selector_list, '&&')

            url = get_absolute_url(response, '')
            request = Request(url, callback=self.parse_sub_sub, dont_filter=True, meta={
                'parent_loader': parent_loader,
                'splash': {
                    'endpoint': 'execute',
                    'args': {'lua_source': script}
                }
            })
            yield request
