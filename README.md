# Niko for Codex

[简体中文](README.zh-CN.md)

A free, unofficial Niko fan pet for Codex desktop, carrying the sun through your next adventure.

![Niko's idle and jump animations](assets/preview.webp)

The pet includes nine animation states and 16 look directions. Its idle keeps both feet planted, with a complete 220 ms blink in a 6.22-second cycle. Niko jumps with happy closed eyes, an open smile, and moving feet, and occasionally tends to the lightbulb.

## Install

Python 3.10 or newer is all you need for installation:

```sh
git clone https://github.com/Rockdu/niko-codex-pet.git
cd niko-codex-pet
python3 tools/install.py
```

The installer copies the pet to your Codex pets directory and automatically backs up an existing installation. Select **Niko** in Codex afterward. If Niko was already selected, select it again to load the update; the installer does not reload the desktop widget.

For a different Codex home directory, use `python3 tools/install.py --codex-home /path/to/codex-home`. Use `python3 tools/install.py --static` to install the static atlas fallback. The fallback still supplies the regular sprite animation rows, but does not contain the animated atlas's additional idle timing.

This package uses the v2 custom-pet format. Development checks used macOS Codex 26.915.31029; compatibility with every Codex version has not been verified.

## Validate or rebuild

Installation does not need image-processing dependencies. To validate the package or rebuild it from the included source images:

```sh
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 tools/validate.py
```

Building also requires `webpmux`, available on macOS with `brew install webp`:

```sh
python3 tools/build.py --output build
```

The repository contains the ready-to-install files in [`pet/`](pet/), animation sources in [`source/`](source/), and previews in [`assets/`](assets/). The source images and `source/animation.json` are sufficient for the included build tool; image generation is not required to rebuild the package.

## Artwork and licensing

**The original tools and documentation are MIT-licensed. The character artwork is not.** See [LICENSE](LICENSE) for the scope and [ARTWORK-NOTICE.md](ARTWORK-NOTICE.md) for attribution, provenance, and reuse limits.

Niko and OneShot belong to their respective rights holders, including Future Cat LLC. This project is not affiliated with or endorsed by Future Cat, OneShot's publishers, or OpenAI. The artwork was generated with AI and refined through compositing and animation work; it is unofficial fan artwork, not a set of official game sprites.

The artwork is shared here as a free, noncommercial fanwork. A OneShot developer [encouraged noncommercial fanworks in the official 2022 creator AMA](https://www.reddit.com/r/NintendoSwitch/comments/xk77gr/comment/ipclj1i/), but that statement is not an open-source license to the character or project-specific permission. No commercial rights or rights to the underlying OneShot character are granted here.

For bugs, suggestions, or rights-related requests, [open an issue](https://github.com/Rockdu/niko-codex-pet/issues).
