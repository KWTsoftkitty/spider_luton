import scrapy


class SpiderLutonItem(scrapy.Item):
    """spider item object for Luton Property"""
    url = scrapy.Field()
    full_address = scrapy.Field()
    listing_type = scrapy.Field()
    agent = scrapy.Field()
