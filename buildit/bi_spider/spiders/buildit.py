from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy import Request
from bi_spider.items import BuilditItem
import re

class BuilditSpider(CrawlSpider):
	domain = "wiprodigital.com"

	name = 'builditspider'
	allowed_domains = [domain]
	start_urls = ['http://' + domain]
	all_links = {}


	def parse(self, response):
		sel = Selector(response)
		item = BuilditItem()
	 	item['external_urls'] = []
		item['internal_urls'] = []
		item['images'] = []

		for link in sel.xpath('//img/@href'):
			url = response.urljoin(link.extract())
			item['images'].append(url)

		for link in sel.xpath('//a/@href'):
			url = response.urljoin(link.extract())
			if re.search(r'[https?://][^/]+' + domain, url): # we just add the link to the right type and yield both urls, leaving the choice of what to crawl next to the rules; this keeps the crawling (input) from the generated map (output) decoupled
				item['internal_urls'].append(url) 
			else:
				item['external_urls'].append(url) 

			self.all_links[url] = item
			yield Request(url, callback=self.parse)


	def parse_titles(self, response):
		for post_title in response.css('div.entries > ul > li a::text').extract():
			yield {'title': post_title}

