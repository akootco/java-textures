from pathlib import Path
from scripts.a2s import SkinConverter

BASE_DIR = Path("../assets/plushies/textures/item/plushies")

print("Enter skin names (blank line to finish):")

while True:
    name = input("> ").strip()

    if not name:
        break

    file_path = BASE_DIR / f"{name}.png"

    if not file_path.is_file():
        print(f"File not found: {file_path}")
        continue

    try:
        sc = SkinConverter()
        sc.load_from_file(str(file_path))

        if not sc.is_steve():
            sc.alex_to_steve_stretch()
            sc.save_to_file(str(file_path))
            print(f"converted: {name}.png")
        else:
            print(f"ts already wide gng: {name}.png")

    except Exception as e:
        print(f"failed to convert {name}: {e}")

print("\ngoodnight!!")