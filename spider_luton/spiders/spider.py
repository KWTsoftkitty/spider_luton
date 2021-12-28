import scrapy


class SpiderLuton(scrapy.Spider):
    name = 'luton'
    allowed_domains = ['www.luton.com.au']
    start_urls = ['http://www.luton.com.au/properties-for-sale']

    def parse(self, response):
        urls = response.xpath('//*[@id="contentContainer"]/article/div/div/ul/li/div/a/@href').extract()
        return urls
