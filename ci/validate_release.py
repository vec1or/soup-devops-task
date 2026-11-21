"""Verify the release tag and the metadata of the distributions to publish."""

import argparse
from email import policy
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
import re
import tarfile
import tomllib
from zipfile import ZipFile, BadZipFile


def normalized_name(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def validate_release(tag, pyproject, directory):
    with pyproject.open("rb") as stream:
        project = tomllib.load(stream)["project"]
    name, version = project["name"], project["version"]
    if not re.fullmatch(r"v(?:0|[1-9][0-9]*)(?:\.(?:0|[1-9][0-9]*)){2}", tag):
        raise ValueError(f"Invalid release tag: {tag!r}")
    if tag != f"v{version}":
        raise ValueError(f"Tag {tag} does not match project version {version}")

    entries = list(directory.iterdir())
    wheels = [item for item in entries if item.is_file() and item.suffix == ".whl"]
    sdists = [item for item in entries if item.is_file() and item.name.endswith(".tar.gz")]
    if len(entries) != 2 or len(wheels) != 1 or len(sdists) != 1:
        raise ValueError("Expected exactly one wheel and one source archive")

    with ZipFile(wheels[0]) as wheel:
        candidates = [
            member for member in wheel.namelist()
            if len(PurePosixPath(member).parts) == 2 and member.endswith(".dist-info/METADATA")
        ]
        if len(candidates) != 1:
            raise ValueError("Expected one .dist-info/METADATA in the wheel")
        wheel_metadata = wheel.read(candidates[0])

    with tarfile.open(sdists[0], "r:gz") as sdist:
        candidates = [
            member for member in sdist
            if member.isfile() and len(PurePosixPath(member.name).parts) == 2
            and PurePosixPath(member.name).name == "PKG-INFO"
        ]
        if len(candidates) != 1:
            raise ValueError("Expected one root PKG-INFO in the source archive")
        with sdist.extractfile(candidates[0]) as stream:
            sdist_metadata = stream.read()

    for artifact, raw_metadata in zip([wheels[0], sdists[0]], [wheel_metadata, sdist_metadata]):
        metadata = BytesParser(policy=policy.default).parsebytes(raw_metadata)
        names = metadata.get_all("Name", [])
        if len(names) != 1 or normalized_name(names[0]) != normalized_name(name):
            raise ValueError(f"{artifact.name}: Name does not match {name!r}")
        if metadata.get_all("Version", []) != [version]:
            raise ValueError(f"{artifact.name}: Version does not match {version!r}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag")
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    try:
        validate_release(args.tag, Path("pyproject.toml"), args.directory)
    except (ValueError, OSError, BadZipFile, tarfile.TarError) as exc:
        raise SystemExit(f"Release validation failed: {exc}") from exc
    print(f"Validated wheel and source archive for {args.tag}")


if __name__ == "__main__":
    main()
