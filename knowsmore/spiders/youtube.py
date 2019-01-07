# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy import Selector
from knowsmore.items import YoutubeItem
from ..common import *

class YoutubeSpider(scrapy.Spider):
    name = 'youtube'
    allowed_domains = ['www.youtube.com']
    start_urls = ['https://www.youtube.com/watch?v=3vkqOdMBP48']

    def parse(self, response):
        ytInitialData = r1(r'window\["ytInitialData"\] = (.*?)}};', response.body)
        if ytInitialData:
            ytInitialData = '%s}}' % ytInitialData
            ytInitialDataObj = json.loads(ytInitialData)
            
            videoInfo = ytInitialDataObj['contents']['twoColumnWatchNextResults']['results']['results']['contents'][0]['videoPrimaryInfoRenderer']
            Item = YoutubeItem(
                title = videoInfo['title']['simpleText'].encode('utf-8'),
                view_count = videoInfo['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']
            )

            # yield Item
            print Item
            