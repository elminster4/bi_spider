
# Buildit Site Map Spider 

* Written in Python using the Scrapy web crawling module
* The settings file is in buildit/bi_spider/settings.py; it controls the behaviour of the crawler and of the site map spider in particular (e.g., the output file for the map, by default /tmp/buildit_map)

* Using Scrapy is a little overkill for this project, as it's a very powerful crawler, but not much; it benefits from being very mature, widely used, fast, and flexible. We're not tied to the exact structure of the site's HTML, and we can easily change the output format of the site map. Altogether, it's easy to learn (I just did), we're reasonably future-proof at low cost, and reinvented wheels don't tend to be prod-grade.

* The controlling file is buildit/bi_spider/spiders/site_map_spider.py; it configures the crawler, and emits two types of replies - Requests, which are further URLs for the crawler to process - the deduplication is inbuilt, and SiteMapItems, which are one element in a site map- URL, external links, internal links, images. Items are then processed asynchronously by the SiteMapJsonExportPipeline, which will write the results into a JSON file.

* The file organisation respects the Scrapy default; while I would probably change it somewhat (put the config file in a config/ dir, maybe put Spiders, Items, and Pipeline in the same module since they are largely interdependent), it's more important to respect the convention if there's no overriding reason not to. It makes looking/asking for help a lot easier.

* The map is exported as JSON. There's no particular reason for it, apart from being easy to further process by other tools. We can easily change the pipeline to export to a different format, run post-processing, etc. The config should probably specify what exporter to use, and give it the file as config if relevant.

* There is one unit test, checking that the parsing is correct; more could be added to check that the file is correctly output, that the config makes sense, etc. Scrapy encourages using function contracts instead of unit tests, as it doesn't expose all the internals required to have unit tests be properly separated. I haven't looked much into that, as most of them need to be user-defined. It should certainly be considered, provided they can be integrated into regular unit tests ongoing on the wider system.

## Run
* Install the scrapy module:  
		<pip install scrapy>
* Run the spider, e.g. from the buildit/ directory: 
		<scrapy runspider bi_spider/spiders/site_map.py -a config_module_name=bi_spider.settings>

## Unit testing
* Install the phpunit module if not present already: 
		<pip install phpunit>
* from tests/, run 
		<pytest SiteMapSpiderTest.py>
