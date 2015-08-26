# -*- coding: utf-8 -*-
from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues
from letmescrape.scripts import make_lua_script
from scrapy import Request


class RalphlaurenCategorySpider(CategorySpider):
    name = "ralphlauren_category"
    allowed_domains = ["ralphlauren.com"]
    start_urls = (
        'http://www.ralphlauren.com/home/index.jsp?geos=1',
    )

    def parse(self, response):
        selector_list = ["li[rel=shop-all-men]"]
        script = make_lua_script(selector_list)
        request = Request(response.url, callback=self.parse_redirect_url, meta={
            'splash': {
                    'endpoint': 'execute',
                    'args': {'lua_source': script}
            }
        })

        yield request

    def parse_redirect_url(self, response):
        def _generate_loader(selector):
            loader = CategoryLoader(selector=selector, response=response)
            loader.title_out = JoinExcludingEmptyValues(' ')
            loader.add_xpath('title', 'text()')
            loader.add_xpath('title', 'font/b/text()')
            loader.add_xpath('title', 'b/font/text()')
            loader.add_xpath('title', 'font/text()')
            loader.add_xpath('title', 'span/text()')
            loader.add_xpath('link', '@href')
            loader.add_xpath('link', 'a/@href')
            return loader

        for top_level_sel in response.xpath('//ul[@id="global-nav"]/li[contains(@class, "navitem  more")]'):
            exist_category = top_level_sel.xpath('a[not(contains(@class,"top-nav last"))]').extract()

            if len(exist_category) != 0:
                top_level_category_loader =_generate_loader(
                    top_level_sel.xpath('a[not(contains(@class,"top-nav last"))]'))
                yield top_level_category_loader.load_item()

            for column_sel in top_level_sel.xpath('div/div'):
                for idx, category_sel in enumerate(column_sel.xpath('h3')):
                    category_loader = _generate_loader(category_sel)
                    category_loader.add_value('parent_loader', top_level_category_loader)
                    yield category_loader.load_item()

                    for leaf_sel in category_sel.xpath('../ul[%d]/li/a' % (idx+1)):
                        leaf_loader = _generate_loader(leaf_sel)
                        leaf_loader.add_value('parent_loader', category_loader)
                        yield leaf_loader.load_item()
