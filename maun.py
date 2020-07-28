import requests


class YaUploader:
    def __init__(self, file_path: str, token: str):
        self.token = token
        self.file_path = file_path
        self.file_name = file_path[file_path.rfind('/') + 1:]
        print(self.file_name)

    def upload(self):
        """Метод загруджает файлы по списку file_list на яндекс диск"""
        headers = {'Authorization': self.token}
        params = {'path': f'/{self.file_name}'}
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        upload_data = requests.get(url, params=params, headers=headers).json()
        print(upload_data)
        upload_url = upload_data['href']
        with open(self.file_path, 'rb') as f:
            requests.put(upload_url, f)
        return 'Файл успешно загружен!'


if __name__ == '__main__':
    token = 'AgAAAAAT5t7wAADLW0sZ3dQbGEzNrJPmvs0nLWg'
    file_path = 'files/new_file.txt'
    uploader = YaUploader(file_path, token)
    result = uploader.upload()
