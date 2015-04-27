import scrapy

from letmescrape.loaders import ProductLoader


class LMSpider(scrapy.Spider):
    default_values = {}

    def __init__(self, start_url, site_category_id, job_id, *args, **kwargs):
        super(LMSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.site_category_id = site_category_id
        self.job_id = job_id

    def _get_product_item_loader_with_default_values(self, response):
        loader = ProductLoader(response=response)
        loader.add_value('site_category_id', self.site_category_id)
        loader.add_value('job_id', self.job_id)

        for key, value in self.default_values.iteritems():
            loader.add_value(key, value)

        return loader