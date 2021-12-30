import jsonlines


class SpiderLutonPipeline:

    def __init__(self):
        self.fp = open('luton_data.jsonl', 'a')
        self.writer = jsonlines.Writer(self.fp)

    def process_item(self, item, spider):
        self.writer.write(dict(item))
        return item

    def close_spider(self, spider):
        self.writer.close()
        self.fp.close()
