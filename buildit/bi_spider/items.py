# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BuilditItem(scrapy.Item):
	# define the fields for your item here like:
	external_urls = scrapy.Field()
	internal_urls = scrapy.Field()
	images = scrapy.Field()
