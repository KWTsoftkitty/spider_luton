"""spider testcase"""

from unittest import TestCase
from scrapy.http import HtmlResponse
from spider_luton.spider_luton.spiders.spider import SpiderLuton


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

    def setUp(self):
        self.html_str = ''
        self.html_str = _read_html()
        self.html_response = HtmlResponse(url='test_luton', body=self.html_str, encoding='utf8')

    def test_spider_parse_response_urls(self):
        expected_urls = ['https://www.luton.com.au/1P47501/403-25-edinburgh-avenue-acton',
                         'https://www.luton.com.au/1P49717/50-44-macquarie-street-barton',
                         'https://www.luton.com.au/1P48367/109-8-veryard-lane-belconnen',
                         'https://www.luton.com.au/1P49595/52-41-chandler-street-belconnen',
                         'https://www.luton.com.au/1P49597/714-6-grazier-lane-belconnen',
                         'https://www.luton.com.au/1P47275/7-anna-morgan-circuit-bonner',
                         'https://www.luton.com.au/1P24465/28-20-helpman-street-bonython',
                         'https://www.luton.com.au/1P49562/8-70-hurtle-avenue-bonython',
                         'https://www.luton.com.au/1P49620/84-21-battye-street-bruce',
                         'https://www.luton.com.au/1P49846/lot-21-elm-grove-tarago-road-bungendore']

        spider_luton = SpiderLuton()
        # urls = self.html_response.xpath('//*[@id="contentContainer"]/article/div/div/ul/li/div/a/@href').extract()
        urls = spider_luton.parse(self.html_response)
        self.assertEqual(expected_urls, urls)
