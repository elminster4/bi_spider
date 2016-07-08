import os

from scrapy.http import Response, Request

# Adapted from http://stackoverflow.com/questions/6456304/scrapy-unit-testing
def fake_response_from_file(content_file_name, url):
	"""
	Create a Scrapy fake HTTP response from a HTML file
	@param file_name: The relative filename from the responses directory,
					  but absolute paths are also accepted.
	@param url: The URL of the response.
	returns: A scrapy HTTP response which can be used for unittesting.
	"""

	request = Request(url=url)
	if not content_file_name[0] == '/':
		responses_dir = os.path.dirname(os.path.realpath(__file__))
		file_path = os.path.join(responses_dir, content_file_name)
	else:
		file_path = content_file_name

	file_content = open(file_path, 'r').read()

	response = Response(url=url,
		request=request,
		body=file_content)
	response.encoding = 'utf-8'
	response.text = unicode(file_content)
	return response
