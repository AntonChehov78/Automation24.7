from api import PetFriends
from settings import valid_email, valid_password, incorrect_email, incorrect_password, empty_auth_key, incorrect_animal_type
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Запрос api ключа возвращает статус 200 и в результате содержится слово key"""
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """ Запрос всех питомцев возвращает не пустой список.
    Получение api ключа и сохранение в переменную auth_key. Далее используя этого ключ
    запрос списка всех питомцев и проверка, что список не пустой.
    Доступно значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Добавить питомца с корректными данными"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Обновление информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Еслди список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

# Тест 1
#Нет возможности авторизироваться с пустыми полями
def test_api_key_with_not_email_password(email='', password=''):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# Тест 2
# Нет возможности авторизоваться при неверном логине
def test_get_api_key_for_invalid_user_email(email=incorrect_email, password=valid_password):
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

# Тест 3
# Нет возможности авторизоваться при неверном пароле
def test_get_api_key_for_invalid_user_password(email=valid_email, password = incorrect_password):
    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)
    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

# Тест 4
#Добавление питомца с отрицательным возрастом. БАГ!!!
def test_add_new_pet_with_negative_age(name='Кузя', animal_type='Британец', age='-150', pet_photo='images/cat.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

# Тест 5
#Добавление питомца с возрастом больше возможного для животного(больше 250). БАГ!!!
def test_add_new_pet_with_too_old_age(name='Конь', animal_type='Дворовый',
                                       age='1000000', pet_photo='images/cat.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

# Тест 6
#Нет возможности удалить питомца без указания ID
def test_try_unsuccessful_delete_empty_pet_id():
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Указываем значение id
    pet_id = ''
    # Пробуем удалить питомца с пустым id
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400 or 404

# Тест 7
# Запрос списка питомцев с пустым API возвращает статус 403
def test_get_all_pets_with_empty_key(filter=''):
    # Запрос полного списка питомцев
    status, result = pf.get_list_of_pets(empty_auth_key, filter)
    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 403

# Тест 8
#Добавления питомца без фото, с корректными данными
def test_add_new_pet_without_photo_with_valid_data(name='Эд', animal_type='Гиена', age='15'):
    # Запрос API-ключа
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавление нового питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# Тест 9
#Добавления питомца с некорректным видом (цифровые символы). БАГ!!!
def test_add_new_pet_with_incorrect_animal_type(name='Кузя', animal_type=incorrect_animal_type, age='15', pet_photo='images/cat.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# Тест 10
# Добавления питомца с пустыми полями(кроме фото). БАГ!!!
def test_add_new_pet_with_incorrect_animal_type(name='', animal_type='', age='', pet_photo='images/cat.jpg'):
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name




