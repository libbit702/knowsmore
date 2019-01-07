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
            self.set_youtube_item(item)
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

    '''
    Save Weibo Status Item to DB
    '''
    def set_weibo_status_item(self, item):
        for cItem in item['cards']:
            if cItem['card_type'] != 9:
                continue

            sItem = WeiboStatusModel.objects(mid=cItem['mblog']['mid']).first()
            if not sItem:
                sItem = WeiboStatusModel(
                    mid = cItem['mblog']['mid'],
                    mblog = cItem['mblog']
                )

            sItem.save()
            

    '''
    Save Weibo User Item to DB
    '''
    def set_weibo_user_item(self, item):
        wItem = WeiboUserModel.objects(uid=item['user']['id']).first()
        if not wItem:
            wItem = WeiboUserModel(
                uid = item['user']['id'],
            )

        wItem.fans_url = item['fans_url']
        wItem.follow_url = item['follow_url']
        wItem.more_url = item['more_url']
        wItem.screen_name = item['user']['screen_name']
        wItem.profile_image_url = item['user']['profile_image_url']
        wItem.profile_url = item['user']['profile_url']
        wItem.statuses_count = item['user']['statuses_count']
        wItem.verified = item['user']['verified']
        wItem.verified_type = item['user']['verified_type']
        wItem.verified_type_ext = item['user']['verified_type_ext']
        wItem.verified_reason = item['user']['verified_reason']
        wItem.close_blue_v = item['user']['close_blue_v']
        wItem.description = item['user']['description']
        wItem.gender = item['user']['gender']
        wItem.mbtype = item['user']['mbtype']
        wItem.urank = item['user']['urank']
        wItem.mbrank = item['user']['mbrank']
        wItem.follow_me = item['user']['follow_me']
        wItem.following = item['user']['following']
        wItem.followers_count = item['user']['followers_count']
        wItem.follow_count = item['user']['follow_count']
        wItem.cover_image_phone = item['user']['cover_image_phone']
        wItem.avatar_hd = item['user']['avatar_hd']
        wItem.like = item['user']['like']
        wItem.like_me = item['user']['like_me']

        wItem.save()


    '''
    Save Youtube Item to DB
    '''
    def set_youtube_item(self, item):
        playlistItem = YoutubePlaylistModel.objects(playlist_id=item['playlist_id']).first()
        if not playlistItem:
            playlistItem = YoutubePlaylistModel(
                playlist_id = item['playlist_id'],
                videos = []
            )

        playlistItem['videos'] = []
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
            playlistItem['videos'].append(playlistVideoItem)
        playlistItem.save()

