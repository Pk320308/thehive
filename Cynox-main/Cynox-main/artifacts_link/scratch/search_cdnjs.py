import urllib.request
import json

def search(query):
    url = f"https://api.cdnjs.com/libraries?search={query}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"Results for '{query}':")
            for lib in data.get('results', []):
                print(f" - {lib['name']}: {lib['latest']}")
    except Exception as e:
        print(f"Error: {e}")

search("datetimepicker")
search("resizer")
search("images-resizer")
