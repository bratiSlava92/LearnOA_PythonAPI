import pytest
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("Registration cases")
@allure.issue("https://www.atlassian.com/ru/software/jira")
class TestUserRegister(BaseCase):
    @allure.testcase("100")
    @allure.description("This test successfully register user")
    @allure.severity("BLOCKER")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    @allure.testcase("101")
    @allure.description("This test try to register user with existing email")
    @allure.severity("CRITICAL")
    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"

# 1. Создание пользователя с некорректным email - без символа @
    @allure.testcase("102")
    @allure.description("This test try to register user with wrong email")
    @allure.severity("MAJOR")
    def test_create_user_without_at_in_email(self):
        email = 'mailexample.com'
        data = self.prepare_registration_data(email)

        response = MyRequests.post('/user/', data=data)

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

    @allure.testcase("103")
    @allure.description("This test try to register user without one of required parameter")
    @allure.severity("AVERAGE")
    @pytest.mark.parametrize('data,missed_data', reg_data)
    def test_create_user_without_parameter(self, data, missed_data):

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {missed_data}", \
            f"User didn't register. Required paremeter '{missed_data}' are missed"

# 3. Создание пользователя с очень коротким именем в один символ
    short_names = [
        ({'username': 'A', 'password': '123', 'firstName': 'learnqa', 'lastName': 'learnqa', 'email': 'mail@example.com'}, 'username'),
        ({'firstName': 'B', 'password': '123', 'username': 'learnqa', 'lastName': 'learnqa', 'email': 'mail@example.com'}, 'firstName'),
        ({'lastName': 'C', 'password': '123', 'username': 'learnqa', 'firstName': 'learnqa', 'email': 'mail@example.com'}, 'lastName')
    ]

    @allure.testcase("104")
    @allure.description("This test try to register user with too short name")
    @allure.severity("MINOR")
    @pytest.mark.parametrize('data, short_name', short_names)
    def test_create_user_with_short_name(self, data, short_name):

        response = MyRequests.post('/user/', data=data)

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

    @allure.testcase("105")
    @allure.description("This test try to register user with too long name")
    @allure.severity("TRIVIAL")
    @pytest.mark.parametrize('data, long_name', long_names)
    def test_create_user_with_long_name(self, data, long_name):

        response = MyRequests.post('/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The value of '{long_name}' field is too long", f"User registered with long name'{long_name}'"