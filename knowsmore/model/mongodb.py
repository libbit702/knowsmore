from ..common import *
from mongoengine import *

# ================== Youtube Playlist BEGIN ======================== #
class YoutubePlaylistVideoModel(EmbeddedDocument):
    playlist_id = StringField(required=True)
    video_id = StringField(required=True, unique=True)
    thumbnail = ListField()
    title = StringField(required=True)
    index = IntField()
    length_seconds = IntField()
    is_playable = BooleanField()

class YoutubePlaylistModel(Document):
    playlist_id = StringField(required=True, unique=True)
    videos = ListField(EmbeddedDocumentField(YoutubePlaylistVideoModel))

    meta = {
        'collection':'youtube_playlist'
    }

class YoutubeModel(Document):
    title = StringField(required=True)
    view_count = StringField()

    meta = {
        'collection':'youtube'
    }
# ================== Youtube Playlist END ======================== #


# ================== Weibo User BEGIN ======================== #
class WeiboUserModel(Document):
    fans_url = StringField()
    follow_url = StringField()
    more_url = StringField()

    uid = IntField(required=True, unique=True)
    screen_name = StringField()
    profile_image_url = StringField()
    profile_url = StringField()
    statuses_count = IntField()
    verified = BooleanField()
    verified_type = IntField()
    verified_type_ext = IntField()
    verified_reason = StringField()
    close_blue_v = BooleanField()
    description = StringField()
    gender = StringField()
    mbtype = IntField()
    urank = IntField()
    mbrank = IntField()
    follow_me = BooleanField()
    following = BooleanField()
    followers_count = IntField()
    follow_count = IntField()
    cover_image_phone = StringField()
    avatar_hd = StringField()
    like = BooleanField()
    like_me = BooleanField()

    meta = {
        'collection':'weibo_user'
    }

class WeiboStatusModel(Document):
    mid = StringField(required=True)
    mblog = DictField(required=True)

    meta = {
        'collection':'weibo_status'
    }
# ================== Weibo User END ======================== #

# ================== Youku List BEGIN ======================== #
class YoukuListModel(Document):
    link = StringField(required=True, unique=True)
    thumb_img = StringField()
    title = StringField()
    tag = ListField()
    actors = ListField()
    play_times = StringField()

    meta = {
        'collection':'youku_list'
    }
# ================== Youku List END ======================== #