import urllib.request
import json
import time

API_KEY = "rnd_PQcis2kV4ApbBLRxJnsrFXi69zyM"
SERVICE_ID = "srv-d7tdtcreo5us73b9l2tg"

# Check deploy status
url = f"https://api.render.com/v1/services/{SERVICE_ID}/deploys?limit=1"

req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {API_KEY}")

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print(json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"Error: {e.code}")