import requests

res = requests.get("http://127.0.0.1:5000/stores")
data = res.json()
store = data["stores"][0]["name"]
print(store)
#items = data["items"]

#for item in items:
#    print(item["name"], " : ", item["price"])
