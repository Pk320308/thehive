import os
import re

search_dir = r"E:\THE Hive New"
exclude_dirs = {".git", "db_data", "node_modules", "bower_components"}
exclude_extensions = {".zip", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".jar", ".class"}

# Exact replacements to perform
replacements = [
    # (Regex pattern, replacement string)
    (re.compile(r'\bTheHive\b'), 'Cynox'),
    (re.compile(r'\bthehive\b'), 'cynox'),
    (re.compile(r'\bTHEHIVE\b'), 'CYNOX'),
    (re.compile(r'\bThe Hive\b'), 'Cynox'),
    (re.compile(r'\bthe hive\b'), 'cynox'),
    (re.compile(r'\bTHE HIVE\b'), 'CYNOX')
]

modified_files = 0

for root, dirs, files in os.walk(search_dir):
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in exclude_extensions:
            continue
        
        filepath = os.path.join(root, file)
        
        # Read the file
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
            
        original_content = content
        
        # Safe exceptions for files:
        if file == "docker-compose.yml":
            # Don't touch the image line or volumes that must stay identical
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if "image: thehiveproject" in line:
                    new_lines.append(line)
                elif "/opt/thp/cynox/files" in line:
                    new_lines.append(line)
                elif "/etc/cynox" in line:
                    new_lines.append(line)
                else:
                    # Apply replacements to the line
                    for pattern, rep in replacements:
                        line = pattern.sub(rep, line)
                    new_lines.append(line)
            content = "\n".join(new_lines)
            
        elif file == "application.conf":
            # Don't touch keyspace or index-name to avoid data loss
            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if "keyspace:" in line or "index-name:" in line or "include" in line or "/opt/thp/cynox/files" in line:
                    new_lines.append(line)
                else:
                    for pattern, rep in replacements:
                        line = pattern.sub(rep, line)
                    new_lines.append(line)
            content = "\n".join(new_lines)
            
        else:
            # Apply replacements to the whole content
            for pattern, rep in replacements:
                content = pattern.sub(rep, content)
                
        # Write back if changed
        if content != original_content:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_files += 1
                print(f"Modified: {filepath}")
            except Exception as e:
                print(f"Error writing {filepath}: {e}")

print(f"Finished! Total files modified: {modified_files}")
