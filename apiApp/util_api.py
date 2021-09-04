import json
from datetime import datetime

import requests

from variables import variables


class UtilApi:

    @staticmethod
    def get_comment(video_id: int, page: int, Authorization: str):
        try:
            url = variables().api_get_comment.replace("video_id", str(video_id)).replace("page", str(page))
            headers = {
                'Authorization': Authorization,
                'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, timeout=1)
            if response.status_code == 200:
                data = response.json()['data']
                return data
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def post_new_comment(video_id: int, message: str, Authorization: str):
        try:
            url = variables().api_post_comment
            headers = {
                'Authorization': Authorization,
                'Content-Type': 'application/json'
            }
            payload = {
                "video_id": video_id,
                "message": message
            }
            payload = json.dumps(payload)
            response = requests.request("POST", url, headers=headers, data=payload, timeout=1)
            if response.status_code == 200:
                message = response.json()['data']
                return message
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def post_like_comment(comment_id: int, like: bool, Authorization: str):
        try:
            url = variables().api_post_like_comment
            headers = {
                'Authorization': Authorization,
                'Content-Type': 'application/json'
            }
            payload = {
                "comment_id": comment_id,
                "like": like
            }
            payload = json.dumps(payload)
            response = requests.request("POST", url, headers=headers, data=payload, timeout=1)
            if response.status_code == 200:
                data = response.json()['data']
                return data
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def add_view_count_video(video_id: int, Authorization: str):
        try:
            url = variables().api_add_view_count_video.replace("video_id", str(video_id))
            headers = {
                'Authorization': Authorization,
                'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, timeout=1)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False

    @staticmethod
    def add_view_count_song(song_id: int, Authorization: str):
        try:
            url = variables().api_add_view_count_song.replace("song_id", str(song_id))
            headers = {
                'Authorization': Authorization,
                'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, timeout=1)
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False
