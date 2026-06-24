import urllib.request
import json

candidates = [
    # angular-qr
    "https://unpkg.com/angular-qrcode@1.0.4/angular-qrcode.js",
    "https://unpkg.com/angular-qrcode/angular-qrcode.js",
    "https://cdn.jsdelivr.net/npm/angular-qrcode@1.0.4/angular-qrcode.js",
    
    # smalot-bootstrap-datetimepicker
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/2.4.4/js/bootstrap-datetimepicker.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/2.4.4/css/bootstrap-datetimepicker.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/2.4.4/css/bootstrap-datetimepicker.css",
    "https://cdn.jsdelivr.net/npm/bootstrap-datetimepicker@2.4.4/js/bootstrap-datetimepicker.min.js",
    
    # angular-images-resizer
    "https://unpkg.com/angular-images-resizer@2.0.3/dist/angular-images-resizer.min.js",
    "https://unpkg.com/angular-images-resizer@2.0.3/dist/angular-images-resizer.js",
    "https://unpkg.com/angular-images-resizer@2.0.3/src/angular-images-resizer.js",
    "https://unpkg.com/angular-images-resizer@2.0.3/index.js",
    "https://unpkg.com/angular-images-resizer/dist/angular-images-resizer.js"
]

print("Testing candidates v2:")
for url in candidates:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.getcode() == 200:
                print(f"  [SUCCESS] {url}")
            else:
                print(f"  [FAIL {response.getcode()}] {url}")
    except Exception as e:
        print(f"  [ERROR] {url} -> {e}")
