import urllib.request

urls = [
    "https://cdnjs.cloudflare.com/ajax/libs/smalot-bootstrap-datetimepicker/2.4.4/js/bootstrap-datetimepicker.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/smalot-bootstrap-datetimepicker/2.4.4/css/bootstrap-datetimepicker.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/smalot-bootstrap-datetimepicker/2.4.4/css/bootstrap-datetimepicker.css",
    "https://cdn.jsdelivr.net/gh/FBerthelot/angular-images-resizer@2.0.3/src/angular-images-resizer.js",
    "https://unpkg.com/angular-qrcode/angular-qrcode.js"
]

print("Testing new candidates:")
for url in urls:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            print(f"  [SUCCESS] {response.getcode()} -> {url}")
    except Exception as e:
        print(f"  [FAIL] {url} -> {e}")
