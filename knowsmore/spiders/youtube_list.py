# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy import Selector
from knowsmore.items import YoutubePlaylistItem, YoutubePlaylistVideoItem
from ..common import *

class YoutubeListSpider(scrapy.Spider):
    name = 'youtube_list'
    allowed_domains = ['www.youtube.com']
    start_urls = ['https://www.youtube.com/playlist?list=PLEbPmOCXPYV67l45xFBdmodrPkhzuwSe9']

    def parse(self, response):
        # Extract JSON Data with Regex Expression
        ytInitialData = r1(r'window\["ytInitialData"\] = (.*?)}};', response.body)
        if ytInitialData:
            ytInitialData = '%s}}' % ytInitialData
            ytInitialDataObj = json.loads(ytInitialData)

            # Assign VideoList info to variable
            playListInfo = ytInitialDataObj['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']

            # Build Scrapy Item
            playList = YoutubePlaylistItem(
                playlist_id = playListInfo['playlistId'],
                videos = []
            )

            # Insert the videoItem to YoutubePlaylistItem videos field
            for videoInfo in playListInfo['contents']:
                videoInfo = videoInfo['playlistVideoRenderer']
                videoItem = YoutubePlaylistVideoItem(
                    playlist_id = playListInfo['playlistId'],
                    video_id = videoInfo['videoId'],
                    thumbnail = videoInfo['thumbnail']['thumbnails'],
                    title = videoInfo['title']['simpleText'],
                    index = videoInfo['index']['simpleText'],
                    length_seconds = videoInfo['lengthSeconds'],
                    is_playable = videoInfo['isPlayable']
                )
                playList['videos'].append(videoItem)
            
            yield playList
            
        