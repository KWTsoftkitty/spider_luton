"""spider testcase"""

from unittest import TestCase
from scrapy.http import HtmlResponse
from spider_luton.spider_luton.spiders.spider import SpiderLuton
from spider_luton.spider_luton.items import SpiderLutonItem
from scrapy import Request


def _read_html(filename):
    html_str = ''
    with open(filename, 'r') as f:
        line = f.readline()
        while line:
            html_str = html_str + line
            line = f.readline()
    return html_str


class SpiderTestCase(TestCase):
    """spider test object"""

    def setUp(self):
        self.spider_luton = SpiderLuton()
        self.expected_urls = ['https://www.luton.com.au/1P47501/403-25-edinburgh-avenue-acton',
                              'https://www.luton.com.au/1P49717/50-44-macquarie-street-barton',
                              'https://www.luton.com.au/1P48367/109-8-veryard-lane-belconnen']
        self.html_str = ''
        self.html_str = _read_html('../test_luton.html')
        self.html_response = HtmlResponse(url='test_luton', body=self.html_str, encoding='utf8')

        self.detail_page_html_str = ''
        self.detail_page_html_str = _read_html('../test_luton_detail_page.html')
        self.detail_page_html_response = HtmlResponse(url='test_detail_luton', body=self.detail_page_html_str,
                                                      encoding='utf8')

    def test_spider_parse_response(self):
        next_page_url = 'http://www.luton.com.au/properties-for-sale?page=2'
        self.expected_urls.append(next_page_url)
        request_generator = self.spider_luton.parse(self.html_response)
        self.assertEqual(self.expected_urls, [x.url for x in request_generator])

    def test__spider_parse_detail_initialize_item(self):
        item = SpiderLutonItem()

        expected_item = [{'url': 'https://www.luton.com.au/1P47501/403-25-edinburgh-avenue-acton',
                          'full_address': '403/25 Edinburgh Avenue, Acton, ACT 2601', 'listing_type': 'sale',
                          'agent': [{'name': 'Sophie Luton', 'email': 'sophie.luton@luton.com.au'},
                                    {'name': 'Richard Luton', 'email': 'richard.luton@luton.com.au'}]}]

        xpath_strings = {'street_info': '//*[@id="contentContainer"]/article/div[1]/h1/span/text()',
                         'suburb_name': '//*[@id="contentContainer"]/article/div[1]/h1/small/span[1]/text()',
                         'state_name': '//*[@id="contentContainer"]/article/div[1]/h1/small/span[3]/text()',
                         'postal_code': '//*[@id="contentContainer"]/article/div[1]/h1/small/span[2]/text()',
                         'listing_type': '//*[@id="contentContainer"]/article/div[1]/div/div/text()',
                         'agent_count': 'count(//*[@id="contact"]/ul/li)',
                         'agent_name': '//*[@id="contact"]/ul/li[{}]/div/div/div/span/text()',
                         'agent_email': '//*[@id="contact"]/ul/li[{}]/div/div/dl/dd[1]/a/text()'}

        # self.assertEqual(expected_item[0],
        #                  self.spider_luton._initialize_item(self.detail_page_html_response, xpath_strings, item))
        item['url'] = 'https://www.luton.com.au/1P47501/403-25-edinburgh-avenue-acton'
        self.assertEqual(expected_item[0]['url'], self.spider_luton._initialize_item(self.detail_page_html_response, xpath_strings, item)['url'])
        self.assertEqual(expected_item[0]['full_address'], self.spider_luton._initialize_item(self.detail_page_html_response, xpath_strings, item)['full_address'])
        self.assertEqual(expected_item[0]['listing_type'], self.spider_luton._initialize_item(self.detail_page_html_response, xpath_strings, item)['listing_type'])
        self.assertEqual(expected_item[0]['agent'], self.spider_luton._initialize_item(self.detail_page_html_response, xpath_strings, item)['agent'])
        self.assertEqual(expected_item[0]['agent'], self.spider_luton._initialize_item(self.detail_page_html_response, xpath_strings, item)['agent'])

