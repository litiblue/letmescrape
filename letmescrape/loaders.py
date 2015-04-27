from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import *

from items import *
from letmescrape.processors import extract_price, html2text


class ProductLoader(ItemLoader):
    default_item_class = ProductItem
    default_output_processor = TakeFirst()

    original_price_in = MapCompose(extract_price)
    sale_price_in = MapCompose(extract_price)
    description_in = MapCompose(html2text)

    images_in = MapCompose(dict)
    colors_in = MapCompose(dict)
    reviews_in = MapCompose(dict)

    description_out = Join(u'\n')
    list_images_out = Identity()
    sizes_out = Identity()
    images_out = Identity()
    colors_out = Identity()
    reviews_out = Identity()


class ProductImageLoader(ItemLoader):
    default_item_class = ProductImageItem
    default_output_processor = TakeFirst()


class ProductColorLoader(ItemLoader):
    default_item_class = ProductColorItem
    default_output_processor = TakeFirst()


class ProductReviewLoader(ItemLoader):
    default_item_class = ProductReviewItem
    default_output_processor = TakeFirst()

    date_in = MapCompose(lambda date: date.strftime("%Y-%m-%d"))
    stars_in = MapCompose(int)
    max_stars_in = MapCompose(int)