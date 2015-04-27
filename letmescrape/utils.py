from urlparse import urljoin

from scrapy.utils.response import get_base_url


def get_absolute_url(response, relative_url):
    base_url = get_base_url(response)
    absolute_url = urljoin(base_url, relative_url)
    return absolute_url