import json

import requests

from variables import variables


class UtilApi:
    @staticmethod
    def send_data_new_user(phone_number: str, android_version: int, device_type: str, device_unique_id: str,
                           device_fcm_token: str):
        try:
            url = variables().api_put_verify_user
            payload = {
                "phone_number": phone_number,
                "android_version": android_version,
                "device_type": device_type,
                "unique_id": device_unique_id,
                "fcm_token": device_fcm_token
            }
            payload = json.dumps(payload)
            headers = {'Content-Type': 'application/json'}

            response = requests.request("PUT", url, headers=headers, data=payload)
            if response.status_code == 200:
                data = response.json()['data']
                return data["user_id"], data["device"]
            else:
                return False, False
        except Exception as e:
            # print("Error send new user :", str(e))
            return False, False
