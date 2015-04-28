# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem


class RequiredFieldsPipeline(object):
    def process_item(self, item, spider=None):
        for field_name, options in item.fields.items():
            if options.get('required', False) and field_name not in item:
                raise DropItem("%s is required.", field_name)
        else:
            return item