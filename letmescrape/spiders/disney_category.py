# -*- coding: utf-8 -*-
from collections import defaultdict
from scrapy import Request

from base import CategorySpider
from letmescrape.utils import get_absolute_url
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

    def item_from_dfs(self, parent_loader, tree):
        for child_loader in tree[parent_loader]:
            child_item = self.item_from_dfs(child_loader, tree)
            parent_loader.add_value('sub_categories', child_item)
        return parent_loader.load_item()

    def parse(self, response):
        def _is_head(selector):
            return selector.xpath('self::node()[@class="flyHead"]')

        for top_level_sel in response.css('#mainNav li.navTab > a'):
            top_level_category_loader = self.generate_loader(top_level_sel, response)
            parent_category_loader = top_level_category_loader

            # init
            tree = defaultdict(list)
            parent_loader_list = []
            sel_list = []

            for category_sel in top_level_sel.xpath('../section//ul[@class="folColumn"]/li[normalize-space()]'):
                category_loader = self.generate_loader(category_sel, response)

                if _is_head(category_sel):
                    if parent_category_loader is not top_level_category_loader:
                        tree[top_level_category_loader].append(parent_category_loader)
                    parent_category_loader = category_loader
                else:
                    category_item = category_loader.load_item()
                    if 'See All' in category_item['title'][:7]:
                        parent_loader_list.append(parent_category_loader)
                        sel_list.append(category_sel)
                    else:
                        tree[parent_category_loader].append(category_loader)
            else:
                if parent_category_loader is not top_level_category_loader:
                    tree[top_level_category_loader].append(parent_category_loader)

            if sel_list:
                idx = 0
                url = sel_list[idx].xpath('a/@href').extract()[0]
                url = get_absolute_url(response, url)
                yield Request(url, callback=self.parse_sub, dont_filter=True, meta={
                    'tree': tree, 'sel_list': sel_list, 'parent_loader_list': parent_loader_list,
                    'idx': idx, 'top_level_category_loader': top_level_category_loader})
            else:
                yield self.item_from_dfs(top_level_category_loader, tree)

    def parse_sub(self, response):
        tree = response.meta['tree']
        sel_list = response.meta['sel_list']
        parent_loader_list = response.meta['parent_loader_list']
        idx = response.meta['idx']
        top_level_category_loader = response.meta['top_level_category_loader']

        def _is_exist(parent_loader, category_loader):
            for child_loader in tree[parent_loader]:
                if child_loader.load_item()['link'] == category_loader.load_item()['link']:
                    return True
            return False

        for category_sel in response.xpath('//nav[@class="leftNav"]/ul[@class="navList"]/li/a'):
            category_loader = self.generate_loader(category_sel, response)
            if not _is_exist(parent_loader_list[idx], category_loader):
                tree[parent_loader_list[idx]].append(category_loader)

        if idx < len(sel_list)-1:
            idx += 1
            url = sel_list[idx].xpath('a/@href').extract()[0]
            url = get_absolute_url(response, url)
            yield Request(url, callback=self.parse_sub, dont_filter=True, meta={
                'tree': tree, 'sel_list': sel_list, 'parent_loader_list': parent_loader_list,
                'idx': idx, 'top_level_category_loader': top_level_category_loader})
        else:
            yield self.item_from_dfs(top_level_category_loader, tree)
