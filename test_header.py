import requests

class TestHeaders:
    def test_header(self):
        response = requests.get("https://playground.learnqa.ru/api/homework_header")
        print(response.headers)
        header = response.headers.get('x-secret-homework-header')
        assert "x-secret-homework-header" in response.headers, "There isn't header 'x-secret-homework-header'"
        assert header == "Some secret value", "Header 'x-secret-homework-header' value is not 'Some secret value'"