from urlparse import urljoin

from scrapy.utils.response import get_base_url


def get_absolute_url(response, relative_url):
    if '_splash_processed' in response.meta:
        url = response.meta['_splash_processed']['args']['url']
        response = response.replace(url=url)
    base_url = get_base_url(response)
    absolute_url = urljoin(base_url, relative_url)
    return absolute_url


def _snake_case_key_to_camel_case_key(snake_case_key):
    split = snake_case_key.split('_')
    camel_case_key = split[0] + "".join([word.capitalize() for word in split[1:]])
    return camel_case_key


def snake_case_to_camel_case(snake_case):
    if isinstance(snake_case, dict):
        snake_case_dict = snake_case
        camel_case_dict = {_snake_case_key_to_camel_case_key(key): snake_case_to_camel_case(value)
                           for key, value in snake_case_dict.iteritems()}
        return camel_case_dict
    elif isinstance(snake_case, (list, tuple)):
        snake_case_list = snake_case
        camel_case_list = [snake_case_to_camel_case(elem) for elem in snake_case_list]
        return camel_case_list
    else:
        return snake_case