import os

from scrapy.http import HtmlResponse, Request


def fake_response_from_file(file_name, url=None, meta=None):
    # http://stackoverflow.com/questions/6456304/scrapy-unit-testing

    url = url or "http://www.test.com"
    meta = meta or {}

    request = Request(url=url, dont_filter=True, meta=meta)
    if not file_name[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name

    file_content = open(file_path, 'r').read()

    response = HtmlResponse(url=url, request=request, body=file_content)
    return response