from letmescrape.utils import *
from scrapy.http import HtmlResponse, Request


def test_get_absolute_url():
    test_cases = (
        ('http://www.test.com', 'path/to/resource'),
        ('http://www.test.com/', 'path/to/resource'),
        ('http://www.test.com', '/path/to/resource'),
        ('http://www.test.com/', '/path/to/resource'),
    )

    for base_url, relative_url in test_cases:
        response = HtmlResponse(base_url, request=Request(base_url))
        absolute_url = get_absolute_url(response, relative_url)

        assert absolute_url == 'http://www.test.com/path/to/resource'