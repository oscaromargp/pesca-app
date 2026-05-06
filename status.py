import urllib.request
import json

API_KEY = "rnd_PQcis2kV4ApbBLRxJnsrFXi69zyM"
SERVICE_ID = "srv-d7tdtcreo5us73b9l2tg"

# Get service details
url = f"https://api.render.com/v1/services/{SERVICE_ID}"

req = urllib.request.Request(url)
req.add_header("Authorization", f"Bearer {API_KEY}")

try:
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        s = data.get('service', {})
        print(f"Name: {s.get('name')}")
        print(f"Status: {s.get('status')}")
        print(f"Created: {s.get('createdAt')}")
        print(f"Dashboard: {s.get('dashboardUrl')}")
        print(f"Repo: {s.get('repo')}")
        print(f"Env: {s.get('env')}")
except Exception as e:
    print(f"Error: {e}")