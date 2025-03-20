import os
import zipfile
import requests
# get server icon
def get_icon():
    with open("pack.png", "wb") as f:
        f.write(requests.get(f"https://api.mcstatus.io/v2/icon/akoot.co").content)

get_icon()

# zip everything
def zip_directory(src_dir, zip_name, exclude_folders=[], exclude_files=[]):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(src_dir):
            # exclude the specified folders
            dirs[:] = [d for d in dirs if d not in exclude_folders]

            for file in files:
                # skip the zip file being created
                if file == zip_name:
                    continue

                if file in exclude_files:
                    continue

                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, src_dir))

folders_to_exclude = ['.git', ".idea"]
files_to_exclude = ['zip.py', 'zip.bat', 'items.csv']

zip_directory('./', 'food_pack.zip', folders_to_exclude, files_to_exclude)