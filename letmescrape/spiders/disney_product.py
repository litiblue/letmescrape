# -*- coding: utf-8 -*-
import scrapy


class DisneyProductSpider(scrapy.Spider):
    name = "disney_product"
    allowed_domains = ["disneystore.com"]
    start_urls = (
        'http://www.disneystore.com/',
    )

    def parse(self, response):
        pass
