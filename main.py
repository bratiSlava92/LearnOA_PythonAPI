import requests

# Ex.4
# response = requests.get("https://playground.learnqa.ru/api/get_text")
# print(response.text)


# Ex.3
# print("Hello from Alina Borlakova!")


# Ex.6 узнать сколько редиректов происходит от изначальной точки назначения до итоговой. И какой URL итоговый.
response = requests.get("https://playground.learnqa.ru/api/long_redirect")
response.history
print(f"Количество редиректов =", len(response.history))
print(f"Конечный URL:", response.url)
