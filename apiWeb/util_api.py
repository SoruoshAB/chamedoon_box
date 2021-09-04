import json
from datetime import datetime

import requests

from variables import variables


class UtilApi:

    @staticmethod
    def get_comment(video_id: int, Authorization: str = None):
        try:
            url = variables().api_get_comment_web.replace("video_id", str(video_id))
            headers = {
                # 'Authorization': Authorization,
                'Content-Type': 'application/json'
            }
            response = requests.request("GET", url, headers=headers, timeout=1)
            if response.status_code == 200:
                data = response.json()['data']
                return data
            else:
                return False
        except Exception:
            return False
