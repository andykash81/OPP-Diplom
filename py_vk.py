import requests
import os
from time import sleep
from tqdm import tqdm
from datetime import *
from pprint import pprint


class VkUser:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, ver='5.131'):
        self.params = {
            'access_token': token,
            'v': ver
        }

    def vk_download(self, profile, count, owner_id):
        """Метод выгружает фотографии с VK по owner_id"""
        vk_download_url = self.url + 'photos.get'
        vk_download_params = {
            'owner_id': owner_id,
            'album_id': profile,
            'rev': 1,
            'extended': 1,
            'photo_sizes': 1,
            'count': count
        }
        list_for_download = self._vk_list_for_download(vk_download_url, vk_download_params)
        vk_status = list_for_download
        if vk_status == 5:
            return vk_status
        else:
            os.mkdir('temp')
            list_ = list()
            json_ = dict()
            print('Копирование c VK: ')
            bar = tqdm(unit="B", total=len(list_for_download))
            for photo in list_for_download:
                temp_dict = dict()
                read_f = requests.get(photo['url'])
                name_f = f"{photo['likes_count']}.jpg"
                if os.path.exists(f"temp/{name_f}"):
                    d = datetime.fromtimestamp(photo['date'])
                    date_ = datetime.date(d)
                    name_f = f"{photo['likes_count']}_{date_}.jpg"
                temp_dict['size'] = photo['type']
                temp_dict['file_name'] = name_f
                list_.append(temp_dict)
                with open(f"temp/{name_f}", 'wb') as file:
                    file.write(read_f.content)
                sleep(7)
                bar.update()
            bar.close()
            json_['items'] = list_
            return json_

    def _vk_list_for_download(self, vk_download_url, vk_download_params):
        """Метод формирует список фотографий"""
        vk_info = requests.get(vk_download_url, params={**self.params, **vk_download_params}).json()
        status_key = 'error'
        if status_key in vk_info:
            return vk_info['error']['error_code']
        else:
            photo_items = vk_info['response']['items']
            photo_list = list()
            for items in photo_items:
                temp_dict = dict()
                list_height = []
                temp_dict['id'] = items['id']
                temp_dict['date'] = items['date']
                temp_dict['likes_count'] = items['likes']['count']
                for height in items['sizes']:
                    list_height.append(height['height'])
                max_height = max(list_height)
                for item in items['sizes']:
                    if item['height'] == max_height:
                        temp_dict['type'] = item['type']
                        temp_dict['url'] = item['url']
                photo_list.append(temp_dict)
            return photo_list
