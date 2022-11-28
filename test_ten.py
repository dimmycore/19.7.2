import pytest
from api import PetFriends
from settings import valid_email, valid_password
import os

site = PetFriends()
password = '1234KLmn'
key_auth = 87687645654


def test_invalid_password(email=valid_email, password=password):
    """ проверяем что сервер выдаёт ошибку при неправильном пароле"""
    status, _ = site.get_api_key(email, password)
    assert status == 403


def test_add_new_pet(name='Gabe', animal_type='cheetah', age='3', pet_photo='images/gabe.jpg'):
    """проверяем добавление питомца с корректными данными"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = site.get_api_key(valid_email, valid_password)
    status, result = site.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_negative_age(name='Мухтар', animal_type='немецкая овчарка', age='-5', pet_photo='images/mukhtar.jpg'):
    """ проверяем наличие бага с добавлением питомца с отрицательным возрастом"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = site.get_api_key(valid_email, valid_password)
    status, result = site.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert age in result['age']
    assert int(age) < 0


def test_add_new_invalid_pet(name='Мурзик', animal_type='', age='', pet_photo='images/murzik.jpg'):
    """ проверяем наличие бага с добавлением питомца без данных о типе и возрасте"""
    _, auth_key = site.get_api_key(valid_email, valid_password)
    status, result = site.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert name in result['name']


def test_invalid_key_auth(filter='my_pets'):
    """проверяем ошибку при вводе неправильного ключа авторизации"""
    try:
        auth_key = key_auth
        result = site.get_list_of_pets(auth_key, filter)
        assert result is not filter
        assert auth_key is not key_auth
    except TypeError:
        print('Неверный ключ авторизации')


def test_succesfull_delete_alien_pet():
    """проверяем ошибку с возможностью удаления чужого питомца"""
    _, auth_key = site.get_api_key(valid_email, valid_password)
    _, all_pets = site.get_list_of_pets(auth_key, '')
    print(type(all_pets))
    pet_id = all_pets['pets'][0]['id']
    status, _ = site.delete_pet(auth_key, pet_id)
    _, all_pets = site.get_list_of_pets(auth_key, '')
    assert status == 200
    assert pet_id not in all_pets.values()


def test_update_alien_pet_info(name='Тоша', animal_type='cat', age=2):
    """проверяем ошибку с возможностью изменения данных о чужом питомце"""
    _, auth_key = site.get_api_key(valid_email, valid_password)
    _, all_pets = site.get_list_of_pets(auth_key, '')
    status, result = site.update_pet_info(auth_key, all_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type


def test_add_new_pet_negative(name='ааввапраdrghthtuiy', animal_type='немецкая овчарка', age='5', pet_photo='images/rb.jpeg'):
    """проверяем наличие бага с добавлением питомца с именем состоящим из смешанных символов латиницы и кириллицы"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = site.get_api_key(valid_email, valid_password)
    status, result = site.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert name in result['name']


def test_add_new_pet_over_age(name='Рекс', animal_type='немецкая овчарка', age='100', pet_photo='images/mukhtar.jpg'):
    """проверяем наличие бага с добавлением питомца со слишком большим возрастом"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = site.get_api_key(valid_email, valid_password)
    status, result = site.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert name in result['name']
    assert int(age) > 50


def test_add_photo_for_old_own_pet(pet_photo='images/gosha.jpg'):
    """проверяем добавление фотографии своему уже существующему питомцу"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = site.get_api_key(valid_email, valid_password)
    _, my_pets = site.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = site.add_photo_to_pet(auth_key, my_pets['pets'][-1]['id'], pet_photo)
        assert status == 200
    else:
        raise Exception('There is no my pets')














