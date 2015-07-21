# -*- coding: utf-8 -*-
from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.utils import get_absolute_url

class DrugstoreCategorySpider(CategorySpider):
    name = "drugstore_category"
    allowed_domains = ["drugstore.com"]
    start_urls = (
        'http://www.drugstore.com/',
    )

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.add_xpath('title', 'text()')
        loader.add_xpath('title', 'h2/text()')
        loader.add_xpath('link', '@href')
        return loader

    def parse(self, response):
        for sel in response.xpath('//div[@class="webstoremenu"]/ul/li/a'):
            url = get_absolute_url(response, sel.xpath('@href').extract()[0])

            if any(map(lambda x: x in url, [
                'fsa-store', 'gnc-store', 'green-and-natural', 'the-sale'
            ])):
                continue

            top_category_loader = self.generate_loader(sel, response)
            yield Request(url, callback=self.parse_sub, meta={
                'top_category_loader': top_category_loader})

    def parse_sub(self, response):
        lev2_sel_list = []
        top_category_loader = response.meta['top_category_loader']
        parent_loader_list = []

        for sel in response.xpath('//div[@id="refineBycategory"]/a'):
            url = get_absolute_url(response, sel.xpath('@href').extract()[0])

            lev2_sel_list.append(sel)
            category_loader = self.generate_loader(sel, response)
            parent_loader_list.append(category_loader)

        # go to the first level2 node
        idx = 0
        url = get_absolute_url(
            response, lev2_sel_list[idx].xpath('@href').extract()[0])
        yield Request(url, callback=self.parse_sub_sub,
                      meta={'lev2_sel_list': lev2_sel_list, 'idx': idx,
                            'top_category_loader': top_category_loader,
                            'parent_loader_list': parent_loader_list})

    def parse_sub_sub(self, response):
        lev2_sel_list = response.meta['lev2_sel_list']
        top_category_loader = response.meta['top_category_loader']
        parent_loader_list = response.meta['parent_loader_list']
        idx = response.meta['idx']

        for sel in response.xpath('//div[@id="refineBycategory"]/a'):
            category_loader = self.generate_loader(sel, response)
            parent_loader_list[idx].add_value('sub_categories',
                                              category_loader.load_item())

        top_category_loader.add_value('sub_categories',
                                      parent_loader_list[idx].load_item())

        if idx == len(lev2_sel_list) - 1:
            yield top_category_loader.load_item()
        else:
            # go to the next level2 node
            idx += 1
            url = get_absolute_url(
                response, lev2_sel_list[idx].xpath('@href').extract()[0])
            yield Request(url, callback=self.parse_sub_sub,
                          meta={'lev2_sel_list': lev2_sel_list, 'idx': idx,
                                'top_category_loader': top_category_loader,
                                'parent_loader_list': parent_loader_list})
