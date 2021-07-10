import requests


class YaUploader:
    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def ya_upload(self, ya_file_path, filename):
        """Метод загруджает файлы по списку vk_json на яндекс диск"""
        ya_path_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = self.get_headers()
        params = {"path": ya_file_path, "overwrite": True}
        response = requests.get(ya_path_url, headers=headers, params=params)
        put_file = requests.put(response.json()['href'], data=open(filename, 'rb'))
        put_file.raise_for_status()
