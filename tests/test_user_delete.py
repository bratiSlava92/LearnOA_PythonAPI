import time
from lib.my_requests import MyRequests
from lib.base_case import BaseCase
from lib.assertions import Assertions
import allure


@allure.epic("User deletion cases")
@allure.issue("https://www.atlassian.com/ru/software/jira")
# 1. Первый - на попытку удалить пользователя по ID 2
class TestUserDelete(BaseCase):
    @allure.testcase("1000")
    @allure.description("This test try to delete user with id=2")
    @allure.severity("BLOCKER")
    def test_delete_vinkotov(self):
        # LOGIN
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id = self.get_json_value(response1, "user_id")

        # DELETE
        response2 = MyRequests.delete(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f"User with id {user_id} was deleted"

# 2. Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить,
# затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален
    @allure.testcase("1001")
    @allure.description("This test delete created user")
    @allure.severity("BLOCKER")
    def test_delete_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        password = register_data['password']

        # LOGIN
        login_data = {
            'email': email,
            'password': password
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response2, "user_id")

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid}
                                    )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", f"Found data of deleted user"

        # LOGIN as deleted user
        response5 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response5, 400)
        assert response5.content.decode("utf-8") == "Invalid username/password supplied", f"Deleted user logged in"

# 3. Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем
    @allure.testcase("1002")
    @allure.description("This test try to delete one user being authorized as another user")
    @allure.severity("BLOCKER")
    def test_delete_user_auth_as_another_user(self):
        # CREATE user for auth
        register_test_data = self.prepare_registration_data()
        response = MyRequests.post('/user/', data=register_test_data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id_1st = self.get_json_value(response, "id")

        # REGISTER
        time.sleep(3)
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post('/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email_2nd = register_data['email']
        password_2nd = register_data['password']
        user_id_2nd = self.get_json_value(response1, "id")

        # LOGIN as another User
        login_data = {
            'email': email_2nd,
            'password': password_2nd
        }

        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid_2nd = self.get_cookie(response2, "auth_sid")
        token_2nd = self.get_header(response2, "x-csrf-token")

        # DELETE
        response3 = MyRequests.delete(f"/user/{user_id_1st}",
                                    headers={"x-csrf-token": token_2nd},
                                    cookies={"auth_sid": auth_sid_2nd}
                                    )

        Assertions.assert_code_status(response3, 200)

        # GET
        response4 = MyRequests.get(f"/user/{user_id_1st}")

        Assertions.assert_code_status(response4, 200)

        response5 = MyRequests.get(f"/user/{user_id_2nd}")
        Assertions.assert_code_status(response5, 404)
