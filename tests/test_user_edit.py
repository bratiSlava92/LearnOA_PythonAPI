from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User modification cases")
@allure.issue("https://www.atlassian.com/ru/software/jira")
class TestUserEdit(BaseCase):
    @allure.testcase("01")
    @allure.description("This test edit just registered user")
    @allure.severity("CRITICAL")
    def test_edit_just_created_user(self):
        # REGISTER
        with allure.step("1. Register new user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            email = register_data['email']
            first_name = register_data['firstName']
            password = register_data['password']
            user_id = self.get_json_value(response1, "id")

        # LOGIN
        with allure.step("2. Login as created user"):
            login_data = {
                'email': email,
                'password': password
            }

            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        with allure.step("3. Change first name"):
            new_name = "Changed Name"

            response3 = MyRequests.put(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data={"firstName": new_name}
                                     )

            Assertions.assert_code_status(response3, 200)

        # GET
        with allure.step("4. Check new firstName value "):
            response4 = MyRequests.get(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid}
                                     )
            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                new_name,
                "Wrong name of the user after edit"
            )

# 1. Попытаемся изменить данные пользователя, будучи неавторизованными
    @allure.testcase("02")
    @allure.description("This test try to edit user without authorization")
    @allure.severity("MAJOR")
    def test_edit_user_without_auth(self):
        # REGISTER
        with allure.step("1. Register new user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id = self.get_json_value(response1, "id")

        # EDIT
        with allure.step("2. Edit user without auth and check response"):
            response2 = MyRequests.put(f"/user/{user_id}", data={"firstName": "New Name"})

            Assertions.assert_code_status(response2, 400)
            assert response2.content.decode("utf-8") == f"Auth token not supplied", f"User edited without auth"

# 2. Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    @allure.testcase("03")
    @allure.description("This test edit user being authorized as another user")
    @allure.severity("AVERAGE")
    def test_edit_user_auth_as_another_user(self):
        # REGISTER
        with allure.step("1. Register new user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id = self.get_json_value(response1, "id")
            old_name = register_data["username"]

        # LOGIN as another User
        with allure.step("2. Login as another user"):
            login_data = {
                'email': 'vinkotov@example.com',
                'password': '1234'
            }

            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        with allure.step("3. Edit user name"):
            new_name = "Changed Name"

            response3 = MyRequests.put(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data={"username": new_name}
                                     )

            Assertions.assert_code_status(response3, 400)

        # GET
        with allure.step("4. Check user name didn't change"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid}
                                     )
            Assertions.assert_json_value_by_name(
                response4,
                "username",
                old_name,
                "User was edited by another user"
            )

# 3. Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
    @allure.testcase("04")
    @allure.description("This test try to edit email without @")
    @allure.severity("MINOR")
    def test_edit_user_email(self):
        # REGISTER
        with allure.step("1. Register new user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id = self.get_json_value(response1, "id")
            email = register_data['email']
            password = register_data['password']

        # LOGIN
        with allure.step("2. Login as the same user"):
            login_data = {
                'email': email,
                'password': password
            }

            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        with allure.step("3. Edit email and check response"):
            new_email = "mailexample.com"

            response3 = MyRequests.put(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data={"email": new_email}
                                     )

            Assertions.assert_code_status(response3, 400)
            assert response3.content.decode("utf-8") == "Invalid email format", "User edited with wrong email address"

        # GET
        with allure.step("4. Check email didn't change"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid}
                                     )
            Assertions.assert_json_value_by_name(
                response4,
                "email",
                email,
                "User was edited with wrong email address"
            )

# 4. Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    @allure.testcase("05")
    @allure.description("This test try to edit firstName to 1 symbol value")
    @allure.severity("TRIVIAL")
    def test_edit_user_with_short_name(self):
        # REGISTER
        with allure.step("1. Register new user"):
            register_data = self.prepare_registration_data()
            response1 = MyRequests.post('/user/', data=register_data)

            Assertions.assert_code_status(response1, 200)
            Assertions.assert_json_has_key(response1, "id")

            user_id = self.get_json_value(response1, "id")
            email = register_data['email']
            password = register_data['password']
            old_first_name = register_data['firstName']

        # LOGIN
        with allure.step("2. Login as the same user"):
            login_data = {
                'email': email,
                'password': password
            }

            response2 = MyRequests.post("/user/login", data=login_data)

            auth_sid = self.get_cookie(response2, "auth_sid")
            token = self.get_header(response2, "x-csrf-token")

        # EDIT
        with allure.step("3. Edit firstName to 1 symbol value"):
            new_first_name = "A"

            response3 = MyRequests.put(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid},
                                     data={"firstName": new_first_name}
                                     )

            Assertions.assert_code_status(response3, 400)

        # GET
        with allure.step("4. Check firstName didn't change"):
            response4 = MyRequests.get(f"/user/{user_id}",
                                     headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid}
                                     )
            Assertions.assert_json_value_by_name(
                response4,
                "firstName",
                old_first_name,
                "User was edited with short name"
            )

