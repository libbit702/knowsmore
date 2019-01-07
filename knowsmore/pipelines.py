# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import shutil
import os,sys
from pipeline.mongodb import *
from common import *
# from pipeline.sqlalchemy import *

class ProxySavePipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings)

    def __init__(self, settings):
        self.proxy_txt = None
        self.source_file = '%s%s' % (project_proxy_file, '.tmp')
        self.dest_file = project_proxy_file

    def open_spider(self,spider):
        if spider.name in spider.settings.get('RANDOM_PROXY_SPIDER'):
            self.proxy_txt = open(self.source_file, 'wb')

    def close_spider(self,spider):
        if spider.name in spider.settings.get('RANDOM_PROXY_SPIDER'):
            self.proxy_txt.close()
            shutil.copy(self.source_file, self.dest_file)

    def process_item(self, item, spider):
        if spider.name in spider.settings.get('RANDOM_PROXY_SPIDER'):
            self.proxy_txt.write(item['proxy'] + "\n")
            return item
        else:
            return item
