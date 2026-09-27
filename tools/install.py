#!/usr/bin/env python3
"""Install the bundled pet using only the Python standard library."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import tempfile

REPO = Path(__file__).resolve().parents[1]
FILES = ("pet.json", "spritesheet.webp", "spritesheet-static-fallback.webp")


def install(package: Path, codex_home: Path, static: bool = False) -> tuple[Path, Path | None]:
    manifest = json.loads((package / "pet.json").read_text(encoding="utf-8"))
    pet_id = manifest["id"]
    if pet_id != "niko-oneshot" or manifest.get("spriteVersionNumber") != 2:
        raise ValueError("Expected the Niko v2 pet package")
    if manifest.get("spritesheetPath") != "spritesheet.webp":
        raise ValueError("Unexpected spritesheet path")
    data = {name: (package / name).read_bytes() for name in FILES}
    if static:
        data["spritesheet.webp"] = data["spritesheet-static-fallback.webp"]
    pets = codex_home.expanduser() / "pets"
    pets.mkdir(parents=True, exist_ok=True)
    target = pets / pet_id
    if target.is_symlink():
        raise ValueError(f"Refusing to replace a symlink: {target}")
    if target.exists() and not target.is_dir():
        raise ValueError(f"Expected a directory: {target}")
    if target.exists() and all((target / n).is_file() and (target / n).read_bytes() == b for n, b in data.items()):
        return target, None
    backup = None
    if target.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup = pets / f"{pet_id}.backup-{stamp}"
        shutil.copytree(target, backup)
    target.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".niko-install-", dir=pets) as temporary:
        stage = Path(temporary)
        for name, content in data.items():
            (stage / name).write_bytes(content)
        # The atlas is switched last; backups preserve the previous package.
        for name in ("pet.json", "spritesheet-static-fallback.webp", "spritesheet.webp"):
            os.replace(stage / name, target / name)
    for name, content in data.items():
        if (target / name).read_bytes() != content:
            raise OSError(f"Installed file verification failed: {name}")
    return target, backup


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex-home", type=Path, default=Path(os.environ.get("CODEX_HOME", "~/.codex")))
    parser.add_argument("--static", action="store_true", help="Use the static atlas instead of intrinsic WebP animation")
    args = parser.parse_args()
    target, backup = install(REPO / "pet", args.codex_home, args.static)
    print(f"Installed Niko: {target}")
    if backup:
        print(f"Previous pet backed up to: {backup}")
    print("Select Niko again in Codex to reload the spritesheet.")


if __name__ == "__main__":
    main()
