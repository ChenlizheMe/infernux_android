"""Consume the Android native payload published by the plugin's CMake target."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

NATIVE_LIBRARIES = (
    "libmain.so", "libSDL3.so", "_Infernux.so", "_InfernuxBootstrap.so",
    "libInfernuxFoundation.so", "libInfernuxParticleRuntime.so",
    "libInfernuxRenderCore.so", "libInfernuxRendererRuntime.so",
    "libInfernuxShaderCompiler.so", "libInfernuxVulkanBackend.so",
    "libInfernuxVulkanLoader.so", "libassimp.so", "libJolt.so",
)


def inspect_native_payload(root: Path, *, abi: str) -> dict[str, object]:
    from Infernux.version import ENGINE_VERSION

    manifest = json.loads((root / abi / "Player.inxmanifest").read_text(encoding="utf-8"))
    expected = {"engine_version": ENGINE_VERSION, "platform": "android",
                "abi": abi, "python_abi": "cp313", "minimum_api": 26}
    if not isinstance(manifest, dict) or any(manifest.get(k) != v for k, v in expected.items()):
        raise ValueError("Android Player payload does not match this engine/ABI")
    if manifest.get("configuration") not in {"Release", "RelWithDebInfo"}:
        raise ValueError("Android Player payload must be an optimized native build")
    for name in NATIVE_LIBRARIES:
        path = root / abi / "jniLibs" / name
        if not path.is_file():
            raise FileNotFoundError(f"Android platform plugin is missing {path}")
    if not (root / "java/org/libsdl/app/SDLActivity.java").is_file():
        raise FileNotFoundError("Android platform plugin has no SDL Java host")
    return manifest


def stage_native_payload(root: Path, staging: Path, *, abi: str) -> None:
    """Assemble an already selected payload; CPython remains Hub-owned."""
    native = staging / "app/src/main/jniLibs" / abi
    native.mkdir(parents=True, exist_ok=True)
    # The directory is generated build state. Keep only the just-staged CPython
    # libraries while replacing the platform payload, including removed members.
    for path in native.glob("*.so"):
        if not path.name.startswith("libpython") and not path.name.endswith("_python.so"):
            path.unlink()
    for path in (root / abi / "jniLibs").glob("*.so"):
        shutil.copy2(path, native / path.name)
    java = staging / "app/src/main/java/org/libsdl"
    if java.exists():
        shutil.rmtree(java)
    shutil.copytree(root / "java/org/libsdl", java, ignore=shutil.ignore_patterns("*.meta"))
