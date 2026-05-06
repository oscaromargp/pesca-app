import urllib.request
import json

API_KEY = "rnd_PQcis2kV4ApbBLRxJnsrFXi69zyM"
SERVICE_ID = "srv-d7tdtcreo5us73b9l2tg"

# Get live logs
url = f"https://api.render.com/v1/services/{SERVICE_ID}/logs?limit=50"

req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {API_KEY}")

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        for log in data.get('logs', []):
            print(f"[{log.get('timestamp')}] {log.get('message')}")
except Exception as e:
    print(f"Error: {e}")