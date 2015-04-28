from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose

from items import *
from letmescrape.processors import extract_price, html2text, JoinExcludingEmptyValues


class ProductLoader(ItemLoader):
    default_item_class = ProductItem

    original_price_in = MapCompose(extract_price)
    sale_price_in = MapCompose(extract_price)
    description_in = MapCompose(html2text)

    description_out = JoinExcludingEmptyValues(u'\n')


class ProductImageLoader(ItemLoader):
    default_item_class = ProductImageItem


class ProductColorLoader(ItemLoader):
    default_item_class = ProductColorItem


class ProductReviewLoader(ItemLoader):
    default_item_class = ProductReviewItem


class CategoryLoader(ItemLoader):
    default_item_class = CategoryItem