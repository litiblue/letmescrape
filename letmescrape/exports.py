from collections import defaultdict

from urlparse import urljoin

import requests
import json
from scrapy.contrib.exporter import BaseItemExporter
from scrapy.utils.serialize import ScrapyJSONEncoder

from letmescrape.utils import snake_case_to_camel_case

class LetMeShopApiExporter(BaseItemExporter):
    api_end_point = ''
    method = 'POST'

    def __init__(self, api_base_url, auth_token, *args, **kwargs):
        super(LetMeShopApiExporter, self).__init__(*args, export_empty_fields=True, **kwargs)
        self.api_base_url = api_base_url
        self.encoder = ScrapyJSONEncoder(**kwargs)
        self.headers = {'Authorization': 'Token %s' % auth_token}

    def _fill_missing_fields(self, item, default_value=None):
        if self.fields_to_export is None:
            missing_keys = frozenset(item.fields.iterkeys()).difference(item.iterkeys())
        else:
            missing_keys = frozenset(self.fields_to_export).difference(item.iterkeys())

        for missing_key in missing_keys:
            item[missing_key] = item.fields[missing_key].get('default_value', default_value)

        return item

    def _get_serialized_fields(self, item, default_value=None, include_empty=None):
        if include_empty is None:
            include_empty = self.export_empty_fields

        if include_empty:
            item = self._fill_missing_fields(item, default_value)

        return super(LetMeShopApiExporter, self)._get_serialized_fields(item, default_value, include_empty)

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
        self.items = {}
        self.tree = defaultdict(list)
        self.root_idx_list = []

    def export_item(self, item):
        self.items[item['idx']] = item
        if 'parent_idx' in item:
            self.tree[item['parent_idx']].append(item['idx'])
        else:
            self.root_idx_list.append(item['idx'])

    def item_from_dfs(self, parent_item_idx):
        item_list = []
        for child_item_idx in self.tree[parent_item_idx]:
            item_list.append(self.item_from_dfs(child_item_idx))
        if item_list:
            self.items[parent_item_idx]['sub_categories'] = item_list
        return self.items[parent_item_idx]

    def clean_items(self):
        for key, value in self.items.iteritems():
            if 'parent_loader' in value:
                del self.items[key]['parent_loader']
            if 'idx' in value:
                del self.items[key]['idx']
            if 'parent_idx' in value:
                del self.items[key]['parent_idx']

    def finish_exporting(self):
        self.clean_items()
        result_list = []
        for root_idx in self.root_idx_list:
            result_list.append(self.item_from_dfs(root_idx))
        super(LetMeShopApiCategoriesExporter, self).export_item(result_list)


class LetMeShopApiProductExporter(LetMeShopApiExporter):
    def __init__(self, site_category_id, job_id, *args, **kwargs):
        self.api_end_point = 'products/'
        self.site_category_id = site_category_id
        self.job_id = job_id
        super(LetMeShopApiProductExporter, self).__init__(*args, **kwargs)

    def start_exporting(self):
        data = {"status": "started"}
        self.scrapy_start_finish_api_call(data)

    def finish_exporting(self):
        data = {"status": "finished"}
        self.scrapy_start_finish_api_call(data)

    def scrapy_start_finish_api_call(self, data):
        method = 'PATCH'
        request_url = 'site_categories/{0}/crawling_job/{1}'.format(self.site_category_id, self.job_id)
        request_url = urljoin(self.api_base_url, request_url)
        r = requests.request(method, request_url, data=json.dumps(data), headers=self.headers)
        r.raise_for_status()
