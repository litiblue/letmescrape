import re
from datetime import datetime

import html2text as __html2text
from scrapy.contrib.loader.processor import Join

from letmescrape.utils import get_absolute_url as __get_absolute_url


def _filter_empty_values(values):
    values = [value for value in values if value is not None and value != '']
    return values


def extract_price(text):
    result = re.search(r'\$(\d+(\.\d(\d)?)?)', text)
    if result:
        value = result.group(1)
        return float(value)


def html2text(html):
    h = __html2text.HTML2Text()
    h.ignore_links = True
    if html:
        return h.handle(html)
    else:
        return ""


def get_absolute_url(relative_url, loader_context):
    response = loader_context.get('response')
    return __get_absolute_url(response, relative_url)


class SingleValue(object):
    def __call__(self, values):
        values = _filter_empty_values(values)

        if len(values) > 1:
            raise ValueError('Only one value is allowed.')
        elif len(values) == 1:
            return values[0]


class Date(object):
    def __init__(self, date_format):
        self.format = date_format

    def __call__(self, value):
        return datetime.strptime(value, self.format).date()


class JoinExcludingEmptyValues(Join):
    def __call__(self, values):
        values = _filter_empty_values(values)
        return super(JoinExcludingEmptyValues, self).__call__(values)