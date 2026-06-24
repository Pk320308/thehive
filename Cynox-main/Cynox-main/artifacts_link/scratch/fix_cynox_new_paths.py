#!/usr/bin/env python3
import os

target_files = [
    r"E:\THE Hive New\auto_backup.ps1",
    r"E:\THE Hive New\backup_cynox.ps1",
    r"E:\THE Hive New\cynox_backup_task.xml",
    r"E:\THE Hive New\cynox_health_task.xml",
    r"E:\THE Hive New\health_monitor.ps1",
    r"E:\THE Hive New\restore_cynox.ps1"
]

print("=== Fixing root paths and db directories ===")

for filepath in target_files:
    if not os.path.exists(filepath):
        print(f"[WARNING] File not found: {filepath}")
        continue
        
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        original_content = content
        
        # 1. Correct root path
        content = content.replace(r"E:\Cynox New", r"E:\THE Hive New")
        content = content.replace(r"E:/Cynox New", r"E:/THE Hive New")
        
        # 2. Correct db directory copy in auto_backup.ps1
        if "auto_backup.ps1" in filepath:
            content = content.replace(r"db_data\thehive", r"db_data\cynox")
            content = content.replace(r"db_data/thehive", r"db_data/cynox")
            content = content.replace(r"$backupDir\thehive", r"$backupDir\cynox")
            content = content.replace(r"$backupDir/thehive", r"$backupDir/cynox")
            
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[FIXED] {filepath}")
        else:
            print(f"[NO CHANGE] {filepath}")
            
    except Exception as e:
        print(f"[ERROR] Failed to fix {filepath}: {e}")

print("=== Fixes completed ===")
