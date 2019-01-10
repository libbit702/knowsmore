# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy import Selector, Request
from knowsmore.items import YoukuListItem
from ..common import *
from ..model.mongodb import *

class YoukuListSpider(scrapy.Spider):
    name = "youku_list"

    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
        }
    }

    start_urls = [
        'https://list.youku.com/category/show/c_96_s_1_d_4_p_29.html'
    ]

    def parse(self, response):
        GRID_SELECTOR = '.panel .mr1'        
        for grid in response.css(GRID_SELECTOR):
            THUMB_IMG_SELECTOR = '.p-thumb img::attr(_src)'
            LINK_SELECTOR = '.info-list .title a::attr(href)'
            TITLE_SELECTOR = '.info-list .title a::text'
            ACTORS_SELECTOR = '.info-list .actor a::text'
            TAG_SELECTOR = '.p-thumb .p-thumb-tagrt span::text'
            PLAY_TIMES_SELECTOR = '.info-list li:nth-child(3)::text'

            item_thumb_img = grid.css(
                THUMB_IMG_SELECTOR).extract_first()
            item_link = grid.css(
                LINK_SELECTOR).extract_first()
            item_title = grid.css(
                TITLE_SELECTOR).extract_first()
            item_actors = grid.css(
                ACTORS_SELECTOR).extract()
            item_tag = grid.css(
                TAG_SELECTOR).extract()
            item_play_times = grid.css(
                PLAY_TIMES_SELECTOR).extract_first()

            # Build Scrapy Item
            youku_item = YoukuListItem(
                thumb_img = item_thumb_img,
                link =  item_link,
                title = item_title,
                actors = item_actors,
                play_times = item_play_times,
                tag = item_tag
            )

            # Send to Pipelines
            yield youku_item


        NEXT_PAGE_SELECTOR = '.yk-pages .next a::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page is not None:
            print next_page
            yield response.follow(next_page)
