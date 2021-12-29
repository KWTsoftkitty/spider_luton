import scrapy

from ..items import SpiderLutonItem
from ..settings import USER_AGENT


class SpiderLuton(scrapy.Spider):
    name = 'luton'
    allowed_domains = ['www.luton.com.au']
    start_urls = ['http://www.luton.com.au/{}']
    xpath_str_for_href = '//*[@id="contentContainer"]/article/div/div/ul/li/div/a/@href'
    xpath_str_for_next_page = '//div[@class="pager-nav"]/a[contains(@class, "next")]/@href'

    default_xpath_strings = {'street_info': '//*[@id="contentContainer"]/div/h1/span/text()',
                             'suburb_name': '//*[@id="contentContainer"]/div/h1/small/span[1]/text()',
                             'state_name': '//*[@id="contentContainer"]/div/h1/small/span[3]/text()',
                             'postal_code': '//*[@id="contentContainer"]/div/h1/small/span[2]/text()',
                             'listing_type': '//*[@id="contentContainer"]/div/div/div/text()',
                             'agent_count': 'count(//*[@id="contentContainer"]/article/div/div[1]/ul/li)',
                             'agent_name': '//*[@id="contentContainer"]/article/div/div[1]/ul/li[{'
                                           '}]/div/div/div/span/text()',
                             'agent_email': '//*[@id="contentContainer"]/article/div/div[1]/ul/li[{}]/div/div/dl/dd['
                                            '1]/a/text()'}

    def start_requests(self):
        channels = ['/properties-for-sale', '/properties-for-rent']
        for channel in channels:
            url = self.start_urls[0].format(channel)
            yield scrapy.Request(url, callback=self.parse, headers={'User-Agent': USER_AGENT})

    def parse(self, response):
        details_urls = response.xpath(self.xpath_str_for_href).extract()
        for details_url in details_urls:
            item = SpiderLutonItem()
            item['url'] = details_url
            yield scrapy.Request(details_url, callback=self.parse_detail_page, headers={'User-Agent': USER_AGENT})

        next_page_info = response.xpath(self.xpath_str_for_next_page).extract_first()
        if next_page_info != '#':
            next_page_url = self.start_urls[0].format(next_page_info[1:])
            yield scrapy.Request(next_page_url, callback=self.parse, headers={'User-Agent': USER_AGENT})

    def _initialize_item(self, response):
        street_info = response.xpath(
            self._get_xpath_str(self.default_xpath_strings, 'street_info')).extract_first()
        item = SpiderLutonItem()
        item['url'] = response._get_url()
        suburb_name = response.xpath(self._get_xpath_str(self.default_xpath_strings, 'suburb_name')).extract_first()
        state_name = response.xpath(self._get_xpath_str(self.default_xpath_strings, 'state_name')).extract_first()
        postal_code = response.xpath(self._get_xpath_str(self.default_xpath_strings, 'postal_code')).extract_first()
        item['full_address'] = street_info + ', ' + suburb_name + ', ' + state_name + ' ' + postal_code
        listing_type = response.xpath(
            self._get_xpath_str(self.default_xpath_strings, 'listing_type')).extract_first()
        if listing_type:
            item['listing_type'] = listing_type.strip()[4:].lower()
        item['agent'] = []
        agent_number = response.xpath(self._get_xpath_str(self.default_xpath_strings, 'agent_count')).extract_first()
        agent_count = 1
        while True:
            agent_name = response.xpath(
                self._get_xpath_str(self.default_xpath_strings, 'agent_name').format(agent_count)).extract_first()
            agent_email = response.xpath(
                self._get_xpath_str(self.default_xpath_strings, 'agent_email').format(agent_count)).extract_first()
            item['agent'].append({'name': agent_name, 'email': agent_email})
            agent_count += 1
            if agent_count > int(agent_number[0:1]):
                break
        return item

    def _get_xpath_str(self, xpath_strings, property_name):
        return xpath_strings.get(property_name, self.default_xpath_strings[property_name])

    def parse_detail_page(self, response):
        # item = response.meta['item']
        item = self._initialize_item(response)
        yield item
