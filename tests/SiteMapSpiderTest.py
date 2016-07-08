import unittest
from bi_spider.spiders import site_map
from bi_spider.items import SiteMapItem
from responses import fake_response_from_file


class SiteMapSpiderTest(unittest.TestCase):

	def setUp(self):
		self.spider = site_map.SiteMapSpider()


	def test_parse(self):
		results = self.spider.parse(fake_response_from_file('samples/wiprodigital_index.html', 'http://wiprodigital.com'))
		
		for r in results:
			if type(r) is SiteMapItem:
				item = r

		# testing that the URLs are represented as a set is a bit iffy and too close to the implementation; we may want to think about converting everything to lists, or iterating through to compare contents
		sample_results = {
			'external_links': set([
					'http://subdomain.subdomain.wiprodigital.com/4',
                    'http://external.com/3',
                    'https://external.com/1'
			]),
			'images': set([
					'http://wiprodigital.com/imgpath/2.jpg',
			        'http://11689-presscdn-0-83.pagely.netdna-cdn.com/wp-content/uploads/2015/09/WD_logo_150X27.png'
			]),
			'internal_links': set([
					'http://wiprodigital.com/2',
                    'http://wiprodigital.com/',
                    'http://wiprodigital.com/#section-1',
                    'http://wiprodigital.com/#section-2'
			]),
			'url': 'http://wiprodigital.com'
		}
		
		self.assertEqual(item, sample_results)

	''' 
		TODO: test to check the output is a JSON file
		We could also define test_crawl, although that will only test for the 'yield URL' being present - the rest would be unit testing Scrapy
	'''
