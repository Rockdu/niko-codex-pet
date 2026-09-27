"""Installer integration checks use isolated temporary directories."""

import importlib.util
from pathlib import Path
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install", REPO / "tools/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class InstallTest(unittest.TestCase):
    def test_install_idempotence_and_backup(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            target, backup = installer.install(REPO / "pet", home)
            self.assertIsNone(backup)
            for name in installer.FILES:
                self.assertEqual((target / name).read_bytes(), (REPO / "pet" / name).read_bytes())
            self.assertIsNone(installer.install(REPO / "pet", home)[1])
            (target / "spritesheet.webp").write_bytes(b"previous pet")
            (target / "user-note.txt").write_text("keep this")
            target, backup = installer.install(REPO / "pet", home)
            self.assertEqual((backup / "spritesheet.webp").read_bytes(), b"previous pet")
            self.assertEqual((backup / "user-note.txt").read_text(), "keep this")
            self.assertEqual((target / "user-note.txt").read_text(), "keep this")

    def test_static_option(self):
        with tempfile.TemporaryDirectory() as temporary:
            target, _ = installer.install(REPO / "pet", Path(temporary), static=True)
            self.assertEqual((target / "spritesheet.webp").read_bytes(), (REPO / "pet/spritesheet-static-fallback.webp").read_bytes())

    def test_symlink_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            (home / "pets").mkdir()
            elsewhere = home / "elsewhere"
            elsewhere.mkdir()
            (home / "pets/niko-oneshot").symlink_to(elsewhere, target_is_directory=True)
            with self.assertRaises(ValueError):
                installer.install(REPO / "pet", home)
            self.assertEqual(list(elsewhere.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
