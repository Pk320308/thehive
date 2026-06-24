import os
import re

search_dir = r"E:\Cynox New\Cynox-main\Cynox-main\frontend\app"

for root, dirs, files in os.walk(search_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'Cynox' in content or 'Cynox' in content or 'cynox' in content:
                        print(f"Match in HTML: {filepath}")
                        # Print lines containing matches
                        lines = content.splitlines()
                        for i, line in enumerate(lines):
                            if any(x in line for x in ['Cynox', 'Cynox', 'cynox']):
                                print(f"  Line {i+1}: {line.strip()}")
            except Exception:
                pass
