import requests
import pytest


class TestUserAgent:
    user_agent_value = [
        ('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30'
         ' (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        {'platform': 'Mobile', 'browser': 'No', 'device': 'Android'}),
        ('Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
         ' CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1',
        {'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'}),
        ('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        {'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'}),
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
         ' Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0',
        {'platform': 'Web', 'browser': 'Chrome', 'device': 'No'}),
        ('Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15'
         ' (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
         {'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})
    ]

    @pytest.mark.parametrize('user_agent,expected_result', user_agent_value)
    def test_user_agent(self, user_agent, expected_result):
        response = requests.get("https://playground.learnqa.ru/ajax/api/user_agent_check", headers={"User-Agent": user_agent})
        assert response.status_code == 200, "Wrong response code"
        response_dict = response.json()
        for i in expected_result:
            assert i in response_dict, f"There is not User-Agent parameter {i} in response"
            assert response_dict[i] == expected_result[i], f"Value '{i}' is not correct"
