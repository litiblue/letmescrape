# -*- coding: utf-8 -*-
import re

from scrapy import Request
from scrapy.contrib.loader.processor import MapCompose

from letmescrape.processors import JoinExcludingEmptyValues
from base import ProductSpider
from letmescrape.loaders import ProductImageLoader, ProductColorLoader, ProductReviewLoader

from letmescrape.processors import Date


class CartersProductSpider(ProductSpider):
    name = "carters_product"
    allowed_domains = ["carters.com"]
    start_urls = (
        'http://www.carters.com/',
    )
    list_url_base = "http://www.carters.com/%s?cgid=%s&sz=all&format=ajax"
    default_values = {
        'brand': 'carters',
        'sub_brand': None,
        'default_color': None,
        'colors': None
    }

    def get_ajax_url_for_list(self, url):
        m = re.search('(?!.*\/)(.*?)\?', url)
        N = m.group(1)

        ajax_url = self.list_url_base % (N, N)
        return ajax_url

    def start_requests(self):
        for url in self.start_urls:
            ajax_url = self.get_ajax_url_for_list(url)
            yield Request(ajax_url, callback=self.parse_list)

    def extract_values_from_list(self, item, response):
        url = item.xpath('div[@class="product-tile "]/div[@class="product-image"]/a[@class="thumb-link"]/@href').extract()[0]
        list_images = item.xpath('div[@class="product-tile "]/div[@class="product-image"]/a[@class="thumb-link"]/img/@src').extract()[0]
        product_number = item.xpath('div[@class="product-tile "]/div[@class="product-image"]/a[@class="thumb-link"]/@href').re(r'(?!.*\/)(.*?).html\?')[0]

        return {
            'url': url,
            'list_images': list_images,
            'product_number': product_number
        }

    def parse_list(self, response):
        for item_sel in response.xpath('//div[@class="search-result-content"]/ul[@id="search-result-items"]/li[@class="grid-tile"]'):
            values_from_list = self.extract_values_from_list(item_sel, response)
            request = Request(values_from_list['url'], callback=self.parse_item, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': '1.0'}
                }
            })

            request.meta['values_from_list'] = values_from_list
            yield request

    def parse_item(self, response):
        loader = self.get_product_item_loader_with_default_values(response)

        values_from_list = response.meta.get('values_from_list', {})
        for key, value in values_from_list.iteritems():
            loader.add_value(key, value)

        loader.add_xpath('title', '//h1[@class="product-name"]/text()')
        loader.add_xpath('description', '//div[@class="tab-content"]/text()')
        loader.add_xpath('description', '//div[@class="additional"]/ul/li/text()')
        loader.add_xpath('original_price', '//div[@id="product-content"]/div[@class="product-price"]/span[@class="price-standard"]/text()[2]')
        loader.add_xpath('sale_price', '//div[@id="product-content"]/div[@class="product-price"]/span[contains(@class,"price-sales")]/text()')
        loader.add_xpath('sizes', '//ul[@class="swatches size"]//a/@title')
        loader.add_xpath('default_color', '//ul[@class="swatches color"]/li[@class="selectedColor"]/text()')

        #colors
        for selector in response.xpath('//ul[@class="swatches color"]/li[not(contains(@class, "selectedColor"))]'):
            color_loader = ProductColorLoader(response=response, selector=selector)
            color_loader.add_xpath('name', 'a/@title')
            color_loader.add_xpath('swatch_image', 'a/@style', re='background: url\((.*)\) repeat;')
            loader.add_value('colors', color_loader.load_item())

        #images
        for selector in response.xpath('//div[@class="product-primary-image"]'):
            image_loader = ProductImageLoader(response=response, selector=selector)
            image_loader.add_xpath('thumbnail', 'a//img[@class="primary-image"]/@src')
            image_loader.add_xpath('normal_size', 'a//img[@class="primary-image"]/@src')
            image_loader.add_xpath('zoomed', 'a/@href')
            loader.add_value('images', image_loader.load_item())

        #reviews
        for selector in response.xpath('//div[@id="BVReviewsContainer"]//div[contains(@class,"BVRRContentReview")]'):
            review_loader = ProductReviewLoader(response=response, selector=selector)
            review_loader.body_out = JoinExcludingEmptyValues('\n')
            review_loader.add_css('author', '.BVRRReviewDisplayStyle5BodyUser .BVRRNickname::text')
            review_loader.add_css('title', '.BVRRReviewDisplayStyle5Header .BVRRReviewTitle::text')
            review_loader.add_css('date', '.BVRRReviewDisplayStyle5Header .BVRRReviewDate::text',
                                  MapCompose(Date('%B %d, %Y')))
            review_loader.add_css('body', '.BVRRReviewDisplayStyle5BodyContent .BVRRReviewText::text')
            review_loader.add_css('max_stars', '.BVRRReviewDisplayStyle5Header .BVRRRating img::attr(title)',
                                  re=r'^\s*\d\s*/\s*(\d)\s*$')
            review_loader.add_css('stars', '.BVRRReviewDisplayStyle5Header .BVRRRating img::attr(title)',
                                  re=r'^\s*(\d)\s*/\s*\d\s*$')
            loader.add_value('reviews', review_loader.load_item())

        yield loader.load_item()
