import urllib.request
import json

API_KEY = "rnd_PQcis2kV4ApbBLRxJnsrFXi69zyM"
SERVICE_ID = "srv-d7tdtcreo5us73b9l2tg"

# Force cancel and restart
# First, stop the service
url = f"https://api.render.com/v1/services/{SERVICE_ID}/stop"
req = urllib.request.Request(url, data=b"{}", method="POST")
req.add_header("Authorization", f"Bearer {API_KEY}")
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req) as response:
        print("Stop:", response.status, response.read().decode())
except Exception as e:
    print("Stop error:", e)

# Then start again
url = f"https://api.render.com/v1/services/{SERVICE_ID}/start"
req = urllib.request.Request(url, data=b"{}", method="POST")
req.add_header("Authorization", f"Bearer {API_KEY}")
req.add_header("Content-Type", "application/json")

try:
    with urllib.request.urlopen(req) as response:
        print("Start:", response.status, response.read().decode())
except Exception as e:
    print("Start error:", e)