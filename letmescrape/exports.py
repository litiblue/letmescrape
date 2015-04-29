from urlparse import urljoin

import requests
from scrapy.contrib.exporter import BaseItemExporter
from scrapy.utils.serialize import ScrapyJSONEncoder

from letmescrape.utils import snake_case_to_camel_case


class LetMeShopApiExporter(BaseItemExporter):
    api_end_point = ''
    method = 'POST'

    def __init__(self, api_base_url, auth_token, *args, **kwargs):
        super(LetMeShopApiExporter, self).__init__(*args, **kwargs)
        self.api_base_url = api_base_url
        self.encoder = ScrapyJSONEncoder(**kwargs)
        self.headers = {'Authorization': 'Token %s' % auth_token}

    @property
    def request_url(self):
        return urljoin(self.api_base_url, self.api_end_point)

    def export_item(self, item_or_items):
        if isinstance(item_or_items, (list, tuple)):
            item_list = item_or_items
            serialized = [dict(self._get_serialized_fields(item)) for item in item_list]
        else:
            item = item_or_items
            serialized = dict(self._get_serialized_fields(item))

        serialized = snake_case_to_camel_case(serialized)
        payload = self.encoder.encode(serialized)

        r = requests.request(self.method, self.request_url, data=payload, headers=self.headers)
        r.raise_for_status()

    def start_exporting(self):
        pass

    def finish_exporting(self):
        pass


class LetMeShopApiCategoriesExporter(LetMeShopApiExporter):
    method = 'PUT'

    def __init__(self, site_id, *args, **kwargs):
        super(LetMeShopApiCategoriesExporter, self).__init__(*args, **kwargs)
        self.api_end_point = 'sites/%s/site_categories/' % site_id
        self.top_level_categories = []

    def export_item(self, item):
        self.top_level_categories.append(item)

    def finish_exporting(self):
        super(LetMeShopApiCategoriesExporter, self).export_item(self.top_level_categories)


class LetMeShopApiProductExporter(LetMeShopApiExporter):
    def __init__(self, *args, **kwargs):
        self.api_end_point = 'products/'
        super(LetMeShopApiProductExporter, self).__init__(*args, **kwargs)