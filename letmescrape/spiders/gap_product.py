# -*- coding: utf-8 -*-

import json
import re

from scrapy.contrib.loader.processor import TakeFirst
from scrapy import Request
from scrapy.contrib.loader.processor import MapCompose

from letmescrape.processors import JoinExcludingEmptyValues
from base import ProductSpider
from letmescrape.loaders import ProductImageLoader, ProductColorLoader, ProductReviewLoader
from letmescrape.processors import Date
from letmescrape.utils import get_absolute_url


class CartersProductSpider(ProductSpider):
    name = "gap_product"
    allowed_domains = ["gap.com"]
    start_urls = (
        'http://www.gap.com/',
    )
    default_values = {
        'brand': 'gap',
        'sub_brand': None,
        'default_color': None,
        'colors': None
    }

    def get_ajax_url_for_list(self, url):
        cid = re.search(r'cid=(\d*)', url).group(1)
        ajax_url = "http://www.gap.com/resources/productSearch/v1/search?cid=%s" % cid
        return ajax_url

    def start_requests(self):
        for url in self.start_urls:
            ajax_url = self.get_ajax_url_for_list(url)
            request = Request(ajax_url, callback=self.parse_ajax)
            request.meta['url'] = url
            yield request

    def parse_ajax(self, response):
        data = json.loads(response.body)
        total_page = int(data['productCategoryFacetedSearch']['productCategory']['productCategoryPaginator']['pageNumberTotal'])
        page = 0
        while page < total_page:
            list_url = self.get_url_for_list(response.meta.get('url'), page)
            yield Request(list_url, callback=self.parse_list, meta={
                'splash': {
                    'endpoint': 'render.html',
                    'args': {'wait': '1.0'}
                }
            })
            page += 1

    def get_url_for_list(self, url, page=0):
        list_url = "%s#pageId=%s" % (url, page)
        return list_url

    def extract_values_from_list(self, item, response):
        url = get_absolute_url(response, item.xpath('a/@href').extract()[0])
        list_images = item.xpath('a/img/@productimagepath').extract()[0]

        return {
            'url': url,
            'list_images': list_images
        }

    def get_url_for_data(self, url):
        vid = re.search('\??vid=(.*?)(&|$)', url).group(1)
        pid = re.search('\??pid=(.*?)(&|$)', url).group(1)
        data_url = "http://www.gap.com/browse/productData.do?pid=%s&vid=%s" % (pid[0:6], vid)
        return data_url

    def parse_list(self, response):
        for item_sel in response.xpath('//div[contains(@class,"productPlaceholder")]'):
            values_from_list = self.extract_values_from_list(item_sel, response)
            url = self.get_url_for_data(values_from_list['url'])

            request = Request(url, callback=self.parse_data)
            request.meta['values_from_list'] = values_from_list
            yield request

    def parse_data(self, response):
        values_from_list = response.meta.get('values_from_list', {})
        pid = re.search('\??pid=(.*?)(&|$)', values_from_list['url']).group(1)
        pattern = "StyleColor\(\"%s\".*?\.styleColorImagesMap = (.*?);" % pid
        images_data = json.loads(re.search(pattern, response.body).group(1).replace("'", "\""))

        request = Request(values_from_list['url'], callback=self.parse_item, meta={
            'splash': {
                'endpoint': 'render.html',
                'args': {'wait': '1.0'}
            }
        })

        request.meta['values_from_list'] = values_from_list
        request.meta['images_data'] = images_data
        yield request

    def parse_item(self, response):
        loader = self.get_product_item_loader_with_default_values(response)
        loader.original_price_out = TakeFirst()
        loader.sale_price_out = TakeFirst()

        values_from_list = response.meta.get('values_from_list', {})
        for key, value in values_from_list.iteritems():
            loader.add_value(key, value)

        loader.add_xpath('product_number', '//div[@id="swatchContent"]/div[@id="productNumber"]/text()', re='#(.*)')
        loader.add_xpath('title', '//div[@id="productNameText"]/span[@class="productName"]/text()')
        loader.add_xpath('description', '//div[@id="tabWindow"]//text()')
        loader.add_xpath('original_price', '//div[@id="selectionContent"]/span[@id="priceText"]/strike/text()')
        loader.add_xpath('original_price', '//div[@id="selectionContent"]/span[@id="priceText"]/text()')
        loader.add_xpath('sale_price', '//div[@id="selectionContent"]/span[@id="priceText"]/span[@class="salePrice"]/text()')
        loader.add_xpath('sale_price', '//div[@id="selectionContent"]/span[@id="priceText"]/text()')
        loader.add_xpath('sizes', '//div[@id="productContentRight"]/div[@id="swatchContent"]/div[@id="sizeDimensionSwatchContent"]/div[@id="sizeDimension1SwatchContent"]/div[@id="sizeDimension1Swatches"]/button/text()')
        loader.add_xpath('default_color', '//div[@id="selectionContent"]/span[@id="selectionConfirmText"]/text()')

        #colors
        for selector in response.xpath('//div[@id="swatchContent"]/div[@id="colorSwatchContent"]/input'):
            color_loader = ProductColorLoader(response=response, selector=selector)
            color_loader.add_xpath('name', '@alt', re='(.*) product image$')
            color_loader.add_xpath('swatch_image', '@src')
            loader.add_value('colors', color_loader.load_item())

        #images
        images_data = response.meta.get('images_data', {})
        if images_data.get('P01'):
            image_loader = ProductImageLoader(response=response)
            image_loader.add_value('thumbnail', images_data.get('T'))
            image_loader.add_value('normal_size', images_data.get('P01'))
            image_loader.add_value('zoomed', images_data.get('Z'))
            loader.add_value('images', image_loader.load_item())
        num = 1
        while num < 9:
            av_num = 'AV%s' % num
            if images_data.get(av_num):
                image_loader = ProductImageLoader(response=response)
                image_loader.add_value('thumbnail', images_data.get('%s_T' % av_num))
                image_loader.add_value('normal_size', images_data.get(av_num))
                image_loader.add_value('zoomed', images_data.get('%s_Z' % av_num))
                loader.add_value('images', image_loader.load_item())
            num += 1

        #reviews
        for selector in response.xpath('//div[@id="BVRRContainer"]//ol[contains(@class,"bv-content-list")]/li[contains(@class,"bv-content-item")]'):
            review_loader = ProductReviewLoader(response=response, selector=selector)
            review_loader.body_out = JoinExcludingEmptyValues('\n')
            review_loader.add_xpath('author', 'div[@class="bv-author-profile"]/div[@class="bv-inline-profile"]/div[@class="bv-author-avatar"]/div[@class="bv-author-avatar-nickname"]/div[@class="bv-content-author-name"]/button/h3/text()')
            review_loader.add_xpath('title', 'div/div[@class="bv-content-container"]//h4[@class="bv-content-title"]/text()')
            review_loader.add_xpath('date', 'div/div[@class="bv-content-container"]//div[@class="bv-content-datetime"]/meta[@itemprop="dateCreated"]/@content',
                                  MapCompose(Date('%Y-%m-%d')))
            review_loader.add_xpath('body', 'div/div[@class="bv-content-container"]//div[@class="bv-content-summary-body-text"]/p/text()')
            review_loader.add_xpath('max_stars', 'div/div[@class="bv-content-container"]//span[contains(@class,"bv-content-rating")]/meta[@itemprop="bestRating"]/@content')
            review_loader.add_xpath('stars', 'div/div[@class="bv-content-container"]//span[contains(@class,"bv-content-rating")]/meta[@itemprop="ratingValue"]/@content')
            loader.add_value('reviews', review_loader.load_item())

        yield loader.load_item()
