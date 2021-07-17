import shutil
from py_vk import VkUser
from py_yandex import YaUploader
from py_ok import OkUser
from pprint import pprint
from tqdm import tqdm


def vk(token):
    owner_id = input('Введите id пользователя VK: ')
    count = input('Введите количество фотографий:  ')
    vk_user1 = VkUser(token)
    vk_j = vk_user1.vk_download('profile', count, owner_id)
    if vk_j == 5:
        return vk_j
    else:
        return vk_j


def ya_uploader(json_):
    ya_token = input('Введите токен для загрузки на Яндекс Диск:  ')
    ya_folder = input('Введите название папки для загрузки на Яндекс Диск:  ')
    ya_user1 = YaUploader(ya_token)
    ya_status = ya_user1.ya_folder_create(ya_folder)
    if ya_status == 401:
        pass
    elif ya_status == 503:
        pass
    else:
        print('Копирование на Яндекс Диск: ')
        bar = tqdm(unit="B", total=len(json_['items']))
        for name_f in json_['items']:
            ya_name = f"{ya_folder}/{name_f['file_name']}"
            temp_name = f"temp/{name_f['file_name']}"
            ya_user1.ya_upload(ya_name, temp_name)
            bar.update()
        bar.close()
    shutil.rmtree('temp/')


if __name__ == '__main__':
    while True:
        command = input('Откуда копировать фотографии(OK или VK)? Для выхода нажмите q:  ')
        if command.lower() == 'q':
            break
        if command.lower() == 'vk':
            with open("vk_token.txt", "r") as vk_f:
                vk_token = vk_f.readline().strip()
            vk_json = vk(vk_token)
            if vk_json == 5:
                print('Авторизация пользователя не удалась.')
                pass
            else:
                ya_uploader(vk_json)
                pprint(vk_json)
        if command.lower() == 'ok':
            with open('ok_token.txt', 'r') as file:
                access_token = file.readline().strip()
                session_secret_key = file.readline().strip()
            ok_user = OkUser(fid='38179506084', count='30')
            ok_j = ok_user.ok_download(session_secret_key, access_token)
            if ok_j == 103:
                print('Авторизация пользователя не удалась.')
                pass
            else:
                ya_uploader(ok_j)
                pprint(ok_j)




