ip_sever = "http://*******.com/api/box"
company_id = "*"


class variables:
    def __init__(self):
        self.ip_box = "*.*.**.*"
        self.api_downloader = "http://*.*.*.*.*:7070/queue"
        self.api_get_comment = ip_sever + "/VideoComments/video_id/page"
        self.api_post_comment = ip_sever + "/VideoComments"
        self.api_post_like_comment = ip_sever + "/VideoCommentLike"
        self.api_get_comment_web = ip_sever + "/VideoCommentsWeb/video_id"
        self.api_put_verify_user = ip_sever + "/VerifyUserServer"
        self.api_add_view_count_video = ip_sever + "/AddViewVidoeCount/video_id"
        self.api_add_view_count_song = ip_sever + "/AddViewSongCount/song_id"
        self.api_get_data = ip_sever + "/get/data/" + company_id
        self.destination_video = "/mnt/files/videos"
        self.destination_image = "/mnt/files/images"
        self.destination_song = "/mnt/files/songs"
