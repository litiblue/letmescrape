# -*- coding: utf-8 -*-
from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.utils import get_absolute_url


class IherbCategorySpider(CategorySpider):
    name = "iherb_category"
    allowed_domains = ["iherb.com"]
    start_urls = (
        'http://www.iherb.com/',
    )

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'iher-pref':'ctd=www&sccode=KR&lan=ko-KR&scurcode=USD&lchg=1&svcode=KR&vlan=ko-KR&vcurcode=USD&ifv=i'}, callback=self.parse)

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.add_xpath('title', 'text()')
        loader.add_xpath('link', '@href')
        return loader

    def parse(self, response):
        for top_level_sel in response.xpath('//nav[@id="iherb-main-nav"]/div/ul/li/a'):
            top_level_category_loader = self.generate_loader(top_level_sel, response)
            yield top_level_category_loader.load_item()

            url = get_absolute_url(response, top_level_sel.xpath('@href').extract()[0])
            request = Request(url, callback=self.parse_sub)
            request.meta['top_level_category_loader'] = top_level_category_loader
            yield request

    def parse_sub(self, response):
        top_level_category_loader = response.meta['top_level_category_loader']
        parent_category_loader = top_level_category_loader

        for category_sel in response.xpath('//div[@id="divCategories"]/div/ul[@class="categories"]/li/a'):
            category_loader = self.generate_loader(category_sel, response)
            category_loader.add_value('parent_loader', parent_category_loader)
            yield category_loader.load_item()
