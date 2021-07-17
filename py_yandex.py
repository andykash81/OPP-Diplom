import requests


class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def ya_folder_create(self, folder_name):
        """Метод создает папку на яндекс диске"""
        ya_folder_url = "https://cloud-api.yandex.net/v1/disk/resources"
        headers = self.get_headers()
        params = {"path": folder_name}
        response = requests.get(ya_folder_url, headers=headers, params=params).status_code
        if response == 404:
            requests.put(ya_folder_url, headers=headers, params=params)
        elif response == 401:
            print('Неверный ключ авторизации')
            return response
        elif response == 503:
            print('Сервис временно недоступен')
            return response

    def ya_upload(self, ya_file_path, filename):
        """Метод загруджает файлы по списку на яндекс диск"""
        ya_path_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": ya_file_path, "overwrite": True}
        response = requests.get(ya_path_url, headers=headers, params=params)
        put_file = requests.put(response.json()['href'], data=open(filename, 'rb'))
        put_file.raise_for_status()
