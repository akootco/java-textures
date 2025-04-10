import os
import zipfile
import requests
# get server icon
def get_icon():
    with open("pack.png", "wb") as f:
        f.write(requests.get(f"https://api.mcstatus.io/v2/icon/akoot.co").content)

get_icon()

# zip everything
def zip_directory(src_dir, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src_dir):
            # exclude the specified folders
            dirs[:] = [d for d in dirs if d not in ['.git', ".idea"] ]

            for file in files:
                # skip files
                if file in {zip_name, 'zip.py'}:
                    continue

                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, src_dir))

zip_directory('./', 'food_pack.zip')