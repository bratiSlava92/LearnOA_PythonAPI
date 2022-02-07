import requests

# Ex.4
# response = requests.get("https://playground.learnqa.ru/api/get_text")
# print(response.text)


# Ex.3
# print("Hello from Alina Borlakova!")


# Ex.6 узнать сколько редиректов происходит от изначальной точки назначения до итоговой. И какой URL итоговый.
# response = requests.get("https://playground.learnqa.ru/api/long_redirect")
# response.history
# print(f"Количество редиректов =", len(response.history))
# print(f"Конечный URL:", response.url)


# Ex.7
url = "https://playground.learnqa.ru/ajax/api/compare_query_type"

# 7.1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response = requests.get(url)
print("Result for request without method:", response.status_code, response.text)


# 7.2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response = requests.head(url)
print("Result for request out of list:", response.status_code, response.text)


# 7.3. Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
response = requests.get(url, params={"method": "GET"})
print("Result for request type matches parameter value:", response.status_code, response.text)


# 7.4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# method_list = ["get", "post", "put", "delete"]
param_value = ["GET", "POST", "PUT", "DELETE"]
for i in param_value:
    print("Result for", i, "requests:")
    response = requests.get(url, params={"method": i})
    print("Method GET", response.status_code, response.text)
    response = requests.post(url, data={"method": i})
    print("Method POST", response.status_code, response.text)
    response = requests.put(url, data={"method": i})
    print("Method PUT", response.status_code, response.text)
    response = requests.delete(url, data={"method": i})
    print("Method DELETE", response.status_code, response.text)
    print()
