from letmescrape.spiders.base import ProductSpider


def test_get_product_item_loader_with_default_values():
    start_url = 'http://test.com'
    site_category_id = 1
    job_id = 2
    test_key = 'title'
    test_value = 'value'

    spider = ProductSpider(name='default', start_url=start_url, site_category_id=site_category_id, job_id=job_id)
    spider.default_values = {
        test_key: test_value
    }
    loader = spider.get_product_item_loader_with_default_values(None)

    assert loader.get_output_value('site_category_id') == site_category_id
    assert loader.get_output_value('job_id') == job_id
    assert loader.get_output_value(test_key) == test_value