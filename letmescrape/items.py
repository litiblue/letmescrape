# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    site_category_id = scrapy.Field(required=True)
    job_id = scrapy.Field(required=True)
    url = scrapy.Field(required=True)
    product_number = scrapy.Field(required=True)
    title = scrapy.Field(required=True)
    brand = scrapy.Field(required=True)
    sub_brand = scrapy.Field()
    description = scrapy.Field()
    list_images = scrapy.Field()
    original_price = scrapy.Field()
    sale_price = scrapy.Field(required=True)
    sizes = scrapy.Field()
    default_color = scrapy.Field()

    images = scrapy.Field(required=True)
    colors = scrapy.Field()
    reviews = scrapy.Field()


class ProductImageItem(scrapy.Item):
    thumbnail = scrapy.Field()
    normal_size = scrapy.Field(required=True)
    zoomed = scrapy.Field()


class ProductColorItem(scrapy.Item):
    name = scrapy.Field(required=True)
    swatch_image = scrapy.Field()


class ProductReviewItem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    body = scrapy.Field(required=True)
    url = scrapy.Field()
    stars = scrapy.Field()
    max_stars = scrapy.Field()


class CategoryItem(scrapy.Item):
    title = scrapy.Field(required=True)
    link = scrapy.Field()
    sub_categories = scrapy.Field()