# -*- coding: utf-8 -*-
import json
import re

from scrapy import Request
from scrapy.contrib.loader.processor import MapCompose

from base import ProductSpider
from letmescrape.loaders import ProductImageLoader, ProductReviewLoader
from letmescrape.processors import Date, JoinExcludingEmptyValues
from letmescrape.utils import get_absolute_url
from letmescrape.scripts import make_lua_script


class DisneyProductSpider(ProductSpider):
    name = "disney_product"
    allowed_domains = ["disneystore.com"]
    start_urls = (
        'http://www.disneystore.com/',
    )
    default_values = {
        'brand': 'disney',
    }

    def get_ajax_url_for_list(self, url, num_items=10000, start=0):
        m = re.search(r'/mn/(\d(\+?\d)*)/', url)
        N = m.group(1)

        ajax_url = "http://www.disneystore.com/disney/store/DSIProcessWidget?storeId=10051&templateId=Width-3_4-ProductList&" \
                   "N=%s&navNum=%s&Nao=%s" % (N, num_items, start)
        return ajax_url

    def start_requests(self):
        for url in self.start_urls:
            ajax_url = self.get_ajax_url_for_list(url)
            yield Request(ajax_url, callback=self.parse_list)

    def check_scrapable(self, item):
        return (item['isCollection'] == 'false'
                and 'Create Your Own' not in item['title']
                and 'Customizable' not in item['title'])

    def extract_values_from_list(self, item, response):
        url = item['link']
        list_images = item.get('imageUrl', None)
        product_number = item.get('productId')

        return {
            'url': url,
            'list_images': list_images,
            'product_number': product_number
        }

    def parse_list(self, response):
        data = json.loads(response.body)
        for item in data['items']:
            if self.check_scrapable(item):
                url = get_absolute_url(response, item['link'])
                values_from_list = self.extract_values_from_list(item, response)

                selector_list = [".BVRRWidget", "iframe#contentFrame"]
                script = make_lua_script(selector_list, '&&')

                request = Request(url, callback=self.parse_item, meta={
                    'splash': {
                        'endpoint': 'execute',
                        'args': {'lua_source': script}
                    }
                })

                request.meta['values_from_list'] = values_from_list
                yield request

    def parse_item(self, response):
        if response.css("iframe#contentFrame"):
            # personalize product
            return

        loader = self.get_product_item_loader_with_default_values(response)

        values_from_list = response.meta.get('values_from_list', {})
        for key, value in values_from_list.iteritems():
            loader.add_value(key, value)

        loader.add_css('title', '#main .pageHeader h1[itemprop=name]::text')
        loader.add_css('description', '#main .productDescription div.productShortDescription')
        loader.add_css('description', '.fullDetails .longDescription')
        loader.add_css('original_price', '#main .productDescription .priceBar .price.regular::text')
        loader.add_css('sale_price', '#main .productDescription .priceBar [itemprop=price]::text')
        loader.add_css('sizes', '#variantSelector .customSelect select option::attr(data-key)')

        #images
        for selector in response.css('#imageViewer .viewerThumbs a.productThumb img'):
            image_loader = ProductImageLoader(response=response, selector=selector)
            image_loader.add_css('thumbnail', '::attr(src)')
            image_loader.add_css('normal_size', '::attr(src)',
                                 MapCompose(lambda url: url.replace('yetiProductThumb', 'yetidetail')))
            image_loader.add_css('zoomed', '::attr(src)',
                                 MapCompose(lambda url: url.replace('yetiProductThumb', 'yetizoom')))
            loader.add_value('images', image_loader.load_item())

        #reviews
        for selector in response.css('.reviewSection #BVRRWidgetID .BVRRContentReview'):
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