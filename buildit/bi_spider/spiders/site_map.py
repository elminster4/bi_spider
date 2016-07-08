from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import Request

from importlib import import_module
import re

from bi_spider.items import SiteMapItem

class SiteMapSpider(CrawlSpider):
	''' A spider that will build a site map, showing what external, internal, and image links each page on a site references'''
	name = 'sitemapspider'

	def __init__(self, config_module_name):
		''' This spider needs to be given a parameter config_module_name from the command line, pointing to a module containing a dictionary like
			'site_map_spider' : {
				'crawl_domain': 'www.yahoo.com', # what domains we should spider; subdomains are not considered part of the domain
				'start_urls': ['http://www.yahoo.com'], # what pages to start crawling from
				'map_file': '/tmp/foo' # where to write the map
			}
			TODO: the map_file param should really be what exporter to use, with the map_file as its parameter if relevant
		'''
		mod = import_module(config_module_name)
		settings = getattr(mod, 'site_map_spider')
		self.config = settings

		self.domain = settings['crawl_domain']
		# we only crawl through the specified domain
		self.allowed_domains = [self.domain]
		self.start_urls = settings['start_urls']


	def parse(self, response):
		sel = Selector(response)
		item = SiteMapItem()
		item['url'] = response.url
	 	item['external_links'] = set()
		item['internal_links'] = set()
		item['images'] = set()

		for link in sel.xpath('//img/@src'):
			url = response.urljoin(link.extract())
			item['images'].add(url)

		for link in sel.xpath('//a/@href'):
			url = response.urljoin(link.extract())
			# we just add the link to the right type and yield both urls, leaving the choice of what to crawl next to the rules in allowed_domains[]; this keeps the crawling (input) from the generated map (output) decoupled. we don't consider subdomains internal.
			if re.search(r'https?://' + self.domain, url): 
				item['internal_links'].add(url) 
			else:
			    item['external_links'].add(url) 

			yield Request(url, callback=self.parse) 
	
		yield item


