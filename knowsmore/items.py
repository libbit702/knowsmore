# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field

# Weibo User Info
class WeiboUserItem(Item):
    fans_url = scrapy.Field()
    follow_url = scrapy.Field()
    more_url = scrapy.Field()
    user = scrapy.Field()

class WeiboStatusItem(Item):
    cards = scrapy.Field()

# Youtube Video Page
class YoutubeItem(Item):
    title = scrapy.Field()
    view_count = scrapy.Field()

# Youtube Playlist Page
class YoutubePlaylistItem(Item):
    playlist_id = scrapy.Field()
    videos = scrapy.Field()

# Youtube Playlist Item
class YoutubePlaylistVideoItem(Item):
    playlist_id = scrapy.Field()
    video_id = scrapy.Field()
    thumbnail = scrapy.Field()
    title = scrapy.Field()
    index = scrapy.Field()
    length_seconds = scrapy.Field()
    is_playable = scrapy.Field()

# Youku Playlist Page
class YoukuListItem(Item):
    thumb_img = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    tag = scrapy.Field()
    actors = scrapy.Field()
    play_times = scrapy.Field()
