import json
import requests
from pathlib import Path

from scripts.a2s import SkinConverter

print("Enter plushie names (blank line to finish):")

names = []
while name := input("> ").strip():
    names.append(name)

base = Path("../assets/plushies/models/plushies")
base.mkdir(parents=True, exist_ok=True)

def write_json(path, data):
    path.write_text(json.dumps(data, separators=(",", ": ")), encoding="utf-8")

for name in names:
    folder = base / name
    folder.mkdir(parents=True, exist_ok=True)

    textures = {"0": f"plushies:item/plushies/{name}"}

    write_json(folder / f"{name}.json", {
        "parent": "plushies:plushies/plush",
        "textures": textures
    })

    write_json(folder / f"{name}.st.json", {
        "parent": "plushies:plushies/plush_statue",
        "textures": textures
    })

out_dir = Path("../assets/plushies/textures/item/plushies")
out_dir.mkdir(exist_ok=True)

for name in names:
    url = f"https://maltsburg.com/skin/{name}"
    r = requests.get(url)

    if r.status_code == 200:
        file_path = str(out_dir / f"{name}.png")
        (out_dir / f"{name}.png").write_bytes(r.content)

        sc = SkinConverter()
        sc.load_from_file(file_path)

        if not sc.is_steve():
            sc.alex_to_steve_stretch()
            sc.save_to_file(file_path)
            print(f"Converted {name}")
        else: print(f"Downloaded {name}")
    else:
        print(f"Failed {name}: {r.status_code}")

print("\n\n".join(
    "\n".join(
        json.dumps({
            "when": when,
            "model": {
                "type": "model",
                "model": model
            }
        }) + ","
        for when, model in [
            (name, f"plushies:plushies/{name}/{name}"),
            (f"{name}.st", f"plushies:plushies/{name}/{name}.st"),
        ]
    )
    for name in names
))

print("\ngood work!")