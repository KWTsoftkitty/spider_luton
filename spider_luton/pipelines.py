import os
import re
import jsonlines
from scrapy.exceptions import DropItem


class SpiderLutonPipeline:

    def __init__(self):
        output_path = './out/'
        if not os.path.exists(output_path):
            os.makedirs(output_path, exist_ok=True)
        self.fp = open(output_path + 'luton_data.jsonl', 'w+')
        self.writer = jsonlines.Writer(self.fp)

    def process_item(self, item, spider):
        self.writer.write(dict(item))
        return item

    def close_spider(self, spider):
        self.writer.close()
        self.fp.close()


class StateFilterPipeline:
    """A filter to ignore the data when state name is NSW"""
    def process_item(self, item, spider):
        full_address = item['full_address']
        regex = r'(?P<state>\w+)\s?\d+$'
        pattern = re.compile(regex)
        matched_result = pattern.search(full_address)
        state_matched = matched_result.group('state')
        if state_matched == 'NSW':
            raise DropItem('ignore the data that its state name is %s' % state_matched)
        return item
