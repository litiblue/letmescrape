# -*- coding: utf-8 -*-

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues

from scrapy import Request

class RalphlaurenCategorySpider(CategorySpider):
    name = "ralphlauren_category"
    # allowed_domains = ["ralphlauren.com"]
    start_urls = (
        'http://www.ralphlauren.com',
    )

    def parse(self, response):

        splash = 'http://192.168.59.103:8050/render.html?wait=1&render_all=1&url=http://www.ralphlauren.com/home/index.jsp?geos=1'
        request = Request(splash, callback=self.parse_redirect_url)
        request.meta['original_url'] = 'http://www.ralphlauren.com/home/index.jsp?geos=1'

        yield request

    def parse_redirect_url(self, response):
        url = response.meta['original_url']
        response = response.replace(url=url)

        def _generate_loader(selector):
            loader = CategoryLoader(selector=selector, response=response)
            loader.title_out = JoinExcludingEmptyValues(' ')
            loader.add_xpath('title', '@title')
            loader.add_xpath('title', 'h3/text()')
            loader.add_xpath('title', 'a/text()')
            loader.add_xpath('link', '@href')
            loader.add_xpath('link', 'a/@href')

            return loader

        for top_level_sel in response.xpath('//ul[@id="global-nav"]/li[contains(@class, "navitem")][node()]'):
            top_level_category_loader =_generate_loader(top_level_sel.xpath('a[not(contains(@class,"top-nav last"))]'))
            parent_category_loader = top_level_category_loader

            for column_sel in top_level_sel.xpath('div/div'):
                category_candidate = column_sel.xpath('h3/text()').extract()

                if category_candidate:
                    category_loader = _generate_loader(column_sel)

                    for leaf_sel in column_sel.xpath('ul[@class="nav-items"]/li'):
                        leaf_loader = _generate_loader(leaf_sel)
                        category_loader.add_value('sub_categories', leaf_loader.load_item())

                    parent_category_loader.add_value('sub_categories', category_loader.load_item())

            yield top_level_category_loader.load_item()
