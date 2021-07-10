import os
import hashlib
import requests
from datetime import *
from time import sleep
from tqdm import tqdm


def _datetime_from_millis(millis, epoch=datetime(1970, 1, 1)):
    """Преобразует время в миллисекундах в дату создания фотографии"""
    date_ = epoch + timedelta(milliseconds=millis)
    date_photo = datetime.date(date_)
    return date_photo


class OkUser:
    ok_url = 'https://api.ok.ru/fb.do?'

    def __init__(self, fid, count):
        self.params = {
            'application_key': 'COCFNEKGDIHBABABA',
            'count': count,
            'detectTotalCount': 'true',
            'fid': fid,
            'fields': 'photo.LIKE_COUNT, photo.pic_max, photo.CREATED_MS',
            'format': 'json',
            'method': 'photos.getPhotos'
        }

    def __ok_sig_access(self, session_secret_key):
        str_ = ''.join('='.join((key, val)) for (key, val) in self.params.items()) + session_secret_key
        sig = hashlib.md5(str_.encode('utf-8')).hexdigest()
        return sig

    def _ok_request_json(self, session_secret_key, access_token):
        sig = self.__ok_sig_access(session_secret_key)
        params_req = {
            'sig': sig,
            'access_token': access_token
        }
        ok_request = requests.get(self.ok_url, params={**self.params, **params_req}).json()
        return ok_request['photos']

    def ok_download(self, session_secret_key, access_token):
        photo_json = self._ok_request_json(session_secret_key, access_token)
        os.mkdir('temp')
        list_ = list()
        json_ = dict()
        print('Копирование c OK: ')
        bar = tqdm(unit="B", total=len(photo_json))
        for items in photo_json:
            temp_dict = dict()
            read_photo = requests.get(items['pic_max'])
            date_create = items['created_ms']
            name_photo = f"{items['like_count']}.jpg"
            if os.path.exists(f"temp/{name_photo}"):
                date_photo = _datetime_from_millis(date_create)
                name_photo = f"{name_photo}_{date_photo}.jpg"
            temp_dict['created_ms'] = date_create
            temp_dict['file_name'] = name_photo
            list_.append(temp_dict)
            with open(f"temp/{name_photo}", 'wb') as file:
                file.write(read_photo.content)
            sleep(3)
            bar.update()
        bar.close()
        json_['items'] = list_
        return json_
