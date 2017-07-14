# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request

from dblp.items import DblpItem

import pandas as pd
import numpy as np 
from pandas import DataFrame, Series


class DblpSpider(scrapy.Spider):

    name = "dblpSpider"

    headers = { 
                'Host':'dblp.uni-trier.de',
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
                'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
                'Accept-Encoding':'gzip, deflate, sdch',
                'Referer':'http://dblp.uni-trier.de/',
                'Cookie': 'dblp-hideable-show-feeds=true; dblp-hideable-show-rawdata=true; dblp-view=y; dblp-search-mode=c',
                'Connection':'keep-alive',
                'Cache-Control':'max-age=0',}

    df_tmp = pd.read_csv("conference_dblp_source.csv")

    def start_requests(self):
        cnt = 0
        for con_id in self.df_tmp['con_id'].unique():
            df_cur = self.df_tmp[self.df_tmp.con_id == con_id]['paper_title']
            title_set = df_cur.reset_index()['paper_title']
            print "--------------------------------", cnt, "-----------------------------------"
            for paper_title in title_set:
                line = paper_title.replace("%","%25").replace(" ", "%20").replace(",", "%2C").replace(":", "%3A").replace("?", "%3F").replace("&", "%26").replace("'","%27")
                url = "http://dblp.uni-trier.de/search?q=" + line

                yield Request(url, headers=self.headers, meta={'paper_title':paper_title}, callback=self.parse_paper_url)
            cnt += 1

    def parse(self, response):
        item = PaperscrapyItem()   
        yield item


    def parse_paper_url(self, response):

        try:
        
            dblp_name = response.xpath('//ul[@class="publ-list"]/li[2]/div[@class="data"]/a/span[1]/span/text()').extract()
            #print "----------------------------", dblp_name, "--------------------------------"
            dblp_num = len(dblp_name)
            if dblp_num == 0:
                raise Exception("Not matches paper!")
            elif dblp_num > 1:
                raise Exception("Too many matches paper!")
            dblp_name = dblp_name[0]
        except Exception, e:        # 匹配到多个或者没匹配到
            print e.args[0]
            print 'dblp_name', dblp_name

        paper_item = DblpItem()  # 声明自己定义的item类 并赋值
        paper_item['paper_title'] = response.meta['paper_title'] 
        paper_item['dblpname'] = dblp_name

        yield paper_item
