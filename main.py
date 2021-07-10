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
    return vk_j


def ya_uploader(json_, com):
    ya_token = input('Введите токен для загрузки на Яндекс Диск:  ')
    ya_user1 = YaUploader(ya_token)
    print('Копирование на Яндекс Диск: ')
    bar = tqdm(unit="B", total=len(json_['items']))
    if com == 'vk':
        for name_f in json_['items']:
            ya_name = f"VK_Photo/{name_f['file_name']}"
            temp_name = f"temp/{name_f['file_name']}"
            ya_user1.ya_upload(ya_name, temp_name)
            bar.update()
    elif com == 'ok':
        for name_f in json_['items']:
            ya_name = f"OK_Photo/{name_f['file_name']}"
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
        try:
            if command.lower() == 'vk':
                with open("vk_token.txt", "r") as vk_f:
                    vk_token = vk_f.readline().strip()
                vk_json = vk(vk_token)
                ya_uploader(vk_json, command.lower())
                pprint(vk_json)
            if command.lower() == 'ok':
                with open('ok_token.txt', 'r') as file:
                    access_token = file.readline().strip()
                    session_secret_key = file.readline().strip()
                ok_user = OkUser(fid='38179506084', count='30')
                ok_j = ok_user.ok_download(session_secret_key, access_token)
                ya_uploader(ok_j, command.lower())
                pprint(ok_j)
        except (KeyError, FileExistsError) as errors:
            print('Введено неверное значение ключа!')
            shutil.rmtree('temp/')
            continue
