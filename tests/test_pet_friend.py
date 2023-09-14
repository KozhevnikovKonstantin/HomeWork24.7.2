import os

from api import PetFriends
from settings import email, password


pf = PetFriends()
"""Получение апи-ключа по валидному email и паролю: PASSED"""
def test_api_for_valid_user(email = email, password = password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
"""Получение списка питомцев по валидному ключу: PASSED"""
def test_get_all_pets_with_valid_authkey(filter = ''):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0
"""Простое создание записи о питомце по валидному ключу: PASSED"""
def test_create_pet_simple_with_valid_authkey(name = 'Симба', animal_type = 'Лев', age = 10):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert  status == 200
    assert result['name'] == name
"""Успешное удаление записи о питомце: PASSED"""
def test_successful_delete_self_pet():

    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.create_pet_simple(auth_key, "Пумба", "кабан", 12)
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()
"""Создание записи о новом питомце с корректными данными: PASSED"""
def test_add_new_pet_with_valid_data(name='Игорь', animal_type='салат', age=4, pet_photo='images/kisspng-savoy-cabbage-kale-vegetable-brussels-sprout-kale-5a7a563c2f7bb8.6007409015179669081945.png'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(email, password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name
"""Обновление данных о питомце: PASSED"""
def test_successful_update_self_pet_info(name='Сапфира', animal_type='Дракон', age=5):

    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("You should create pet before updating")
"""Добавление фото в запись о питомце:FAILED
Ответ сервера: 500. В причине пока не разобрался"""
def test_successful_add_photo_of_pet(pet_photo = 'images/dragon.png'):
    _, auth_key = pf.get_api_key(email, password)
    _, my_pets = pf.get_list_of_pets(auth_key,"my_pets")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'],pet_photo)

        assert status == 200
        assert result['pet_photo'] == pet_photo
    else:
        raise Exception("You should create pet before set photo")
"""Отказ получения апи-ключа несуществующим пользователем: PASSED"""
def test_api_for_invalid_user(email = email, password = ''):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
"""Отказ создания записи с некорректным типом параметра animal_type: FAILED
Баг приложения"""
def test_create_pet_simple_with_int_as_animaltype(name = 'Симба', animal_type = 404, age = 10):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert  status == 400
"""Отказ создания записи с использованием некорректного апи-ключа: PASSED"""
def test_create_pet_simple_with_invalid_authkey(name = 'Симба', animal_type = 'Лев', age = 10):
    auth_key = {'key': '123'}
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert  status == 403
"""Отказ получения списка всех питомцев по некорректному апи-ключу: PASSED"""
def test_get_all_pets_with_invalid_authkey(filter = 'my_pets'):
    auth_key = {'key': "key"}
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 403
"""Ошибка создания записи питомца без обязательного параметра name: PASSED"""
def test_create_pet_simple_without_name(animal_type = 404, age = 10):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.create_pet_simple_without_name(auth_key, animal_type, age)
    assert  status == 400
"""Ошибка создания записи питомца при использования значения 
некорректного типа для параметра name: FAILED
Баг приложения"""
def test_create_pet_simple_with_bool_as_name(name = True, animal_type = 'Лев', age = 10):
    _, auth_key = pf.get_api_key(email, password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert  status == 400
"""Ошибка создания записи нового питомца без обязательрого параметра photo: PASSED"""
def test_add_new_pet_with_invalid_data(name='Игорь', animal_type='салат', age=4):

    _, auth_key = pf.get_api_key(email, password)

    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    assert status == 400
"""Ошибка создания записи новго питомца с некорректным апи-ключом: PASSED"""
def test_add_new_pet_with_incorrect_authkey(name='Игорь', animal_type='салат', age=4, pet_photo='images/kisspng-savoy-cabbage-kale-vegetable-brussels-sprout-kale-5a7a563c2f7bb8.6007409015179669081945.png'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    auth_key = {'key': "0"}

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 403












