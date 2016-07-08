# -*- coding: utf-8 -*-

import scrapy


def to_list(value):
	''' Converts a list-like object (like a set) to a list, for canonicalisation down the line '''
	return list(value)	

class SiteMapItem(scrapy.Item):
	''' One 'unit' of a site map '''
	url = scrapy.Field()
	external_links = scrapy.Field( serializer=to_list )
	internal_links = scrapy.Field( serializer=to_list )
	images = scrapy.Field( serializer=to_list )


