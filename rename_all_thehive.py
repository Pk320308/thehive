#!/usr/bin/env python3
import os
import re

search_dir = r"E:\THE Hive New"
exclude_dirs = {".git", "db_data", "node_modules", "bower_components", "BACKUPS"}
exclude_extensions = {".zip", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf", ".eot", ".jar", ".class"}

# Regex pattern for case-insensitive "thehive" or "the hive" or "the-hive"
pattern = re.compile(r'the[- ]?hive', re.IGNORECASE)

# Case preservation mapping function
def preserve_case_replace(match):
    text = match.group(0)
    # Check exact forms
    if text == "TheHive":
        return "Cynox"
    elif text == "thehive":
        return "cynox"
    elif text == "THEHIVE":
        return "CYNOX"
    elif text == "Thehive":
        return "Cynox"
    elif text == "The Hive":
        return "Cynox"
    elif text == "the hive":
        return "cynox"
    elif text == "THE HIVE":
        return "CYNOX"
    elif text == "theHive":
        return "cynox"
    
    # Fallbacks based on casing rules
    if text.isupper():
        return "CYNOX"
    if text.islower():
        return "cynox"
    if text[0].isupper():
        return "Cynox"
    return "cynox"

# Exclusions to prevent breaking the application or database
exclusions = [
    "image: thehiveproject",
    "/etc/thehive",
    "/opt/thp/thehive",
    "db_data/thehive",
    "db_data\\thehive",
    "keyspace: thehive",
    "index-name: thehive",
    "keyspace = thehive",
    "index-name = thehive",
    "thehive.local" # keep default admin user domains intact
]

def should_skip_line(line):
    for exc in exclusions:
        if exc in line:
            return True
    return False

modified_files_count = 0

print("=== Starting Global Content Renaming ===")

# Walk through all files to modify content
for root, dirs, files in os.walk(search_dir):
    # Skip excluded directories
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext in exclude_extensions:
            continue
        
        filepath = os.path.join(root, file)
        
        # Don't modify the rename scripts themselves to avoid recursion / errors
        if "rename_all_thehive.py" in filepath or "rename_thehive.py" in filepath:
            continue
            
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
            
        lines = content.splitlines()
        new_lines = []
        changed = False
        
        for line in lines:
            if should_skip_line(line):
                new_lines.append(line)
            else:
                new_line = pattern.sub(preserve_case_replace, line)
                if new_line != line:
                    changed = True
                new_lines.append(new_line)
                
        if changed:
            try:
                # Re-add trailing newline if it was present
                output_content = "\n".join(new_lines)
                if content.endswith("\n"):
                    output_content += "\n"
                    
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(output_content)
                modified_files_count += 1
                print(f"[MODIFIED CONTENT] {filepath}")
            except Exception as e:
                print(f"[ERROR WRITING] {filepath}: {e}")

print(f"Finished content modifications. Total files modified: {modified_files_count}")

print("\n=== Starting File Renaming ===")
renamed_files_count = 0

# Walk through all files and rename them if they contain "thehive" in their name
for root, dirs, files in os.walk(search_dir, topdown=False):
    # Exclude directories
    dirs[:] = [d for d in dirs if d not in exclude_dirs]
    
    for name in files + dirs:
        if name in exclude_dirs:
            continue
            
        # Match case-insensitive thehive or the_hive or the-hive in filename
        if pattern.search(name):
            old_path = os.path.join(root, name)
            
            # Skip the script itself
            if "rename_all_thehive.py" in old_path or "rename_thehive.py" in old_path:
                continue
                
            new_name = pattern.sub(preserve_case_replace, name)
            new_path = os.path.join(root, new_name)
            
            try:
                os.rename(old_path, new_path)
                renamed_files_count += 1
                print(f"[RENAMED FILE] {old_path} -> {new_path}")
            except Exception as e:
                print(f"[ERROR RENAMING] {old_path}: {e}")

print(f"Finished file renaming. Total files/folders renamed: {renamed_files_count}")
print("=== GLOBAL RENAMING COMPLETE ===")
