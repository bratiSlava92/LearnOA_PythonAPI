import requests
import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = requests.post("https://playground.learnqa.ru/api/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

# 1. Создание пользователя с некорректным email - без символа @
    def test_create_user_without_at_in_email(self):
        email = 'mailexample.com'
        data = self.prepare_registration_data(email)

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", "User registered with unexpected email address"

# 2. Создание пользователя без указания одного из полей
    reg_data = [
        ({'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'mail@example.com'}, 'password'),
        ({'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'mail@example.com'}, 'username'),
        ({'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'mail@example.com'}, 'firstName'),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'mail@example.com'}, 'lastName'),
        ({'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'lastName': 'learnqa'}, 'email')
    ]

    @pytest.mark.parametrize('data,missed_data', reg_data)
    def test_create_user_without_parameter(self, data, missed_data):

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missed_data}", \
            f"User didn't register. Required paremeter '{missed_data}' are missed"

# 3. Создание пользователя с очень коротким именем в один символ
    short_names = [
        ({'username': 'A', 'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'mail@example.com'}, 'username'),
        ({'firstName': 'B', 'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'mail@example.com'}, 'firstName'),
        ({'lastName': 'C', 'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'mail@example.com'}, 'lastName')
    ]

    @pytest.mark.parametrize('data, short_name', short_names)
    def test_create_user_with_short_name(self, data, short_name):

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{short_name}' field is too short", f"User registered with short name '{short_name}'"

# 4. Создание пользователя с очень длинным именем - длиннее 250 символов
    long_names = [
        ({'username': '251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols2',
          'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'mail@example.com'}, 'username'),
        ({'firstName': '251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols2',
          'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'mail@example.com'}, 'firstName'),
        ({'lastName': '251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols251Symbols2',
          'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'mail@example.com'}, 'lastName')
    ]

    @pytest.mark.parametrize('data, long_name', long_names)
    def test_create_user_with_long_name(self, data, long_name):

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{long_name}' field is too long", f"User registered with long name'{long_name}'"