import os
from functools import partial

from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.utils.project import get_project_settings
from scrapy import Spider, Request, signals


def _get_default_crawler():
    settings = get_project_settings()
    return Crawler(settings)


def _get_default_spider():
    return Spider('default')


def _get_request(url, js=False):
    meta = {}
    if js:
        meta['splash'] = {
            'endpoint': 'render.html',
            'args': {'wait': '1.0'}
        }

    return Request(url, dont_filter=True, meta=meta)


def _write_response(file_name, response):
    if not file_name[0] == '/':
        responses_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(responses_dir, file_name)
    else:
        file_path = file_name

    with open(file_path, 'w') as f:
        f.write(response.body)


def download(url, file_name, js):
    request = _get_request(url, js)
    spider = _get_default_spider()
    crawler = _get_default_crawler()

    request.callback = partial(_write_response, file_name)

    crawler.signals.connect(reactor.stop, signal=signals.response_received)
    crawler.configure()
    crawler.crawl(spider, requests=[request])
    crawler.start()
    reactor.run()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("file_name")
    parser.add_argument("--js", help="use splashjs", action="store_true")

    args = parser.parse_args()
    download(args.url, args.file_name, args.js)