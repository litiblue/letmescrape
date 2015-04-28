import re

import html2text as __html2text


def extract_price(text):
    result = re.search(r'\$(\d+(\.\d(\d)?)?)', text)
    if result:
        value = result.group(1)
        return float(value)


def html2text(html):
    h = __html2text.HTML2Text()
    h.ignore_links = True
    if html:
        return h.handle(html)
    else:
        return ""