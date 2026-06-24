import os

images_dir = r"E:\Cynox New\Cynox-main\Cynox-main\frontend\app\images"
for root, dirs, files in os.walk(images_dir):
    for file in files:
        if 'logo' in file.lower() or 'brand' in file.lower():
            print(os.path.join(root, file))
