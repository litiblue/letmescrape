# -*- coding: utf-8 -*-
from carters_category import CartersCategorySpider


class OshkoshCategorySpider(CartersCategorySpider):
    name = "oshkosh_category"
    allowed_domains = ["oshkosh.com"]
    start_urls = (
        'http://www.oshkosh.com/',
    )