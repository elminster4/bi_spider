# -*- coding: utf-8 -*-

from scrapy.exporters import JsonItemExporter
from scrapy import signals


class SiteMapJsonExportPipeline(object):
	'''Process the SiteMap spider output Items, and write them as JSON to an output file. The output file is taken from the Spider's config (spider.config)'''

	@classmethod
	def from_crawler(cls, crawler):
		''' Boilerplate '''
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

	def spider_opened(self, spider):
		self.file = open(spider.config['map_file'], 'wb')
		self.exporter = JsonItemExporter(self.file)
		self.exporter.start_exporting()

	def spider_closed(self, spider):
		self.exporter.finish_exporting()
		self.file.close()

	def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
