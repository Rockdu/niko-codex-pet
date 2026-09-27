#!/usr/bin/env python3
"""Rebuild the atlas from editable source frames without changing their pixels."""

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from PIL import Image

REPO = Path(__file__).resolve().parents[1]


def build(output: Path, webpmux: str) -> None:
    plan = json.loads((REPO / "source/animation.json").read_text(encoding="utf-8"))
    base = Image.open(REPO / "source/atlas.webp").convert("RGBA")
    assert base.size == tuple(plan["atlas_size"]) == (1536, 2288)
    output.mkdir(parents=True, exist_ok=True)
    expected = []
    with tempfile.TemporaryDirectory(prefix="niko-build-") as temporary:
        mux = [webpmux]
        for i, frame in enumerate(plan["frames"]):
            cell = Image.open(REPO / "source" / frame["file"]).convert("RGBA")
            assert cell.size == tuple(plan["cell_size"]) == (192, 208)
            page = base.copy()
            for col in range(plan["idle_columns"]):
                page.paste(cell, (col * 192, 0))
            expected.append(page)
            encoded = page if i == 0 else page.crop((0, 0, 1152, 208))
            path = Path(temporary) / f"{i:02d}.webp"
            encoded.save(path, lossless=True, quality=100, method=6, exact=True)
            mux.extend(["-frame", str(path), f'+{frame["duration_ms"]}+0+0+0-b'])
        target = output / "spritesheet.webp"
        mux.extend(["-loop", "0", "-bgcolor", "0,0,0,0", "-o", str(target)])
        subprocess.run(mux, check=True)
    actual = Image.open(target)
    assert actual.n_frames == len(expected)
    for i, wanted in enumerate(expected):
        actual.seek(i)
        decoded = actual.convert("RGBA")
        assert decoded.tobytes() == wanted.tobytes(), f"RGBA mismatch in page {i}"
        assert actual.info["duration"] == plan["frames"][i]["duration_ms"]
    shutil.copy2(REPO / "source/atlas.webp", output / "spritesheet-static-fallback.webp")
    shutil.copy2(REPO / "pet/pet.json", output / "pet.json")
    print(f"Built and verified {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=REPO / "dist/niko-oneshot")
    parser.add_argument("--webpmux", default="webpmux")
    args = parser.parse_args()
    executable = shutil.which(args.webpmux)
    if not executable:
        parser.error("webpmux is required (macOS: brew install webp)")
    build(args.output, executable)
