import json
import os
import zipfile
import requests
# get server icon
def get_icon():
    with open("pack.png", "wb") as f:
        f.write(requests.get(f"https://api.mcstatus.io/v2/icon/akoot.co").content)

get_icon()

def generate_sound_definitions(folder, output_file):
    sounds = {
        os.path.splitext(f)[0]: {
            "sounds": [{"name": f"plushies:{os.path.splitext(f)[0]}"}]
        }
        for f in os.listdir(folder)
        if f.endswith('.ogg')
    }

    with open(output_file, "w") as f:
        json.dump(sounds, f, indent=2)

# Call it (change folder path if needed)
generate_sound_definitions("assets/plushies/sounds", "assets/plushies/sounds.json")


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