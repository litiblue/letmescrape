# -*- coding: utf-8 -*-

from collections import defaultdict

from scrapy import Request

from base import CategorySpider
from letmescrape.loaders import CategoryLoader
from letmescrape.processors import JoinExcludingEmptyValues


class CartersCategorySpider(CategorySpider):
    name = "carters_category"
    allowed_domains = ["carters.com"]
    start_urls = (
        'http://www.carters.com/',
    )

    def item_from_dfs(self, parent_loader, tree_dict):
        for child_loader in tree_dict[parent_loader]:
            parent_loader.add_value('sub_categories', self.item_from_dfs(child_loader, tree_dict))
        return parent_loader.load_item()

    def generate_loader(self, selector, response):
        loader = CategoryLoader(selector=selector, response=response)
        loader.title_out = JoinExcludingEmptyValues(' ')
        loader.add_xpath('title', 'text()')
        loader.add_xpath('title', 'a/text()')
        loader.add_xpath('title', 'a/span/text()')
        loader.add_xpath('link', '@href')
        loader.add_xpath('link', 'a/@href')
        return loader

    def parse(self, response):
        tree_dict = defaultdict(list)

        for top_level_sel in response.xpath('//li[contains(@class, "topCat") and not(contains(@class, "mobilevisible"))]/a[@href]'):
            top_level_category_loader = self.generate_loader(top_level_sel, response)
            parent_category_loader = top_level_category_loader

            leaf_sel_list = []
            parent_loader_list = []

            for column_sel in top_level_sel.xpath('../div[@class="subnav"]/div[@class="subnav-categories"]/div[contains(@class, "column") and not(contains(@class, "desktopvisible"))]'):
                i = 1
                if len(column_sel.xpath('h3')) > 0:
                    for category_sel in column_sel.xpath('h3'):
                        category_loader = self.generate_loader(category_sel, response)

                        for leaf_sel in column_sel.xpath('ul[%d]/li[not(contains(@class, "mobilevisible"))]' % i):
                            leaf_loader = self.generate_loader(leaf_sel, response)
                            tree_dict[category_loader].append(leaf_loader)

                            leaf_sel_list.append(leaf_sel)
                            parent_loader_list.append(leaf_loader)

                        tree_dict[parent_category_loader].append(category_loader)
                        i += 1
                else:
                    for leaf_sel in column_sel.xpath('ul[%d]/li[not(contains(@class, "mobilevisible"))]' % i):
                        leaf_loader = self.generate_loader(leaf_sel, response)
                        tree_dict[parent_category_loader].append(leaf_loader)

                        leaf_sel_list.append(leaf_sel)
                        parent_loader_list.append(leaf_loader)
            idx = 0
            yield Request(leaf_sel_list[idx].xpath('a/@href').extract()[0], callback=self.parse_sub,
                          meta={'idx': idx, 'leaf_sel_list': leaf_sel_list, 'parent_loader_list': parent_loader_list,
                                'tree_dict': tree_dict, 'top_level_category_loader': top_level_category_loader})

    def parse_sub(self, response):
        idx = response.meta['idx']
        leaf_sel_list = response.meta['leaf_sel_list']
        parent_loader_list = response.meta['parent_loader_list']
        tree_dict = response.meta['tree_dict']
        top_level_category_loader = response.meta['top_level_category_loader']

        parent_category_loader = parent_loader_list[idx]
        for category_sel in response.xpath('//div[contains(@class, "Style clearfix")]/ul/li/a'):
            category_loader = self.generate_loader(category_sel, response)
            tree_dict[parent_category_loader].append(category_loader)

        if idx < len(leaf_sel_list)-1:
            idx += 1
            yield Request(leaf_sel_list[idx].xpath('a/@href').extract()[0], callback=self.parse_sub,
                          meta={'idx': idx, 'leaf_sel_list': leaf_sel_list, 'parent_loader_list': parent_loader_list,
                                'tree_dict': tree_dict, 'top_level_category_loader': top_level_category_loader})
        else:
            yield self.item_from_dfs(top_level_category_loader, tree_dict)
