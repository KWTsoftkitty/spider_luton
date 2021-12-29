"""spider testcase"""

from unittest import TestCase
from scrapy.http import HtmlResponse
from spider_luton.spider_luton.spiders.spider import SpiderLuton
from spider_luton.spider_luton.items import SpiderLutonItem
from scrapy import Request


def _read_html():
    html_str = ''
    with open('../test_luton.html', 'r') as f:
        line = f.readline()
        while line:
            html_str = html_str + line
            line = f.readline()
    return html_str


class SpiderTestCase(TestCase):
    """spider test object"""
    expected_urls = ['https://www.luton.com.au/1P47501/403-25-edinburgh-avenue-acton',
                     'https://www.luton.com.au/1P49717/50-44-macquarie-street-barton',
                     'https://www.luton.com.au/1P48367/109-8-veryard-lane-belconnen']

    def test_spider_parse_response(self):
        self.html_str = ''
        self.html_str = _read_html()
        self.html_response = HtmlResponse(url='test_luton', body=self.html_str, encoding='utf8')

        next_page_url = 'http://www.luton.com.au/properties-for-sale?page=2'
        self.expected_urls.append(next_page_url)
        spider_luton = SpiderLuton()
        request_generator = spider_luton.parse(self.html_response)
        self.assertEqual(self.expected_urls, [x.url for x in request_generator])

