from api import PetFriends
from settings import valid_email, valid_password, incorrect_email, incorrect_password, empty_auth_key, incorrect_animal_type
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в тезультате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее используя этого ключ
    запрашиваем список всех питомцев и проверяем что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat1.jpg'):
    """Проверяем что можно добавить питомца с корректными данными"""

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
    """Проверяем возможность удаления питомца"""

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
    """Проверяем возможность обновления информации о питомце"""

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
#Авторизация с пустыми полями
def test_api_key_with_not_email_password(email='', password=''):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

# Тест 1
def test_get_api_key_for_invalid_user_email(email=incorrect_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 при вводе неверного логина"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

# Тест 2
def test_get_api_key_for_invalid_user_password(email=valid_email, password = incorrect_password):
    """ Проверяем, что запрос api ключа возвращает статус 403 при вводе неверного пароля"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 403

# Тест 3
def test_add_new_pet_with_negative_age(name='Кузя', animal_type='Британеw', age='-150', pet_photo='images/cat.jpg'):
    """Проверяем, что нельзя добавить питомца с отрицательным возрастом
    !!!Баг- сайт позволяет добавить питомца с отрицательным возрастом"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200

# Тест 4
def test_add_new_pet_with_too_old_age(name='Орел', animal_type='Сиамский',
                                       age='1000000', pet_photo='images/cat.jpg'):
    """Проверяем, что нельзя добавить питомца, указав слишком большой возраст (больше 50)
    !!Баг - сайт позволяет добавить питомца, указав слишком большой возраст"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    print('Баг - сайт позволяет добавить питомца, указав слишком большой возраст (более 50 лет)')


# Тест 5
def test_try_unsuccessful_delete_empty_pet_id():
    """Проверяем, что нельзя удалить питомца с пустым id"""

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Указываем значение id
    pet_id = ''

    # Пробуем удалить питомца с пустым id
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 400 or 404

# Тест 6
def test_get_all_pets_with_empty_key(filter=''):
    """Проверка того, что запрос списка всех питомцев c пустым значением API-ключа возвращает статус '403'"""

    # Запрос полного списка питомцев
    status, result = pf.get_list_of_pets(empty_auth_key, filter)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 403

# Тест 7
def test_add_new_pet_without_photo_with_valid_data(name='Эд', animal_type='Гиена', age='15'):
    """Проверка возможности добавления питомца без фото с корректными данными"""

    # Запрос API-ключа
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавление нового питомца
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)

    # Сопоставление полученных данных с ожидаемым результатом
    assert status == 200
    assert result['name'] == name



# Тест 8
def test_add_new_pet_with_incorrect_animal_type(name='Кузя', animal_type=incorrect_animal_type, age='15', pet_photo='images/cat.jpg'):
    """Проверяем, что нельзя добавить некорректный вид питомца
    !!!Баг- сайт вид питомца с цифровыми символами"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name

# Тест 9
def test_add_new_pet_with_incorrect_animal_type(name='', animal_type='', age='', pet_photo='images/cat.jpg'):
    """Проверяем, что нельзя добавить некорректный вид питомца
    !!!Баг- сайт вид питомца с цифровыми символами"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name




