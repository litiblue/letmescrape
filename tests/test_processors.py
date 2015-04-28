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