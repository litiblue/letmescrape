import scrapy
from scrapy.contrib.loader.processor import MapCompose, Identity

from letmescrape.processors import SingleValue, get_absolute_url


class PredefinedField(scrapy.Field):
    def __init__(self, defaults=None, **kwargs):
        defaults = defaults or self.defaults.copy()
        defaults.update(kwargs)
        super(PredefinedField, self).__init__(**defaults)

        
class SingleItemField(PredefinedField):
    defaults = {
        'output_processor': SingleValue()
    }


class CharField(PredefinedField):
    defaults = {
        'input_processor': MapCompose(lambda chars: chars.strip()),
        'output_processor': SingleValue(),
        'default_value': ''
    }


class NumberField(PredefinedField):
    defaults = {
        'input_processor': MapCompose(float),
        'output_processor': SingleValue()
    }


class DateField(PredefinedField):
    defaults = {
        'input_processor': MapCompose(lambda date: date.strftime("%Y-%m-%d")),
        'output_processor': SingleValue()
    }


class UrlField(PredefinedField):
    defaults = {
        'input_processor': MapCompose(get_absolute_url),
        'output_processor': SingleValue()
    }


class ArrayField(PredefinedField):
    defaults = {
        'output_processor': Identity(),
        'default_value': []
    }

    def __init__(self, field_or_item, **kwargs):
        if issubclass(field_or_item, scrapy.Item):
            defaults = {
                'input_processor': MapCompose(dict)
            }
        elif issubclass(field_or_item, PredefinedField):
            defaults = field_or_item.defaults.copy()
        else:
            defaults = {}

        defaults.update(self.defaults)
        super(ArrayField, self).__init__(defaults, **kwargs)