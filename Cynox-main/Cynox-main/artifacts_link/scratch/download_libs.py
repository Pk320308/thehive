#!/usr/bin/env python3
import urllib.request
import os

downloads = {
    # AngularJS 1.8.3 (using Google CDN which is highly reliable)
    "angular.min.js": "https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular.min.js",
    "angular-animate.min.js": "https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-animate.min.js",
    "angular-sanitize.min.js": "https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-sanitize.min.js",
    "angular-cookies.min.js": "https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-cookies.min.js",
    "angular-resource.min.js": "https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-resource.min.js",
    "angular-touch.min.js": "https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-touch.min.js",
    "angular-messages.min.js": "https://ajax.googleapis.com/ajax/libs/angularjs/1.8.3/angular-messages.min.js",
    
    # Font Awesome 6 (SVG/JS with v4 shims compatibility)
    "fontawesome-all.js": "https://use.fontawesome.com/releases/v6.5.2/js/all.js",
    "fontawesome-v4-shims.js": "https://use.fontawesome.com/releases/v6.5.2/js/v4-shims.js"
}

dest_dir = r"E:\THE Hive New\Cynox-main\Cynox-main\frontend\app\scripts"

# Create directory if it doesn't exist
os.makedirs(dest_dir, exist_ok=True)

print("=== Downloading updated frontend libraries ===")

for filename, url in downloads.items():
    dest_path = os.path.join(dest_dir, filename)
    print(f"Downloading {filename}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(dest_path, 'wb') as out_file:
            out_file.write(response.read())
        print(f"[OK] Downloaded {filename} successfully")
    except Exception as e:
        print(f"[ERROR] Failed to download {filename}: {e}")

print("=== Download process complete ===")
