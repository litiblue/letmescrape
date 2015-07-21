# -*- coding: utf-8 -*-

import re

from scrapy import Request
from scrapy.contrib.loader.processor import TakeFirst, MapCompose

from letmescrape.processors import JoinExcludingEmptyValues, Date
from letmescrape.loaders import ProductImageLoader, ProductReviewLoader
from base import ProductSpider


class DrugstoreProductSpider(ProductSpider):
    name = "drugstore_product"
    allowed_domains = ["drugstore.com"]
    start_urls = (
        'http://www.drugstore.com',
    )
    default_values = {
        'brand': None,
        'sub_brand': None,
        'default_color': None,
        'colors': None
    }

    def get_next_link(self, response):
        next_links = response.xpath(
            '//table[@class="srdSrchNavigation"]//a[@class="nextpage"]/@href'
        ).extract()

        if len(next_links) > 0:
            return next_links[0]
        else:
            return None

    def extract_product_number(self, url):
        product_number = re.search(r'(/qxp)(\d+)', url).group(2)
        return product_number

    def parse(self, response):
        next_link = self.get_next_link(response)
        if next_link is None:
            for request in self.parse_list(response):
                yield request
        else:
            next_link = re.sub(r'Nao=18', r'Nao=0', next_link)
            next_link = re.sub(r'ipp=18', r'ipp=80', next_link)
            next_link = 'http://www.drugstore.com' + next_link
            yield Request(next_link, callback=self.parse_page)

    def parse_page(self, response):
        next_link = self.get_next_link(response)
        if next_link is None:
            pass
        else:
            next_link = 'http://www.drugstore.com' + next_link
            yield Request(next_link, callback=self.parse_page)

        for request in self.parse_list(response):
            yield request

    def parse_list(self, response):
        for item_sel in response.xpath('//div[@class="prodImg"]'):
            url = item_sel.xpath('a/@href').extract()[0]
            product_number = self.extract_product_number(url)
            item_url = 'http://www.drugstore.com' + url
            thumbnail = item_sel.xpath('a/img/@src').extract()[0]
            yield Request(item_url, self.parse_item, meta={
                'product_number': product_number,
                'url': item_url,
                'thumbnail': thumbnail
            })

    def parse_item(self, response):
        loader = self.get_product_item_loader_with_default_values(response)
        loader.brand_in = lambda x: x[0][14:] if x else 'no brand'
        loader.brand_out = TakeFirst()
        loader.description_out = JoinExcludingEmptyValues('\n')
        loader.sale_price_out = TakeFirst()

        reviews = self.parse_review(response)
        loader.add_value('reviews', reviews)

        loader.add_value('url', response.meta['url'])
        loader.add_value('product_number', response.meta['product_number'])
        loader.add_xpath('brand', '//a[@class="brandstore"]/text()')
        loader.add_xpath('title', '//div[@id="divCaption"]/h1[@class="captionText"]/text()')
        loader.add_xpath('description', '//div[@id="divPromosPDetail"]')
        loader.add_xpath('description', '//div[@id="divingredientsPDetail"]')
        loader.add_xpath('original_price', '//span[@class="rowMSRP"]/s/text()')
        loader.add_xpath('sale_price', '//div[@id="productprice"]/span/text()')
        loader.add_xpath('sizes', '//div[@id="divCaption"]//span[@class="captionSizeText"]/text()')

        # images
        for sel in response.xpath('//div[@id="divPImage"]'):
            image_loader = ProductImageLoader(response=response, selector=sel)
            image_loader.add_value('thumbnail', response.meta['thumbnail'])
            image_loader.add_xpath('normal_size', 'a/img/@src')
            image_loader.add_xpath('zoomed', 'a/img/@src')

        loader.add_value('images', image_loader.load_item())

        yield loader.load_item()

    def parse_review(self, response):
        reviews = []
        for sel in response.xpath('//div[@class="pr-review-wrap"]'):
            loader = ProductReviewLoader(response=response, selector=sel)
            loader.body_out = JoinExcludingEmptyValues('\n')
            loader.add_xpath('author', 'p[@class="pr-review-author-name"]/span/text()')
            loader.add_xpath('title', 'p[@class="pr-review-rating-headline"]/text()')
            loader.add_xpath('date', 'div[@class="pr-review-rating-wrapper"]/div/text()',
                             MapCompose(Date('%m/%d/%Y')))
            loader.add_xpath('body', 'div/div/p[@class="pr-comments"]/text()')
            loader.add_value('max_stars', '5.0')
            loader.add_css('stars', 'span.pr-rating.pr-rounded::text')
            reviews.append(loader.load_item())
        return reviews
