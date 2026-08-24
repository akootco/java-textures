import subprocess
from pathlib import Path
import sys


if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <directory>")
    sys.exit(1)

root = Path(sys.argv[1])

for folder in root.rglob("*"):
    if not folder.is_dir() or folder.name not in ("hurt", "greet"):
        continue

    files = sorted(folder.glob("*.rsd"))

    for index, source in enumerate(files):
        output = folder / f"{folder.name}_{index}.ogg"

        print(f"{source} -> {output}")

        subprocess.run([
            "ffmpeg",
            "-y",
            "-i", str(source),
            str(output)
        ], check=True)