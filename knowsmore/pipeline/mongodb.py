from ..model.mongodb import *
from ..common import *

class MongoPipeline(object):
    def open_spider(self,spider):
        connect(
            spider.settings.get('DB_NAME'),
            host=spider.settings.get('DB_HOST'),
            port=spider.settings.get('DB_PORT'),
            username=spider.settings.get('DB_USERNAME'),
            password=spider.settings.get('DB_PASSWORD')
        )

    def close_spider(self,spider):
        # no need to close connection?
        pass

    def process_item(self, item, spider):
#==================================================
        if spider.name is 'youtube_list':
            self.set_youtube_list_item(item)
            return item
        if spider.name is 'youtube':
            self.set_youtube_item(item)
            return item
#==================================================
        if spider.name is 'youku_list':
            self.set_youku_list_item(item)
            return item
#==================================================
        if spider.name is 'weibo_user':
            className = item.__class__.__name__
            if className == 'WeiboUserItem':
                self.set_weibo_user_item(item)
                return item['user']['id']
            if className == 'WeiboStatusItem':
                self.set_weibo_status_item(item)
                return len(item['cards'])
            return None
#==================================================
        return item

    '''
    Save Weibo Status Item to DB
    '''
    def set_weibo_status_item(self, item):
        for cItem in item['cards']:
            if cItem['card_type'] != 9:
                continue

            dbItem = WeiboStatusModel.objects(mid=cItem['mblog']['mid']).first()
            if not dbItem:
                dbItem = WeiboStatusModel(
                    mid = cItem['mblog']['mid'],
                    mblog = cItem['mblog']
                )

            dbItem.save()
            

    '''
    Save Weibo User Item to DB
    '''
    def set_weibo_user_item(self, item):
        dbItem = WeiboUserModel.objects(uid=item['user']['id']).first()
        if not dbItem:
            dbItem = WeiboUserModel(
                uid = item['user']['id'],
            )

        dbItem.fans_url = item['fans_url']
        dbItem.follow_url = item['follow_url']
        dbItem.more_url = item['more_url']
        dbItem.screen_name = item['user']['screen_name']
        dbItem.profile_image_url = item['user']['profile_image_url']
        dbItem.profile_url = item['user']['profile_url']
        dbItem.statuses_count = item['user']['statuses_count']
        dbItem.verified = item['user']['verified']
        dbItem.verified_type = item['user']['verified_type']
        dbItem.verified_type_ext = item['user']['verified_type_ext']
        dbItem.verified_reason = item['user']['verified_reason']
        dbItem.close_blue_v = item['user']['close_blue_v']
        dbItem.description = item['user']['description']
        dbItem.gender = item['user']['gender']
        dbItem.mbtype = item['user']['mbtype']
        dbItem.urank = item['user']['urank']
        dbItem.mbrank = item['user']['mbrank']
        dbItem.follow_me = item['user']['follow_me']
        dbItem.following = item['user']['following']
        dbItem.followers_count = item['user']['followers_count']
        dbItem.follow_count = item['user']['follow_count']
        dbItem.cover_image_phone = item['user']['cover_image_phone']
        dbItem.avatar_hd = item['user']['avatar_hd']
        dbItem.like = item['user']['like']
        dbItem.like_me = item['user']['like_me']

        dbItem.save()

    '''
    Save Youtube Item to DB
    '''
    def set_youtube_item(self, item):
        dbItem = YoutubeModel.objects(title=item['title']).first()
        if not dbItem:
            dbItem = YoutubeModel(
                title = item['title'],
                view_count = item['view_count'],
            )
            
        dbItem.save()

    '''
    Save Youtube List Item to DB
    '''
    def set_youtube_list_item(self, item):
        dbItem = YoutubePlaylistModel.objects(playlist_id=item['playlist_id']).first()
        if not dbItem:
            dbItem = YoutubePlaylistModel(
                playlist_id = item['playlist_id'],
                videos = []
            )

        dbItem['videos'] = []
        for video in item['videos']:
            playlistVideoItem = YoutubePlaylistVideoModel(
                playlist_id = item['playlist_id'],
                video_id = video['video_id'],
                thumbnail = video['thumbnail'],
                title = video['title'],
                index = video['index'],
                length_seconds = video['length_seconds'],
                is_playable = video['is_playable']
            )
            dbItem['videos'].append(playlistVideoItem)
        dbItem.save()

    '''
    Save Youku List Item to DB
    '''
    def set_youku_list_item(self, item):
        dbItem = YoukuListModel.objects(link=item['link']).first()
        if not dbItem:
            dbItem = YoukuListModel(
                thumb_img = item['thumb_img'],
                title = item['title'],
                link = item['link'],
                tag = item['tag'],
                actors = item['actors'],
                play_times = item['play_times'],
            )

        dbItem.thumb_img = item['thumb_img']
        dbItem.title = item['title']
        dbItem.tag = item['tag']
        dbItem.actors = item['actors']
        dbItem.play_times = item['play_times']

        dbItem.save()

