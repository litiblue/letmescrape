# -*- coding: utf-8 -*-

import re
import json

from scrapy import Request
from scrapy.contrib.loader.processor import MapCompose

from letmescrape.utils import get_absolute_url
from letmescrape.processors import JoinExcludingEmptyValues
from base import ProductSpider
from letmescrape.loaders import ProductImageLoader


class VitatraProductSpider(ProductSpider):
    name = "vitatra_product"
    allowed_domains = ["vitatra.com"]
    start_urls = (
        'http://www.vitatra.com/',
    )
    default_values = {
        'brand': 'vitatra',
        'sub_brand': None,
        'default_color': None,
        'colors': None
    }

    def get_url_for_list(self, url, page=1):
        category = re.search(r'category/(.*?)(/|$)', url).group(1)
        list_url = "http://www.vitatra.com/product/ajax_category/%s/page/%s" % (category, (page-1)*40)
        return list_url

    def start_requests(self):
        for url in self.start_urls:
            list_url = self.get_url_for_list(url)
            yield Request(list_url, callback=self.parse_list)

    def extract_values_from_list(self, item, response):
        url = get_absolute_url(response, item.xpath('@href').extract()[0])
        list_images = get_absolute_url(response, item.xpath('img/@src').extract()[0])
        product_number = re.search(r'(?!.*\/)(.*?)$', url).group(1)

        return {
            'url': url,
            'list_images': list_images,
            'product_number': product_number
        }

    def parse_list(self, response):

        def is_json(json_string):
            try:
                json_object = json.loads(json_string)
            except ValueError, e:
                return False
            return True

        for item_sel in response.xpath('//table/tbody//div/div[@class="img"]/a'):
            values_from_list = self.extract_values_from_list(item_sel, response)
            request = Request(values_from_list['url'], callback=self.parse_item)

            request.meta['values_from_list'] = values_from_list
            yield request

        if is_json(response.body):
            yield Request(response.url, callback=self.parse_list, dont_filter=True)

        elif response.xpath('//div[@class="top_sorting"]/div[@class="paging"]/a[@class="next"]/@href'):
            next_url = response.xpath('//div[@class="top_sorting"]/div[@class="paging"]/a[@class="next"]/@href').extract()[0]
            next_page = int(re.search(r'page/(.*?)$', next_url).group(1)) / 40 + 1
            list_url = self.get_url_for_list(response.url, next_page)
            yield Request(list_url, callback=self.parse_list)

    def parse_item(self, response):
        loader = self.get_product_item_loader_with_default_values(response)
        loader.description_out = JoinExcludingEmptyValues('\n')

        values_from_list = response.meta.get('values_from_list', {})
        for key, value in values_from_list.iteritems():
            loader.add_value(key, value)

        loader.add_xpath('title', '//div[@class="sub_detail"]/div[@class="goods_info_img"]/div[@class="goods_info"]/div[@class="tit"]/text()')
        loader.add_xpath('description', '//div[@class="sub_detail"]/div[@class="goods_info_img"]/div[@class="goods_info"]/div[@class="tip"]/div/text()')
        loader.add_xpath('description', '//div[@class="sub_detail"]/div[@id="overview"]/div[@class="cnts"]//text()')
        loader.add_xpath('original_price', '//div[@class="sub_detail"]/div[@class="goods_info_img"]/div[@class="goods_info"]//span[@class="price"]/text()')
        loader.add_xpath('sale_price', '//div[@class="sub_detail"]/div[@class="goods_info_img"]/div[@class="goods_info"]//strong[@class="sale_price"]/text()')

        #images
        for selector in response.xpath('//div[@class="sub_detail"]/div[@class="goods_info_img"]/div[@class="goods_img"]/div[@class="small_img"]/ul/li/a/img'):
            image_loader = ProductImageLoader(response=response, selector=selector)
            image_loader.add_css('thumbnail', '::attr(src)')
            image_loader.add_css('normal_size', '::attr(src)',
                                 MapCompose(lambda url: url.replace('VIEWLIST', 'ZOOM')))
            image_loader.add_css('zoomed', '::attr(src)',
                                 MapCompose(lambda url: url.replace('VIEWLIST', 'ZOOM')))
            loader.add_value('images', image_loader.load_item())

        yield loader.load_item()
