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

        script = make_lua_script('li[rel=shop-all-men]')
        request = Request(response.url, callback=self.parse_redirect_url, meta={
            'splash': {
                    'endpoint': 'execute',
                    'args': {'lua_source': script}
            }
        })

        yield request

    def sale_category_loader(self, selector, response, title, link):
        loader = CategoryLoader(selector=selector, response=response)
        loader.title_out = JoinExcludingEmptyValues(' ')
        loader.add_value('title', title)
        loader.add_value('link', link)

        return loader


    def parse_redirect_url(self, response):

        def _generate_loader(selector):
            loader = CategoryLoader(selector=selector, response=response)
            loader.title_out = JoinExcludingEmptyValues(' ')
            loader.add_xpath('title', '@title')
            loader.add_xpath('title', 'h3/text()')
            loader.add_xpath('title', 'a/text()')
            loader.add_xpath('title', 'a/font/b/text()')
            loader.add_xpath('link', '@href')
            loader.add_xpath('link', 'a/@href')

            return loader

        for top_level_sel in response.xpath('//ul[@id="global-nav"]/li[contains(@class, "navitem  more")]'):
            exist_category = top_level_sel.xpath('a[not(contains(@class,"top-nav last"))]').extract()

            if len(exist_category) != 0:
                top_level_category_loader =_generate_loader(top_level_sel.xpath('a[not(contains(@class,"top-nav last"))]'))

            parent_category_loader = top_level_category_loader

            for column_sel in top_level_sel.xpath('div/div'):
                category_candidate = column_sel.xpath('h3/text()').extract()

                if category_candidate:
                    category_loader = _generate_loader(column_sel)

                    for leaf_sel in column_sel.xpath('ul[@class="nav-items"]/li'):

                        exist_leaf_sel_title_text = leaf_sel.xpath('a/text()').extract()
                        exist_sale_category = leaf_sel.xpath('a/font/b/text()').extract()

                        if len(exist_leaf_sel_title_text) != 0 or len(exist_sale_category):
                            leaf_loader = _generate_loader(leaf_sel)
                            category_loader.add_value('sub_categories', leaf_loader.load_item())

                    parent_category_loader.add_value('sub_categories', category_loader.load_item())

            yield top_level_category_loader.load_item()
