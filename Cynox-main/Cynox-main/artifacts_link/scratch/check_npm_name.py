import urllib.request
import json

names = ["angular-images-resizer", "angular-image-resizer"]

for name in names:
    url = f"https://unpkg.com/{name}/package.json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"Package: {name}")
            print(f" - Version: {data.get('version')}")
            print(f" - Main: {data.get('main')}")
            print(f" - Repository: {data.get('repository')}")
    except Exception as e:
        print(f"Error for '{name}': {e}")
