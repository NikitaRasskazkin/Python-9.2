import requests


class YaUploader:
    def __init__(self, file_path: str, token: str):
        self.token = token
        self.file_path = file_path
        self.path = '/*upload_test/'

    def upload(self):
        """Метод загруджает файлы по списку file_list на яндекс диск"""

        def get_upload_data(file_path: str, token: str, path: str):
            """Функция получает данные запроса, в том числе url на загрузку файла"""
            file_name = file_path[file_path.rfind('/') + 1:]
            headers = {'Authorization': token}
            params = {
                'path': f'{path}{file_name}',
                'overwrite': True
            }
            url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
            reply = requests.get(url, params=params, headers=headers)
            return {'reply': reply, 'code': reply.status_code}

        def create_folder(token: str, path: str):
            """Функция создаёт папку, если она ещё не существует"""
            headers = {'Authorization': token}
            params = {'path': path}
            url = 'https://cloud-api.yandex.net/v1/disk/resources'
            reply = requests.put(url, params=params, headers=headers)
            return reply.status_code

        def upload_file(upload_data: dict):
            """Функция загружает файл на Яндекс Диск"""
            upload_url = upload_data['href']
            with open(self.file_path, 'rb') as f:
                reply = requests.put(upload_url, f)
                return reply.status_code // 100 == 2

        create_folder(self.token, self.path)
        reply_data = get_upload_data(self.file_path, self.token, self.path)
        is_upload = False
        if reply_data['code'] // 100 == 2:
            upload_data = reply_data['reply'].json()
            is_upload = upload_file(upload_data)
        if is_upload:
            return 'Файл успешно загружен'
        else:
            return 'Произошла ошибка'


if __name__ == '__main__':
    # Примеры для ввода: files/new_file.txt | files/Python.webp
    token = '*******************'
    file_path = input('Введите путь к файлу: ')
    uploader = YaUploader(file_path, token)
    result = uploader.upload()
    print(result)
