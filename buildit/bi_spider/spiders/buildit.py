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
	all_links = {} # here we add all results to a structure so that we can display them later all at once. allows postprocessing like sorting at memory cost. ok for one site. could also print as we go or write to temp file.


	def parse(self, response):
		sel = Selector(response)
                i = 0
		item = BuilditItem()
                item['url'] = response.url
	 	item['external_links'] = set()
		item['internal_links'] = set()
		item['images'] = set()

		for link in sel.xpath('//img/@src'):
			url = response.urljoin(link.extract())
			item['images'].add(url)

		for link in sel.xpath('//a/@href'):
			url = response.urljoin(link.extract())
			if re.search(r'https?://' + BuilditSpider.domain, url): # we just add the link to the right type and yield both urls, leaving the choice of what to crawl next to the rules; this keeps the crawling (input) from the generated map (output) decoupled. we don't consider subdomains internal.
                            #if not url in item['internal_links']:
                            item['internal_links'].add(url) 
			else:
                            
			    item['external_links'].add(url) 

                        i += 1 
                        #if i < 100:
			    #yield Request(url, callback=self.parse) 
                yield item






