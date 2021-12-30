"""start the spider from cmdline"""
import sys

from scrapy import cmdline


sys.argv = ['scrapy', 'crawl', 'luton']
cmdline.execute()
