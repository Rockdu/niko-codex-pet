#!/usr/bin/env python3
"""Validate the bundled Niko atlas and its planted idle animation."""

import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image

REPO = Path(__file__).resolve().parents[1]
SIZE = (1536, 2288)
CELL = (192, 208)
COUNTS = (6, 8, 8, 4, 5, 8, 6, 6, 6, 8, 8)


def validate(package: Path) -> dict:
    manifest = json.loads((package / "pet.json").read_text(encoding="utf-8"))
    assert manifest["id"] == "niko-oneshot", "Unexpected pet id"
    assert manifest["spriteVersionNumber"] == 2, "V2 manifest is required"
    assert manifest["spritesheetPath"] == "spritesheet.webp", "Unexpected atlas path"
    fallback = Image.open(package / "spritesheet-static-fallback.webp").convert("RGBA")
    assert fallback.size == SIZE, "Wrong fallback dimensions"
    for row, count in enumerate(COUNTS):
        for col in range(count):
            alpha = fallback.crop((col * 192, row * 208, (col + 1) * 192, (row + 1) * 208)).getchannel("A")
            assert alpha.getbbox(), f"Empty cell {row},{col}"
    reference_boots = fallback.crop((0, 177, 192, 208)).tobytes()
    reader = Image.open(package / "spritesheet.webp")
    assert reader.size == SIZE, "Wrong atlas dimensions"
    assert reader.n_frames == 16, "Expected sixteen temporal frames"
    durations = []
    for i in range(reader.n_frames):
        reader.seek(i)
        page = reader.convert("RGBA")
        durations.append(reader.info["duration"])
        for col in range(6):
            boots = page.crop((col * 192, 177, (col + 1) * 192, 208)).tobytes()
            assert boots == reference_boots, f"Idle feet moved in page {i}, cell {col}"
        assert page.crop((0, 208, *SIZE)).tobytes() == fallback.crop((0, 208, *SIZE)).tobytes(), f"Non-idle art changed in page {i}"
        assert page.crop((1152, 0, 1536, 208)).tobytes() == fallback.crop((1152, 0, 1536, 208)).tobytes(), "Neutral cell changed"
    expected = [item["duration_ms"] for item in json.loads((REPO / "source/animation.json").read_text())["frames"]]
    assert durations == expected, "Temporal durations differ from editable source"
    assert sum(durations) == 6220, "Unexpected idle loop length"
    return {"ok": True, "dimensions": list(SIZE), "temporal_frames": len(durations), "idle_loop_ms": sum(durations), "fixed_boot_pixels": True, "sha256": hashlib.sha256((package / "spritesheet.webp").read_bytes()).hexdigest()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", nargs="?", type=Path, default=REPO / "pet")
    print(json.dumps(validate(parser.parse_args().package), indent=2))
