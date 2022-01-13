import requests
import json

url = "http://34.124.166.150:22014/recomm"
url = "http://localhost:22014/recomm"

res = requests.post(url, params={
    "sep": "-",
    "thisBendom": "1-0-1-0-0-1-1-1-1-0-0-0-1-1-1",
    "rattingStrs": "青椒也太難吃-番茄超級好吃"
}
).text

res = json.loads(res)
print(res)
