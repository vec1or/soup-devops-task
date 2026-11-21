"""Exercise the release validator with small synthetic archives."""

import io
from pathlib import Path
import tarfile
import tempfile
import unittest
from zipfile import ZipFile

from ci.validate_release import validate_release


class ReleaseValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.project = root / "pyproject.toml"
        self.project.write_text('[project]\nname = "demo-project"\nversion = "0.1.0"\n')
        self.dist = root / "dist"
        self.dist.mkdir()
        self.write_wheel()
        self.write_sdist()

    def write_wheel(self, name="demo_project", version="0.1.0"):
        with ZipFile(self.dist / "demo.whl", "w") as wheel:
            wheel.writestr("demo.dist-info/METADATA", f"Name: {name}\nVersion: {version}\n")

    def write_sdist(self, name="demo-project", version="0.1.0"):
        with tarfile.open(self.dist / "demo.tar.gz", "w:gz") as archive:
            for path, contents in (
                ("demo/src/demo.egg-info/PKG-INFO", b"Name: wrong\nVersion: 9.9.9\n"),
                ("demo/PKG-INFO", f"Name: {name}\nVersion: {version}\n".encode()),
            ):
                member = tarfile.TarInfo(path)
                member.size = len(contents)
                archive.addfile(member, io.BytesIO(contents))

    def test_matching_release_uses_root_pkg_info(self):
        validate_release("v0.1.0", self.project, self.dist)

    def test_invalid_tag(self):
        with self.assertRaisesRegex(ValueError, "Invalid release tag"):
            validate_release("v00.1.0", self.project, self.dist)

    def test_tag_version_mismatch(self):
        with self.assertRaisesRegex(ValueError, "does not match project version"):
            validate_release("v0.2.0", self.project, self.dist)

    def test_artifact_metadata_mismatch(self):
        for writer in (self.write_wheel, self.write_sdist):
            for field, value in (("name", "another-project"), ("version", "0.9.0")):
                with self.subTest(artifact=writer.__name__, field=field):
                    writer(**{field: value})
                    with self.assertRaisesRegex(ValueError, f"{field.title()} does not match"):
                        validate_release("v0.1.0", self.project, self.dist)
                    writer()

    def test_unexpected_file(self):
        (self.dist / "unexpected.whl").touch()
        with self.assertRaisesRegex(ValueError, "Expected exactly"):
            validate_release("v0.1.0", self.project, self.dist)
