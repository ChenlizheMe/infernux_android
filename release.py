"""Build this repository's standalone InxPackage and GitHub release manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from runpy import run_path

import package


def _require_native_payloads(root: Path) -> None:
    player = root / "package/editor/infernux_android/player"
    libraries = run_path(str(player.parent / "native_payload.py"))["NATIVE_LIBRARIES"]
    for abi, machine in (("arm64-v8a", 183), ("x86_64", 62)):
        directory = player / abi
        manifest = json.loads((directory / "Player.inxmanifest").read_text(encoding="utf-8"))
        expected = {"engine_version": "0.4.0", "platform": "android", "abi": abi,
                    "python_abi": "cp313", "minimum_api": 26, "configuration": "Release"}
        if not isinstance(manifest, dict) or any(manifest.get(k) != v for k, v in expected.items()):
            raise ValueError(f"Android {abi} payload must match the 0.4.0 Release contract")
        for name in libraries:
            with (directory / "jniLibs" / name).open("rb") as stream:
                header = stream.read(20)
            if header[:6] != b"\x7fELF\x02\x01" or int.from_bytes(header[18:20], "little") != machine:
                raise ValueError(f"Android native payload has the wrong ELF ABI: {abi}/{name}")
    if not (player / "java/org/libsdl/app/SDLActivity.java").is_file():
        raise FileNotFoundError("Android plugin is missing the SDL Java host")


def build_release(tag: str | None = None, output: Path | None = None) -> tuple[Path, Path]:
    root = Path(__file__).resolve().parent
    metadata = json.loads((root / "package/inx_package.json").read_text(encoding="utf-8"))
    expected = f"v{metadata['version']}"
    if tag is None:
        tag = expected
    if tag != expected:
        raise ValueError(f"Release tag must match package version: {expected}")
    _require_native_payloads(root)
    destination = output if output is not None else root / "dist"
    destination.mkdir(parents=True, exist_ok=True)
    stem = metadata["reference"].replace("/", ".")
    artifact = package.build(destination / f"{stem}.inxpkg")
    manifest = destination / f"{stem}.release.json"
    document = {
        "$schema": "infernux.plugin_release",
        "reference": metadata["reference"],
        "version": metadata["version"],
        "engine": metadata["engine"],
        "artifact": {"name": artifact.name},
        "generator": "Infernux platform package release.py",
        "release_tag": tag,
    }
    manifest.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return artifact, manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", nargs="?", help="v followed by package/inx_package.json version")
    arguments = parser.parse_args()
    for path in build_release(arguments.tag):
        print(path)
