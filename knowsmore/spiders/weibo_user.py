# -*- coding: utf-8 -*-
import scrapy
import re
import json
import os,sys
from scrapy import Selector, Request
from knowsmore.items import WeiboUserItem, WeiboStatusItem
from ..common import *
from ..model.mongodb import *

WEIBO_USER_CONFIG = {
    'BASE_URL' : 'https://m.weibo.cn',
    'USER_IDS' : ['6883966016']
}

class WeiboUserSpider(scrapy.Spider):

    name = "weibo_user"

    def start_requests(self):
        for uid in WEIBO_USER_CONFIG['USER_IDS']:
            url = '%s/profile/info?uid=%s' % (WEIBO_USER_CONFIG['BASE_URL'], uid)
            yield Request(url)
            # Define your statuses implementation here, just a demo below
            for i in range(1, 2):
                status_url = '%s/api/container/getIndex?containerid=230413%s_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=%d' % (WEIBO_USER_CONFIG['BASE_URL'], uid, i)
                yield Request(status_url, callback=self.parse_status)

    # https://m.weibo.cn/profile/1784537661
    def parse(self, response):
        user_data = json.loads(response.text)
        yield WeiboUserItem(
            fans_url = user_data['data']['fans'],
            follow_url = user_data['data']['follow'],
            more_url = user_data['data']['more'],
            user = user_data['data']['user']
        )

    # https://m.weibo.cn/api/container/getIndex?containerid=2304131784537661_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page=2
    def parse_status(self, response):
        status_data = json.loads(response.text)
        yield WeiboStatusItem(
            cards = status_data['data']['cards']
        )

