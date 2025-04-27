import json
import os
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