# -*- coding: utf-8 -*-

import re
import sys

from scrapy.contrib.loader.processor import TakeFirst
from scrapy import Request
from scrapy.contrib.loader.processor import MapCompose

from letmescrape.utils import get_absolute_url
from letmescrape.processors import JoinExcludingEmptyValues
from base import ProductSpider
from letmescrape.loaders import ProductImageLoader, ProductReviewLoader
from letmescrape.processors import Date


reload(sys)
sys.setdefaultencoding('utf-8')

class IherbProductSpider(ProductSpider):
    name = "iherb_product"
    allowed_domains = ["iherb.com"]
    start_urls = (
        'http://www.iherb.com/',
    )
    default_values = {
        'brand': None,
        'sub_brand': None,
        'default_color': None,
        'colors': None
    }

    def get_url_for_list(self, url, page=1):
        list_url = "%s?p=%s" % (url, page)
        return list_url

    def get_url_for_review(self, url, page=1):
        review_url = "%s/?p=%s" % (url, page)
        review_url = review_url.replace(".iherb.com/", ".iherb.com/product-reviews/")
        return review_url

    def get_next_page_url_for_review(self, url):
        m = re.search(r'(.*/\?p=)(\d+)(&.*|$)', url)
        page = int(m.group(2))
        page += 1

        review_url = "%s%s%s" % (m.group(1), page, m.group(3))

        return review_url


    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'iher-pref':'ctd=www&sccode=KR&lan=ko-KR&scurcode=USD&lchg=1&svcode=KR&vlan=ko-KR&vcurcode=USD&ifv=i'}, callback=self.parse_page)

    def extract_values_from_list(self, item, response):
        url = get_absolute_url(response, item.xpath('@href').extract()[0])
        list_images = item.xpath('img/@src').extract()[0]
        list_images = re.sub(r'http://(.*).iherb.com/', r'http://images.iherb.com/', list_images)
        product_number = re.search(r'(?!.*\/)(.*?)$', url).group(1)

        return {
            'url': url,
            'list_images': list_images,
            'product_number': product_number
        }

    def parse_page(self, response):
        total_page = response.xpath('//div[@id="display-results-header"]/p[@class="display-items"]/text()').extract()[0]
        total_page = int(re.search(ur'전체 (\d+) 상품', total_page).group(1))/24 + 1
        page = 1

        while page <= total_page:
            list_url = self.get_url_for_list(response.url, page)
            request = Request(list_url, callback=self.parse_list)
            page += 1
            yield request

    def parse_list(self, response):

        for item_sel in response.xpath('//div[@id="display-results-content"]/div[@class="prodSlotWide"]/div[@class="imgContainer"]/a'):
            values_from_list = self.extract_values_from_list(item_sel, response)

            # request = Request(values_from_list['url'], callback=self.parse_item)
            request = Request(self.get_url_for_review(values_from_list['url'], 1), callback=self.parse_review)

            request.meta['values_from_list'] = values_from_list
            request.meta['reviews'] = []
            yield request

    def parse_item(self, response):
        if response.xpath('//div[@id="mainContent"]/section[@id="product-summary"]/div[@id="product-action"]/section[@id="product-price"]/div[contains(@class, "s20")]'):
            # See Price in Cart!
            return

        loader = self.get_product_item_loader_with_default_values(response)
        loader.description_out = JoinExcludingEmptyValues('\n')
        loader.sale_price_out = TakeFirst()

        values_from_list = response.meta.get('values_from_list', {})
        reviews = response.meta.get('reviews', [])
        for key, value in values_from_list.iteritems():
            loader.add_value(key, value)

        loader.add_value('reviews', reviews)

        loader.add_xpath('brand', '//div[@id="mainContent"]/section[@id="product-summary"]/div[@id="product-specification"]/h2/a/text()')
        loader.add_xpath('title', '//div[@id="mainContent"]/section[@id="product-summary"]/div[@id="product-specification"]/h1/text()')
        loader.add_xpath('description', '//div[@id="mainContent"]/section[@id="product-summary"]/div[@id="product-specification"]/p[contains(@class, "red")]')
        loader.add_xpath('description', '//div[@class="prodOverview-section"]')
        loader.add_xpath('original_price', '//div[@id="mainContent"]/section[@id="product-summary"]/div[@id="product-action"]/section[@id="product-msrp"]/div[2]/text()')
        loader.add_xpath('sale_price', '//div[@id="mainContent"]/section[@id="product-summary"]/div[@id="product-action"]/section[@id="super-special-price"]/div[2]/b/text()')
        loader.add_xpath('sale_price', '//div[@id="mainContent"]/section[@id="product-summary"]/div[@id="product-action"]/section[@id="product-price"]/div[2]/text()')
        loader.add_xpath('sizes', '//div[@id="mainContent"]/section[@id="product-summary"]/div[@id="product-specification"]/ul[@id="product-specs-list"]/li[4]/text()', re=ur'포장 수량: (.*)')
        loader.add_xpath('sizes', '//div[@id="mainContent"]/section[@id="product-summary"]/div[@id="product-specification"]/ul[@id="product-specs-list"]/li[5]/text()', re=ur'포장 수량: (.*)')

        #images
        if response.xpath('//div[@id="mainContent"]/section[@id="product-summary"]//div[@id="product-image"]/div[@class="smImHolder"]/div[@class="prod-im-sm-front"]'):
            for selector in response.xpath('//div[@id="mainContent"]/section[@id="product-summary"]//div[@id="product-image"]/div[@class="smImHolder"]/div[@class="prod-im-sm-front"]'):
                image_loader = ProductImageLoader(response=response, selector=selector)
                image_loader.add_xpath('thumbnail', 'a/img/@src')
                image_loader.add_xpath('normal_size', 'a/@href')
                image_loader.add_xpath('zoomed', 'a/@href')
                loader.add_value('images', image_loader.load_item())
        else:
            for selector in response.xpath('//div[@id="mainContent"]/section[@id="product-summary"]//div[@id="product-image"]/div[contains(@class, "prod-im-big")]'):
                image_loader = ProductImageLoader(response=response, selector=selector)
                image_loader.add_xpath('thumbnail', 'a/@href', MapCompose(lambda url: url.replace('/l/', '/b/')))
                image_loader.add_xpath('normal_size', 'a/@href')
                image_loader.add_xpath('zoomed', 'a/@href')
                loader.add_value('images', image_loader.load_item())

        yield loader.load_item()

    def parse_review(self, response):
        values_from_list = response.meta.get('values_from_list', {})
        reviews = response.meta.get('reviews', [])

        #reviews
        for selector in response.xpath('//div[@class="review-row"]'):
            review_loader = ProductReviewLoader(response=response, selector=selector)
            review_loader.body_out = JoinExcludingEmptyValues('\n')
            review_loader.add_xpath('author', 'div[contains(@class, "starRatingsContainer")]/p/a/text()')
            review_loader.add_xpath('title', 'div[@class="textcontainerTop"]/p/text()')
            review_loader.add_xpath('date', 'div[contains(@class, "starRatingsContainer")]/p/text()[2]',
                                  MapCompose(Date('님께서 %b %d, %Y 에 작성하셨습니다.\r\n        ')))
            review_loader.add_xpath('body', 'div[@class="textcontainer"]/p/text()')
            review_loader.add_xpath('max_stars', '../../../div[@class="prodOverview-wrapper"][1]/div/div/div[@class="ratingsChart"]/div[@class="row"][1]/div/div/text()', re=ur'(.*) 별점')
            review_loader.add_xpath('stars', 'div[contains(@class, "starRatingsContainer")]/img/@src', re=r'stars/(.*)0.png')

            reviews.append(review_loader.load_item())

        if response.xpath('//div[@class="prodOverview-section"]/p'):
            request = Request(values_from_list['url'], callback=self.parse_item)
        else:
            request = Request(self.get_next_page_url_for_review(response.url), callback=self.parse_review)

        request.meta['values_from_list'] = values_from_list
        request.meta['reviews'] = reviews

        yield request
