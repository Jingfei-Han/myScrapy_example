# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
#from scrapy.item import Item, Field


class DoubanbookItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    num = scrapy.Field()

class DoubanSubjectItem(scrapy.Item):
	title = scrapy.Field()
	link = scrapy.Field()
	info = scrapy.Field()
	rate = scrapy.Field()
	votes = scrapy.Field()
	content_intro = scrapy.Field()
	author_intro = scrapy.Field()
	tags = scrapy.Field()
