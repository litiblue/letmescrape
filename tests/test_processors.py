from scrapy.http import HtmlResponse, Request

from letmescrape.processors import *


def test_extract_price():
    test_cases = (
        (' $13 ', 13),
        (' $13.1 ', 13.1),
        (' $13.11 ', 13.11),
        (' 13.11 ', None),
    )

    for text, price in test_cases:
        assert extract_price(text) == price


def test_html2text():
    assert html2text('<html> hello world! </html>').strip() == 'hello world!'


def test_get_absolute_url():
    base_url, relative_url = 'http://www.test.com', 'path/to/resource'
    absolute_url = base_url + '/' + relative_url
    response = HtmlResponse(base_url, request=Request(base_url))

    assert get_absolute_url(relative_url, {'response': response}) == absolute_url