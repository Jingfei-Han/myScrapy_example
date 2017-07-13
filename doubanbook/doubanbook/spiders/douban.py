import re
import json

from scrapy.selector import Selector
try:
	from scrapy.spiders import Spider 
except:
	from scrapy.spiders import BaseSpider as Spider

from scrapy.utils.response import get_base_url
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle 

from doubanbook.items import *

class DoubanBookSpider(CrawlSpider):
	name = "doubanbook"
	allowed_domains = ["douban.com"]
	start_urls = [
		"https://book.douban.com/tag"
	]
	rules = [
		Rule(sle(allow=("/subject/\d+$")), callback="parse_2"),
		Rule(sle(allow=("/tag/[^/]+$", )), follow=True)
	]

	def parse_2(self, response):
		items = []
		sel = Selector(response)
		# #wrapper means <div id='wrapper'>
		sites = sel.css('#wrapper')
		for site in sites:
			item = DoubanSubjectItem()
			item['title'] = site.css("h1 span::text").extract()
			item['link'] = response.url 
			item['content_intro'] = site.css('#link-report .intro p::text').extract()
			items.append(item)

			print item
		return items

	def process_request(self, request):
		return request