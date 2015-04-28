import scrapy

from letmescrape.loaders import ProductLoader


class ProductSpider(scrapy.Spider):
    default_values = {}

    def __init__(self, *args, **kwargs):
        super(ProductSpider, self).__init__(*args, **kwargs)

        start_url = kwargs.get('start_url', False)
        if start_url:
            self.start_urls = [start_url]

        self.site_category_id = kwargs.get('site_category_id', None)
        self.job_id = kwargs.get('job_id', None)

    def get_product_item_loader_with_default_values(self, response):
        loader = ProductLoader(response=response)
        loader.add_value('site_category_id', self.site_category_id)
        loader.add_value('job_id', self.job_id)

        for key, value in self.default_values.iteritems():
            loader.add_value(key, value)

        return loader


class CategorySpider(scrapy.Spider):
    pass