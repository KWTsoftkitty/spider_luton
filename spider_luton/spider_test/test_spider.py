"""spider testcase"""
from unittest import TestCase

from scrapy.http import TextResponse

from spider_luton.spider_luton.spiders.spider import SpiderLuton


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

    def test_spider_parse_response(self):
        expected_urls = ['https://www.luton.com.au/1P47501/403-25-edinburgh-avenue-acton',
                         'https://www.luton.com.au/1P49717/50-44-macquarie-street-barton',
                         'https://www.luton.com.au/1P48367/109-8-veryard-lane-belconnen',
                         'https://test_luton?page=2']
        list_page_html_str = _read_html('../test_luton.html')
        list_page_html_response = TextResponse(url='https://test_luton', body=list_page_html_str, encoding='utf8')
        spider_luton = SpiderLuton()
        list_page_generator = spider_luton.parse(list_page_html_response)
        self.assertEqual(expected_urls, [x.url for x in list_page_generator])

    def test_spider_parse_detail_page_response(self):
        xpath_str_for_testcase = {'street_info': '//*[@id="contentContainer"]/article/div[1]/h1/span/text()',
                                  'suburb_name': '//*[@id="contentContainer"]/article/div[1]/h1/small/span[1]/text()',
                                  'state_name': '//*[@id="contentContainer"]/article/div[1]/h1/small/span[3]/text()',
                                  'postal_code': '//*[@id="contentContainer"]/article/div[1]/h1/small/span[2]/text()',
                                  'listing_type': '//*[@id="contentContainer"]/article/div[1]/div/div/text()',
                                  'agent_count': 'count(//*[@id="contact"]/ul/li)',
                                  'agent_name': '//*[@id="contact"]/ul/li[{}]/div/div/div/span/text()',
                                  'agent_email': '//*[@id="contact"]/ul/li[{}]/div/div/dl/dd[1]/a/text()'}

        detail_page_html_str = _read_html('../test_luton_detail_page.html')
        detail_page_html_response = TextResponse(url='https://test_detail_luton', body=detail_page_html_str,
                                                 encoding='utf8')

        spider_luton = SpiderLuton()
        spider_luton.xpath_str_for_item = xpath_str_for_testcase
        detail_request_generator = spider_luton.parse_detail_page(detail_page_html_response)

        expected_item = {'agent': [{'email': 'sophie.luton@luton.com.au', 'name': 'Sophie Luton'},
                                   {'email': 'richard.luton@luton.com.au', 'name': 'Richard Luton'}],
                         'full_address': '403/25 Edinburgh Avenue, Acton, ACT 2601',
                         'listing_type': 'sale',
                         'url': 'https://test_detail_luton'}

        self.assertEqual(expected_item, detail_request_generator.__next__())
