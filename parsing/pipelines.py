from datetime import date

from scrapy import signals
from scrapy.exporters import CsvItemExporter


class ParsingPipeline:
    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file = open(f'parse_files/{spider.name}_{date.today()}.csv', 'w+b')
        self.files[spider] = file
        self.exporter = CsvItemExporter(file, delimiter=";")
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
