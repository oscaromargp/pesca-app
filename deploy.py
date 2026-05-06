import urllib.request
import json

API_KEY = "rnd_PQcis2kV4ApbBLRxJnsrFXi69zyM"
SERVICE_ID = "srv-d7tdtcreo5us73b9l2tg"

# Trigger deploy
url = f"https://api.render.com/v1/services/{SERVICE_ID}/deploys"
data = json.dumps({"cursor": ""}).encode()

req = urllib.request.Request(url, data=data, method="POST")
req.add_header("Authorization", f"Bearer {API_KEY}")
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.status}")
        print(response.read().decode())
except urllib.error.HTTPError as e:
    print(f"Error: {e.code}")
    print(e.read().decode())