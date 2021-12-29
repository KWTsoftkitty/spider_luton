import scrapy
from ..items import SpiderLutonItem


class SpiderLuton(scrapy.Spider):
    name = 'luton'
    allowed_domains = ['www.luton.com.au']
    start_urls = ['http://www.luton.com.au/{}']
    xpath_str_for_href = '//*[@id="contentContainer"]/article/div/div/ul/li/div/a/@href'
    xpath_str_for_next_page = '//div[@class="pager-nav"]/a[contains(@class, "next")]/@href'

    def start_requests(self):
        channels = ['/properties-for-sale', '/properties-for-rent']
        for channel in channels:
            url = self.start_urls[0].format(channel)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        details_urls = response.xpath(self.xpath_str_for_href).extract()
        for details_url in details_urls:
            yield scrapy.Request(details_url, callback=self.parse_detail_page)

        next_page_info = response.xpath(self.xpath_str_for_next_page).extract_first()
        if next_page_info != '#':
            next_page_url = self.start_urls[0].format(next_page_info[1:])
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail_page(self, response):
        pass
