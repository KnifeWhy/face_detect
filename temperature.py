import requests

temp = requests.get("https://2269-114-41-49-229.jp.ngrok.io/").text
temp = temp.split("<p>")[1].split("</p>")[0].split(":")[1]
print(temp)
