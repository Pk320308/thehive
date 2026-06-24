import os

search_dir = r"E:\Cynox New\Cynox-main\Cynox-main\frontend\app"

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith('.html') or file.endswith('.js'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'AGPL' in content or '2016-2021' in content:
                        print(f"Match: {filepath}")
                        # Print matching lines
                        lines = content.splitlines()
                        for idx, line in enumerate(lines):
                            if 'AGPL' in line or '2016-2021' in line:
                                print(f"  Line {idx+1}: {line.strip()}")
            except Exception:
                pass
