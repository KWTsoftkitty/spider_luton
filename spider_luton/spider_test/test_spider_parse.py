"""spider testcase"""

from unittest import TestCase
from scrapy.http import TextResponse
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
        self.html_response = TextResponse(url='test_luton', body=self.html_str, encoding='utf8')

        self.detail_page_html_str = ''
        self.detail_page_html_str = _read_html('../test_luton_detail_page.html')
        item = SpiderLutonItem()
        self.detail_page_html_response = TextResponse(url='test_detail_luton', body=self.detail_page_html_str,
                                                      encoding='utf8')
        self.xpath_strings = {'street_info': '//*[@id="contentContainer"]/article/div[1]/h1/span/text()',
                              'suburb_name': '//*[@id="contentContainer"]/article/div[1]/h1/small/span[1]/text()',
                              'state_name': '//*[@id="contentContainer"]/article/div[1]/h1/small/span[3]/text()',
                              'postal_code': '//*[@id="contentContainer"]/article/div[1]/h1/small/span[2]/text()',
                              'listing_type': '//*[@id="contentContainer"]/article/div[1]/div/div/text()',
                              'agent_count': 'count(//*[@id="contact"]/ul/li)',
                              'agent_name': '//*[@id="contact"]/ul/li[{}]/div/div/div/span/text()',
                              'agent_email': '//*[@id="contact"]/ul/li[{}]/div/div/dl/dd[1]/a/text()'}

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
        item['url'] = 'https://www.luton.com.au/1P47501/403-25-edinburgh-avenue-acton'
        self.assertEqual(expected_item[0]['url'],
                         self.spider_luton._initialize_item(self.detail_page_html_response, self.xpath_strings, item)[
                             'url'])
        self.assertEqual(expected_item[0]['full_address'],
                         self.spider_luton._initialize_item(self.detail_page_html_response, self.xpath_strings, item)[
                             'full_address'])
        self.assertEqual(expected_item[0]['listing_type'],
                         self.spider_luton._initialize_item(self.detail_page_html_response, self.xpath_strings, item)[
                             'listing_type'])
        self.assertEqual(expected_item[0]['agent'],
                         self.spider_luton._initialize_item(self.detail_page_html_response, self.xpath_strings, item)[
                             'agent'])
        self.assertEqual(expected_item[0]['agent'],
                         self.spider_luton._initialize_item(self.detail_page_html_response, self.xpath_strings, item)[
                             'agent'])

    def test__get_xpath_str(self):
        xpath_strings = {'street_info': '123'}
        expected_xpath_str = '123'
        expected_default_xpath_str = '//*[@id="contentContainer"]/div/div/div/text()'
        self.assertEqual(expected_xpath_str, self.spider_luton._get_xpath_str(xpath_strings, 'street_info'))
        self.assertEqual(expected_default_xpath_str, self.spider_luton._get_xpath_str(xpath_strings, 'listing_type'))

    def test_spider_parse_detail_page_response(self):
        expected_items_info = [{'full_address': '403/25 Edinburgh Avenue, Acton, ACT 2601', 'listing_type': 'sale',
                                'agent_info': [{'name': 'Sophie Luton', 'email': 'sophie.luton@luton.com.au'},
                                               {'name': 'Richard Luton', 'email': 'richard.luton@luton.com.au'}]},
                               {'full_address': '50/44 Macquarie Street, Barton, ACT 2600', 'listing_type': 'sale',
                                'agent_info': [{'name': 'Kate Yates', 'email': 'kate.yates@luton.com.au'}]
                                },
                               {'full_address': '109/8 Veryard Lane, Belconnen, ACT 2617', 'listing_type': 'sale',
                                'agent_info': [{'name': 'Charles Blackney', 'email': 'charles.blackney@luton.com.au'}]
                                }]
        expected_items = []
        for index, url in enumerate(self.expected_urls):
            item = SpiderLutonItem()
            item['url'] = 'test_detail_luton'
            item['full_address'] = expected_items_info[index]['full_address']
            item['listing_type'] = expected_items_info[index]['listing_type']
            item['agent'] = expected_items_info[index]['agent_info']
            expected_items.append(item)

        detail_request_generator = self.spider_luton.parse_detail_page(self.detail_page_html_response,
                                                                       self.xpath_strings)
        self.actual_item = next(detail_request_generator)
        self.assertEqual(expected_items[0]['url'], self.actual_item['url'])
        self.assertEqual(expected_items[0]['full_address'], self.actual_item['full_address'])
        self.assertEqual(expected_items[0]['listing_type'], self.actual_item['listing_type'])
        self.assertEqual(expected_items[0]['agent'][0]['name'], self.actual_item['agent'][0]['name'])
        self.assertEqual(expected_items[0]['agent'][0]['email'], self.actual_item['agent'][0]['email'])
