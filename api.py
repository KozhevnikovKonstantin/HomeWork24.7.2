import requests

class PetFriends:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"
    """Получение апи-ключа с валидным мейлом и паролем"""
    def get_api_key(self, email, password):
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers= headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    """Получение списка всех питомцев"""
    def get_list_of_pets(self, auth_key, filter):
        headers = {"auth_key": auth_key['key']}
        filter = {"filter": filter}

        res = requests.get(self.base_url+'api/pets', headers= headers, params= filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    """Простое создания питомца (без фото)"""
    def create_pet_simple(self, auth_key, name, animal_type: str, age):
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url+'api/create_pet_simple', headers=headers,data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    """Метод удаления питомца по его id"""
    def delete_pet(self, auth_key, pet_id):

        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    """Добавление питомца """
    def add_new_pet(self, auth_key, name, animal_type,
                    age, pet_photo):

        data ={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            }
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/png')}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result
    """Обновление информации о питомце"""

    def update_pet_info(self, auth_key, pet_id, name,
                        animal_type, age):

        headers = {'auth_key': auth_key['key']}
        data = {
            'name': name,
            'age': age,
            'animal_type': animal_type
        }

        res = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    """Добавление фото в запись о питомце по id"""

    def add_photo_of_pet(self, auth_key, pet_id, pet_photo):
        headers = {'auth_key': auth_key['key']}
        file = {'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/png')}
        res = requests.post(self.base_url + 'api/pets/set_photo/'+ pet_id, headers=headers, files=file)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result
    """Отправка некорректного запроса на создание питомца (без имени)"""

    def create_pet_simple_without_name(self, auth_key, animal_type: str, age):
        data = {

            'animal_type': animal_type,
            'age': age,

        }
        headers = {'auth_key': auth_key['key']}
        res = requests.post(self.base_url+'api/create_pet_simple', headers=headers,data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        return status, result
    """Отправка некорректоного запроса на создание питомца (без фото)"""

    def add_new_pet_without_photo(self, auth_key, name, animal_type,
                    age):

        data ={
                'name': name,
                'animal_type': animal_type,
                'age': age,
            }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url + 'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result



