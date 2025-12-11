import urllib.request
import json

url = "http://127.0.0.1:8000/predict"
data = {
    "features": {
        "alcohol": 12.0,
        "volatile_acidity": 0.5
    }
}
jsondata = json.dumps(data).encode("utf-8")

req = urllib.request.Request(url, data=jsondata, headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.getcode()}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
