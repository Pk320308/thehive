#!/usr/bin/env python3
import os
import shutil
import zipfile
import re
import sys

JAR = "/opt/thehive/lib/org.thp.thehive-frontend-4.1.24-1.jar"
BACKUP = JAR + ".bak"
WORKDIR = "/tmp/frontend_patch"

# Regex for matching thehive case-insensitively
pattern = re.compile(r'the[- ]?hive', re.IGNORECASE)

def preserve_case_replace(match):
    text = match.group(0)
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
        
    if text.isupper():
        return "CYNOX"
    if text.islower():
        return "cynox"
    if text[0].isupper():
        return "Cynox"
    return "cynox"

print("=== Cynox UI Branding Patcher ===")

# Clean workdir
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR)

# Backup original JAR
if not os.path.exists(BACKUP):
    shutil.copy2(JAR, BACKUP)
    print("[OK] Backup of frontend JAR created")

# Extract JAR
with zipfile.ZipFile(JAR, 'r') as z:
    z.extractall(WORKDIR)
print("[OK] Frontend JAR extracted to workdir")

# Replace custom branded images copied from the host to container's /tmp
for img in ["logo.white.svg", "logo.svg", "logo.png"]:
    src = os.path.join("/tmp", img)
    if os.path.exists(src):
        dest = os.path.join(WORKDIR, "frontend", "images", img)
        # Ensure destination directory exists
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(src, dest)
        print(f"[OK] Replaced image: {img}")
    else:
        print(f"[WARNING] Custom image not found in /tmp: {img}")

modified_files = 0

# Walk and replace
for root, dirs, files in os.walk(WORKDIR):
    for file in files:
        ext = os.path.splitext(file)[1].lower()
        if ext not in ['.js', '.html', '.css', '.json', '.xml']:
            continue
            
        filepath = os.path.join(root, file)
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
            
        original_content = content
        
        # Preserve default user domain 'thehive.local'
        content = content.replace("thehive.local", "__THEHIVE_LOCAL_PRESERVE__")
        content = content.replace("THEHIVE.LOCAL", "__THEHIVE_LOCAL_PRESERVE__")
        
        # Apply replacement
        content = pattern.sub(preserve_case_replace, content)
        
        # Restore domain
        content = content.replace("__THEHIVE_LOCAL_PRESERVE__", "thehive.local")
        
        if content != original_content:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                modified_files += 1
            except Exception as e:
                print(f"[ERROR] Failed to write {filepath}: {e}")

print(f"[OK] Rebranded {modified_files} frontend files in workdir")

# Re-create JAR
os.remove(JAR)
with zipfile.ZipFile(JAR, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(WORKDIR):
        for file in files:
            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, WORKDIR)
            zout.write(filepath, arcname)

print("[OK] Re-packaged frontend JAR")
print("=== PATCHING COMPLETE ===")
