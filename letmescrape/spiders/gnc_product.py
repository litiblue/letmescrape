# -*- coding: utf-8 -*-

from scrapy.contrib.loader.processor import TakeFirst
from scrapy import Request
from scrapy.contrib.loader.processor import MapCompose

from letmescrape.utils import get_absolute_url
from letmescrape.processors import JoinExcludingEmptyValues
from base import ProductSpider
from letmescrape.loaders import ProductImageLoader, ProductReviewLoader
from letmescrape.processors import Date

class CartersProductSpider(ProductSpider):
    name = "gnc_product"
    allowed_domains = ["gnc.com"]
    start_urls = (
        'http://www.gnc.com/',
    )
    default_values = {
        'brand': 'gnc',
        'sub_brand': None,
        'default_color': None,
        'colors': None
    }

    def get_url_for_list(self, url, num_items=10000):
        list_url = "%s&ppg=%s" % (url, num_items)
        return list_url

    def start_requests(self):
        for url in self.start_urls:
            list_url = self.get_url_for_list(url)
            yield Request(list_url, callback=self.parse_list)

    def extract_values_from_list(self, item, response):
        url = get_absolute_url(response, item.xpath('div[@class="prodImage"]/a/@href').extract()[0])
        list_images = item.xpath('div[@class="prodImage"]/a/img/@src').extract()[0]

        return {
            'url': url,
            'list_images': list_images
        }

    def parse_list(self, response):
        for item_sel in response.xpath('//div[@id="mainContent"]//ol[@id="products"]/li[@class="productListing"]'):
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
        loader.original_price_out = TakeFirst()

        values_from_list = response.meta.get('values_from_list', {})
        for key, value in values_from_list.iteritems():
            loader.add_value(key, value)

        loader.add_xpath('product_number', '//div[@id="product-info"]/div[contains(@class,"product-info-top")]/div/span[@class="product-number"]/text()', re='Item #(.*)')
        loader.add_xpath('title', '//div[@id="product-title"]/h2/text()')
        loader.add_xpath('description', '//dl[@class="product-info-tabs"]/dd[@id="tab-description-content"]//text()')
        loader.add_xpath('original_price', '//div[@id="product-info"]/div[contains(@class,"product-price")]/p[@class="was"]/text()', re='Price: (.*)')
        loader.add_xpath('original_price', '//div[@id="product-info"]/div[contains(@class,"product-price")]/p[@class="now"]/text()', re='Price: (.*)')
        loader.add_xpath('sale_price', '//div[@id="product-info"]/div[contains(@class,"product-price")]/p[@class="now"]/text()', re='Price: (.*)')
        loader.add_xpath('default_color', '//div[@id="product-info"]/div[@class="product-info-top product-sprite"]/p[@class="product-size"]/text()')

        #images
        for selector in response.xpath('//div[@class="main-image-wrap"]/img[@class="prod-image"]'):
            image_loader = ProductImageLoader(response=response, selector=selector)
            image_loader.add_xpath('thumbnail', '@src')
            image_loader.add_xpath('normal_size', '@src')
            image_loader.add_xpath('zoomed', '@data-enh')
            loader.add_value('images', image_loader.load_item())

        #reviews
        for selector in response.xpath('//div[@id="TTreviewsWrapper"]/div[@id="TTreviews"]/div[@class="TTreview"]'):
            review_loader = ProductReviewLoader(response=response, selector=selector)
            review_loader.body_out = JoinExcludingEmptyValues('\n')
            review_loader.add_xpath('author', 'div[@class="TTrevCol3"]/div/a/span[@itemprop="reviewer"]/text()')
            review_loader.add_xpath('title', 'div[@class="TTrevCol2"]/div[@class="TTreviewTitle"]/text()')
            review_loader.add_xpath('date', 'div[@class="TTrevCol3"]/div[@itemprop="dtreviewed"]/text()',
                                  MapCompose(Date('%B %d, %Y')))
            review_loader.add_xpath('body', 'div[@class="TTrevCol2"]/div[@class="TTreviewBody"]/text()')
            review_loader.add_xpath('max_stars', '../../../div[@class="TTreviewSummary"]/div[@class="TT2left"]/span[@class="TTavgRate"]/text()', re=r'/ (.*)')
            review_loader.add_xpath('stars', '@rating')
            loader.add_value('reviews', review_loader.load_item())

        yield loader.load_item()
