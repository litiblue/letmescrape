# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.contrib.loader.processor import TakeFirst
from base import ProductSpider

from letmescrape.loaders import ProductImageLoader, ProductColorLoader, ProductReviewLoader

class RalphlaurenProductSpider(ProductSpider):
    name = "ralphlauren_product"
    allowed_domains = ["ralphlauren.com"]
    start_urls = (
        'http://www.ralphlauren.com/',
    )
    default_values = {
        'brand': 'ralphlauren',
        'sub_brand': None,
        'default_color': None
    }

    def start_requests(self):
        for url in self.start_urls:
            request = Request(url, callback=self.parse_page)
            yield request

    def extract_values_from_list(self, item, response):

        brand_link = item.xpath('dl[@class="product-details"]/dt/a[@class="brand-link"]/img/@src').extract()[0]
        create_your_own = '../graphics/category_images/polo_family_brand_240x30_1000012.gif'
        if str(brand_link) == create_your_own:
            return None
        else:
            url_candidate = item.xpath('div[@class="product-photo"]/div[contains(@id,"staticImg")]/a/@href').extract()
            if url_candidate:
                url = 'http://www.ralphlauren.com/'+url_candidate[0]
            else:
                return None

            list_images_candidate = item.xpath('div[@class="product-photo"]/div[contains(@id,"staticImg")]/a[@class="photo"]/img/@src').extract()
            if list_images_candidate:
                list_images = list_images_candidate[0]
            else:
                return None

            return {
                'url': url,
                'list_images': list_images
            }

    def parse_page(self, response):
        total_page = response.xpath('//div[@id="grid-nav-top"]/div[@class="grid-nav-links"]/form[@class="pagination"]/span[@class="total-pages"]/text()').extract()
        if total_page:
            total_page = total_page[0]
            page = 1
            while page < int(total_page)+1:
                url = response.url+'&pg=%s' % page
                request = Request(url, callback=self.parse_list, meta={
                    'splash': {
                        'endpoint': 'render.html',
                        'args': {'wait': '1.0'}
                    }
                })
                page += 1
                yield request

    def parse_list(self, response):
        for item_sel in response.xpath('//ol[contains(@class,"products")]/li[contains(@id,"product")]'):
            values_from_list = self.extract_values_from_list(item_sel, response)

            if values_from_list:
                request = Request(values_from_list['url'], callback=self.parse_item, meta={
                    'splash': {
                        'endpoint': 'render.html',
                        'args': {'wait': '1.0'}
                    }
                })

                request.meta['values_from_list'] = values_from_list

                yield request
            else:
                yield None

    def parse_item(self, response):

        loader = self.get_product_item_loader_with_default_values(response)
        loader.original_price_out = TakeFirst()
        loader.sale_price_out = TakeFirst()
        values_from_list = response.meta.get('values_from_list', {})
        for key, value in values_from_list.iteritems():
            loader.add_value(key, value)

        loader.add_xpath('product_number', '//div[@class="prod-summary"]/div[@class="prod-style"]/span[@class="style-num"]/text()')
        loader.add_xpath('title', '//div[@class="prod-summary"]/div[node()]/h1[@class="prod-title"]/text()')
        loader.add_xpath('description', '//div[@class="prod-top-content"]/div[@class="prod-details"]/div[@class="detail"]/ul')
        loader.add_xpath('sizes', '//div[@class="prod-summary"]/div[contains(@class,"product-actions")]/div[@class="prod-sizes"]/ul[@id="size-swatches"]/li[node()]/@title')
        loader.add_xpath('original_price', '//div[@class="prod-summary"]/div[@class="prod-price"]/span/span[contains(@class,"reg-price")]/span/text()') # http://www.ralphlauren.com/product/index.jsp?productId=56228126
        loader.add_xpath('original_price', '//div[@class="prod-summary"]/div[@class="prod-price"]/span/span[contains(@class,"reg-price")]/text()') # http://www.ralphlauren.com//product/index.jsp?productId=56541926
        loader.add_xpath('original_price', '//table[@id="productDescription"]/tbody/tr/td/div[@class="productStylePrice"]/b/span/span/text()')
        loader.add_xpath('original_price', '//td[@id="productDescription"]/font[@class="prodourprice"]/text()', re='Price: (.*)') # http://www.ralphlauren.com//product/index.jsp?productId=11765920
        loader.add_xpath('sale_price', '//div[@class="prod-summary"]/div[@class="prod-price"]/span/span[@class="sale-price"]/span/text()')
        loader.add_xpath('sale_price', '//td[@id="productDescription"]/font[@class="templateSalePrice"]/span/text()')

        sale_price_candidates = response.xpath('//div[@class="prod-summary"]/div[@class="prod-price"]/span/span[@class="sale-price"]/span/text()').extract()

        if sale_price_candidates:
            sale_price = sale_price_candidates[0]
            loader.add_value('sale_price', sale_price)
        else:
            original_price = loader.get_output_value('original_price')
            loader.add_value('sale_price', '$' + str(original_price))

        #colors
        for selector in response.xpath('//div[@class="prod-colors"]/ul[@id="color-swatches"]/li'):
            color_loader = ProductColorLoader(response=response, selector=selector)
            color_loader.add_xpath('name', '@title')
            color_loader.add_xpath('swatch_image', 'img[not(contains(@class, "crossoff"))]/@src')
            loader.add_value('colors', color_loader.load_item())

        #image
        for selector in response.xpath('//div[@class="prod-img"]'):
            image_loader = ProductImageLoader(response=response, selector=selector)
            image_loader.add_xpath('thumbnail', 'div[@class="img-control"]/div[@id="altImages"]/ul[@class="altImages"]/li[@class="swatch active"]/a/img/@src')
            image_loader.add_xpath('normal_size', 'input[@name="enh_0"]/@value')
            image_loader.add_xpath('zoomed', 'input[@name="enh_0"]/@value')
            loader.add_value('images', image_loader.load_item())

        yield loader.load_item()


























