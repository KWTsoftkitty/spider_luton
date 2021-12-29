# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import jsonlines
import json


class SpiderLutonPipeline:

    def __init__(self):
        self.fp = open('luton_data.jsonl', 'a')
        self.writer = jsonlines.Writer(self.fp)

    def process_item(self, item, spider):
        item_json = json.dumps(dict(item), ensure_ascii=False)
        self.writer.write(item_json)
        return item

    def close_spider(self, spider):
        self.writer.close()
        self.fp.close()
