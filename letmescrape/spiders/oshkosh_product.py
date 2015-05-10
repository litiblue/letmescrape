# -*- coding: utf-8 -*-
from carters_product import CartersProductSpider
from letmescrape.utils import get_absolute_url


class OshkoshProductSpider(CartersProductSpider):
    name = "oshkosh_product"
    allowed_domains = ["oshkosh.com"]
    start_urls = (
        'http://www.oshkosh.com/',
    )
    list_url_base = "http://www.oshkosh.com/%s?cgid=%s&sz=all&format=ajax"
    default_values = {
        'brand': 'oshkosh',
        'sub_brand': None,
        'default_color': None,
        'colors': None
    }

    def extract_values_from_list(self, item, response):
        url = item.css('div.product-tile > div.product-image > a.thumb-link::attr(href)').extract()[0]
        url = get_absolute_url(response, url)
        list_images = item.css('div.product-tile > div.product-image > a.thumb-link  > img::attr(src)').extract()[0]
        product_number = item.css('div.product-tile > div.product-image > a.thumb-link::attr(href)').re(r'(?!.*\/)(.*?).html')[0]

        return {
            'url': url,
            'list_images': list_images,
            'product_number': product_number
        }