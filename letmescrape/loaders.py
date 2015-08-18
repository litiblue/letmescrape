from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import MapCompose

from items import *
from letmescrape.processors import extract_price, html2text, JoinExcludingEmptyValues
from scrapy.exceptions import DropItem


class BaseItemLoader(ItemLoader):
    def load_item(self):
        item = super(BaseItemLoader, self).load_item()
        for field_name, options in item.fields.items():
            if options.get('required', False) and field_name not in item:
                raise DropItem("%s is required.", field_name)
        return item

class ProductLoader(BaseItemLoader):
    default_item_class = ProductItem

    original_price_in = MapCompose(extract_price)
    sale_price_in = MapCompose(extract_price)
    description_in = MapCompose(html2text)

    description_out = JoinExcludingEmptyValues(u'\n')


class ProductImageLoader(BaseItemLoader):
    default_item_class = ProductImageItem


class ProductColorLoader(BaseItemLoader):
    default_item_class = ProductColorItem


class ProductReviewLoader(BaseItemLoader):
    default_item_class = ProductReviewItem


class CategoryLoader(BaseItemLoader):
    default_item_class = CategoryItem

    def load_item(self):
        item = super(CategoryLoader, self).load_item()
        if 'parent_loader' in item:
            parent_loader = item['parent_loader'][0]
            item['parent_idx'] = parent_loader.load_item()['idx']
            item['idx'] = '%s|^|%s' % (item['parent_idx'], item['title'])
        else:
            item['idx'] = item['title']
        return item
