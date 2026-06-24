import os

search_dir = r"E:\Cynox New\Cynox-main\Cynox-main\frontend\app"

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'Cynox Project' in content or 'CynoxProject' in content:
                        print(f"Match: {filepath}")
            except Exception:
                pass
