#!/usr/bin/env python3
import os
import shutil
import zipfile
import sys

JAR = "/opt/thehive/lib/org.thp.thehive-frontend-4.1.24-1.jar"
BACKUP = JAR + ".bak"
WORKDIR = "/tmp/frontend_patch"

files_to_copy = [
    "angular.min.js",
    "angular-animate.min.js",
    "angular-sanitize.min.js",
    "angular-cookies.min.js",
    "angular-resource.min.js",
    "angular-touch.min.js",
    "angular-messages.min.js",
    "fontawesome-all.js",
    "fontawesome-v4-shims.js"
]

print("=== Injecting Upgraded Frontend Libraries ===")

# Clean workdir
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR)

# Backup original JAR if backup doesn't exist
if not os.path.exists(BACKUP):
    shutil.copy2(JAR, BACKUP)
    print("[OK] Backup created")

# Extract JAR
with zipfile.ZipFile(JAR, 'r') as z:
    z.extractall(WORKDIR)
print("[OK] JAR extracted")

# Copy the downloaded files into extracted JAR scripts folder
scripts_dir = os.path.join(WORKDIR, "frontend", "scripts")
os.makedirs(scripts_dir, exist_ok=True)

for f in files_to_copy:
    src = os.path.join("/tmp", f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(scripts_dir, f))
        print(f"[OK] Copied {f} to scripts folder")
    else:
        print(f"[ERROR] Source file not found in /tmp: {f}")
        sys.exit(1)

# Find index.html
target_html = None
for root, dirs, files in os.walk(WORKDIR):
    for f in files:
        if f == 'index.html':
            target_html = os.path.join(root, f)
            break

if not target_html:
    print("[ERROR] index.html not found in extracted folder!")
    sys.exit(1)

print(f"[OK] Found index.html: {target_html}")

with open(target_html, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Tag replacement strings
target_str = '<script src="scripts/vendor.78eed977.js"></script>'
replacement_str = """<script src="scripts/vendor.78eed977.js"></script>
<!-- Upgraded AngularJS 1.8.3 Core and Modules -->
<script src="scripts/angular.min.js"></script>
<script src="scripts/angular-animate.min.js"></script>
<script src="scripts/angular-sanitize.min.js"></script>
<script src="scripts/angular-cookies.min.js"></script>
<script src="scripts/angular-resource.min.js"></script>
<script src="scripts/angular-touch.min.js"></script>
<script src="scripts/angular-messages.min.js"></script>
<!-- Upgraded FontAwesome 6 SVG/JS with compatibility shims -->
<script src="scripts/fontawesome-all.js" defer></script>
<script src="scripts/fontawesome-v4-shims.js" defer></script>"""

if "angular.min.js" in content:
    print("[INFO] Upgraded script tags already present in index.html")
else:
    if target_str in content:
        content = content.replace(target_str, replacement_str)
        with open(target_html, 'w', encoding='utf-8') as f:
            f.write(content)
        print("[OK] Injected upgraded script tags into index.html")
    else:
        print("[ERROR] Target vendor script tag not found in index.html!")
        sys.exit(1)

# Rebuild the JAR file
os.remove(JAR)
with zipfile.ZipFile(JAR, 'w', zipfile.ZIP_DEFLATED) as zout:
    for root, dirs, files in os.walk(WORKDIR):
        for file in files:
            filepath = os.path.join(root, file)
            arcname = os.path.relpath(filepath, WORKDIR)
            zout.write(filepath, arcname)

print("[OK] Rebuilt frontend JAR with upgrades successfully")
print("=== UPGRADE COMPLETE ===")
