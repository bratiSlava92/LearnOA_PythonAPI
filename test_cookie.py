import requests


class TestCookie:
    def test_cookie(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookie = response.cookies
        print(cookie)
        assert "HomeWork" in cookie, "There isn't cookie 'HomeWork'"
        assert cookie.get("HomeWork") == "hw_value", "Cookie value isn't correct"