from django.test import TestCase

from setData.set_data import SetData

from apiApp.models import *

from setData.downloader import Downloader


class CatTest(TestCase):
    def test_category(self):
        category = {
            "category_id": 1,
            "image_link": "1.1.1.1/test",
            "title": "test",
            "update": True
        }
        cat1 = SetData.add_cat(category)
        cat_exist = VideoCategory.objects.get(pk=1)
        self.assert_(cat_exist == cat1[0])
        self.assert_(cat1[1][0]["type"] == "4/1.i")
        Downloader.verify_download(cat1[1][0]["url"], cat1[1][0]["type"])
        cat_exist = VideoCategory.objects.get(pk=1)
        self.assert_(cat_exist.image_link == "192.168.255.252/test", )
        self.assert_(cat_exist.is_active)
        category = {
            "category_id": 1,
            "image_link": "1.1.1.1/test2",
            "title": "test2",
            "update": True
        }
        cat2 = SetData.add_cat(category)
        self.assert_(cat_exist.title != cat2[0].title)
        self.assert_(cat_exist.image_link == cat2[0].image_link)
        self.assert_(cat2[1][0]["type"] == "4/1.u")
        self.assert_(cat2[1][0]["url"] == 'http://1.1.1.1/test2')
        Downloader.verify_download(cat2[1][0]["url"], cat2[1][0]["type"])
        cat_exist2 = VideoCategory.objects.get(pk=1)
        self.assert_(cat_exist2.image_link == "192.168.255.252/test2")

    def test_add_singer(self):
        singer_data = {
            'singer_id': 1,
            'fa_name': 'test',
            'en_name': 'test',
            'image_link': '4.4.4.4/test',
            'is_channel': False,
            'update':True
        }
        set_singer, payload = SetData.add_singer(singer_data)
        check_singer = Singer_Channel.objects.get(singer_id=1)
        self.assert_(set_singer == check_singer, f"{set_singer} is not {check_singer}")
        self.assert_(payload['type'] == '9/1.i', f"payload type is {payload['type']} instead of 9/1.i")
        Downloader.verify_download(payload['url'], payload['type'])
        check_singer = Singer_Channel.objects.get(singer_id=1)
        self.assert_(check_singer.image_link == "192.168.255.252/test", "image url ip didn't change!")
        self.assert_(check_singer.is_active, "download verified but image is not active!")
        singer_data2 = {
            'singer_id': 1,
            'fa_name': 'newtest',
            'en_name': 'newtest',
            'image_link': '4.4.4.4/newtest',
            'is_channel': False,
            "update": True
        }
        set_singer2, payload = SetData.add_singer(singer_data2)
        self.assert_(all(
            [check_singer.en_name != set_singer2.en_name, check_singer.fa_name != set_singer2.fa_name,
             check_singer.image_link == set_singer2.image_link]), "fields did not updated successfully")
        self.assert_(payload["type"] == '9/1.u', f"payload type is {payload['type']} instead of 9/1.u")
        self.assert_(payload["url"] == 'http://4.4.4.4/newtest', f"payload url is {payload['url']} instead of 'http://4.4.4.4/newtest'")
        Downloader.verify_download(payload['url'], payload['type'])
        check_singer2 = Singer_Channel.objects.get(singer_id=1)
        self.assert_(check_singer2.image_link == "192.168.255.252/newtest", "image url ip didn't change!")

