# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from letmescrape.fields import SingleItemField, CharField, NumberField, UrlField, DateField, ArrayField


class ProductItem(scrapy.Item):
    site_category_id = SingleItemField(required=True)
    job_id = SingleItemField(required=True)
    url = UrlField(required=True)
    product_number = CharField(required=True)
    title = CharField(required=True)
    brand = CharField(required=True)
    sub_brand = CharField()
    description = CharField(required=True)
    list_images = ArrayField(UrlField)
    original_price = NumberField()
    sale_price = NumberField(required=True)
    sizes = ArrayField(CharField)
    default_color = CharField()

    images = ArrayField(scrapy.Item, required=True)
    colors = ArrayField(scrapy.Item)
    reviews = ArrayField(scrapy.Item)


class ProductImageItem(scrapy.Item):
    thumbnail = UrlField()
    normal_size = UrlField(required=True)
    zoomed = UrlField()


class ProductColorItem(scrapy.Item):
    name = CharField(required=True)
    swatch_image = UrlField()


class ProductReviewItem(scrapy.Item):
    author = CharField()
    title = CharField()
    date = DateField()
    body = CharField(required=True)
    url = UrlField()
    stars = NumberField()
    max_stars = NumberField()


class CategoryItem(scrapy.Item):
    title = CharField(required=True)
    link = UrlField()
    sub_categories = ArrayField(scrapy.Item)