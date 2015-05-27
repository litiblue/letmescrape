# -*- coding: utf-8 -*-
from scrapy import Request
from scrapy.contrib.loader.processor import MapCompose

from letmescrape.processors import JoinExcludingEmptyValues
from base import ProductSpider
from letmescrape.loaders import ProductImageLoader, ProductColorLoader, ProductReviewLoader
from letmescrape.processors import Date
import unicodedata

class GymboreeProductSpider(ProductSpider):
    name = "gymboree_product"
    start_urls = (
        'http://www.gymboree.com/',
    )
    default_values = {
        'brand': 'gymboree',
        'sub_brand': None,
        'default_color': None,
        'colors': None
    }

    def start_requests(self):

        for url in self.start_urls:
            replace_url = url+ "&pageClicked=0"
            yield Request(replace_url, callback=self.parse_list)

    def extract_values_from_list(self, item, response):
        url_candidate = item.xpath('div[contains(@class, "collection-pricing")]/a/@href').extract()
        if url_candidate:
            url = url_candidate[0]
        else:
            url = item.xpath('div[@class="cat_prodImg"]/a[@class="product-image"]/@href').extract()

            if url:
                url = url[0]
            else:
                return None

        list_images = item.xpath('div[@class="cat_prodImg"]/a[@class="product-image"]/img/@src').extract()[0]

        return {
            'url': url,
            'list_images': list_images
        }

    def parse_list(self, response):

        for item_sel in response.xpath('//div[@class="product-list-data"]/div[contains(@class, "c")][node()]'):
            values_from_list = self.extract_values_from_list(item_sel, response)

            if values_from_list:
                splash = 'http://192.168.59.103:8050/render.html'
                url = splash + '?wait=2&render_all=1&url='+values_from_list['url']

                request = Request(url=url, callback=self.parse_item)
                request.meta['values_from_list'] = values_from_list

                yield request
            else:
                yield

    def parse_item(self, response):
        url = response.meta['values_from_list']
        response = response.replace(url=url['url'])
        loader = self.get_product_item_loader_with_default_values(response)
        values_from_list = response.meta.get('values_from_list', {})
        for key, value in values_from_list.iteritems():
            loader.add_value(key, value)

        loader.add_xpath('product_number', '//div[@id="left_block"]/div[@id="product-description"]/h4/span[@id="p-code"]/text()')
        loader.add_xpath('title', '//div[@id="left_block"]/div[@id="product-description"]/h3/span[@id="p-title"]/text()')
        loader.add_xpath('description', '//div[@id="content"]/div[@id="left_block"]/div[@id="product-description"]/ul[@id="p-options"]/li[node()]/text()')
        loader.add_xpath('sizes', '//ul[@id="size-options-ul"]/li/@title')

        original_price = response.xpath('//div[@id="reg-price"]/span[@id="reg-price-s"]/span[@class="reg-price-dollars"]/text()').extract()[0]


        sale_price_candidates = response.xpath('//div[@id="sale-price"]/span[@id="sale-price-s"]/span[@class="reg-price-dollars"]/text()').extract()
        if sale_price_candidates:
            sale_price = sale_price_candidates[0]
        else:
            sale_price = original_price
        now_price = response.xpath('//div[@class="product-options"]/div[@id="b-price"]/span[@id="b-price-s"]/span[@class="reg-price-dollars"]/text()').extract()
        if now_price:
            sale_price = now_price[0]

        loader.add_value('original_price', original_price)
        loader.add_value('sale_price', sale_price)

        #images
        for selector in response.xpath('//div[@id="product-image-section"]/a[@id="a-p-picture"]/img[@id="p-picture"]'):
            image_loader = ProductImageLoader(response=response, selector=selector)
            image_loader.add_xpath('normal_size', '@src')
            image_loader.add_xpath('zoomed', '@src')
            loader.add_value('images', image_loader.load_item())

        #reviews
        for selector in response.xpath('//div[@class="pr-contents-wrapper"]/div[@class="pr-review-wrap"][node()]'):
            review_loader = ProductReviewLoader(response=response, selector=selector)
            review_loader.body_out = JoinExcludingEmptyValues('\n')

            review_month = unicodedata.normalize('NFKD', selector.xpath('div[@class="pr-review-rating-wrapper"]/div[@class="pr-review-author-date pr-rounded"]/p[@class="pr-date-month"]/text()').extract()[0]).encode('utf8', 'ignore')
            review_day = unicodedata.normalize('NFKD', selector.xpath('div[@class="pr-review-rating-wrapper"]/div[@class="pr-review-author-date pr-rounded"]/p[@class="pr-date-day"]/text()').extract()[0]).encode('utf8', 'ignore')
            review_year = unicodedata.normalize('NFKD', selector.xpath('div[@class="pr-review-rating-wrapper"]/div[@class="pr-review-author-date pr-rounded"]/p[@class="pr-date-year"]/text()').extract()[0]).encode('utf8', 'ignore')
            review_date = review_year+"-"+review_month+"-"+review_day

            review_loader.add_xpath('author', 'div[@class="pr-review-author"]/div[@class="pr-review-author-info-wrapper"]/p[@class="pr-review-author-name"]/span/text()')
            review_loader.add_xpath('title', 'div[@class="pr-review-rating-wrapper"]/div[@class="pr-review-rating"]/p[@class="pr-review-rating-headline"]/text()')
            review_loader.add_xpath('body', '//div[@class="pr-review-wrap"]/div[@class="pr-review-main-wrapper"]/div[@class="pr-review-text"]/p[@class="pr-comments"]/text()')
            review_loader.add_value('date', review_date, MapCompose(Date('%Y-%b-%d')))
            review_loader.add_value('max_stars', '5')
            review_loader.add_xpath('stars', 'div[@class="pr-review-rating-wrapper"]/div[@class="pr-review-rating"]/span/text()')
            loader.add_value('reviews', review_loader.load_item())

        #colors
        for selector in response.xpath('//div[@id="product-description"]/form/div[@class="product-options"]/div[@id="color-options-ul"]/span/a/img'):
            color_loader = ProductColorLoader(response=response, selector=selector)
            color_loader.add_xpath('name', '@title')
            color_loader.add_xpath('swatch_image', '@src')
            loader.add_value('colors', color_loader.load_item())

        yield loader.load_item()





