import os
import re

search_dir = r"E:\Cynox New\Cynox-main\Cynox-main\frontend\app"
exclude_extensions = {".zip", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".eot"}

occurrences = []

for root, dirs, files in os.walk(search_dir):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in exclude_extensions:
            continue
        filepath = os.path.join(root, file)
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                matches = re.findall(r'(cynox|cynox)', content, re.IGNORECASE)
                if matches:
                    occurrences.append((filepath, len(matches)))
        except Exception as e:
            pass

print(f"Found {len(occurrences)} files in frontend/app with matches:")
for path, count in sorted(occurrences, key=lambda x: x[1], reverse=True):
    print(f"{path}: {count} matches")
