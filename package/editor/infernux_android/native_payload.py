"""Consume the Android native payload published by the plugin's CMake target."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

NATIVE_LIBRARIES = (
    "libmain.so", "libSDL3.so", "_Infernux.so", "_InfernuxBootstrap.so",
    "libInfernuxFoundation.so", "libInfernuxAudioRuntime.so",
    "libInfernuxAssetRuntime.so", "libInfernuxParticleRuntime.so",
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
    declared = manifest.get("native_libraries")
    if (not isinstance(declared, list)
            or any(not isinstance(name, str) for name in declared)
            or len(declared) != len(set(declared))
            or set(declared) not in (set(NATIVE_LIBRARIES),
                                    set(NATIVE_LIBRARIES) | {"libc++_shared.so"})):
        raise ValueError("Android Player native library manifest does not match this engine")
    for name in declared:
        path = root / abi / "jniLibs" / name
        if not path.is_file():
            raise FileNotFoundError(f"Android platform plugin is missing {path}")
    if not (root / "java/org/libsdl/app/SDLActivity.java").is_file():
        raise FileNotFoundError("Android platform plugin has no SDL Java host")
    return manifest


def stage_native_payload(root: Path, staging: Path, *, abi: str) -> None:
    """Assemble an already selected payload; CPython remains Hub-owned."""
    manifest = inspect_native_payload(root, abi=abi)
    native = staging / "app/src/main/jniLibs" / abi
    native.mkdir(parents=True, exist_ok=True)
    # The directory is generated build state. Keep only the just-staged CPython
    # libraries while replacing the platform payload, including removed members.
    for path in native.glob("*.so"):
        if not path.name.startswith("libpython") and not path.name.endswith("_python.so"):
            path.unlink()
    for name in manifest["native_libraries"]:
        shutil.copy2(root / abi / "jniLibs" / name, native / name)
    java = staging / "app/src/main/java/org/libsdl"
    if java.exists():
        shutil.rmtree(java)
    shutil.copytree(root / "java/org/libsdl", java, ignore=shutil.ignore_patterns("*.meta"))
    input_connection = next(java.rglob("SDLInputConnection.java"), None)
    if input_connection is not None:
        _patch_sdl_input_connection(input_connection)
    activity = next(java.rglob("SDLActivity.java"), None)
    if activity is not None:
        _patch_sdl_activity(activity)


def _patch_sdl_input_connection(path: Path) -> None:
    """Make Enter and Backspace explicit SDL key edges for Android IMEs."""

    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if "SDLActivity.onNativeKeyDown(KeyEvent.KEYCODE_DEL)" in text:
        return
    old_enter = (
        "        if (event.getKeyCode() == KeyEvent.KEYCODE_ENTER) {\n"
        "            if (SDLActivity.onNativeSoftReturnKey()) {\n"
        "                return true;\n"
        "            }\n"
        "        }\n"
    )
    new_enter = (
        "        final int keyCode = event.getKeyCode();\n"
        "        if (keyCode == KeyEvent.KEYCODE_ENTER) {\n"
        "            if (SDLActivity.onNativeSoftReturnKey()) {\n"
        "                return true;\n"
        "            }\n"
        "            if (event.getAction() == KeyEvent.ACTION_DOWN) {\n"
        "                SDLActivity.onNativeKeyDown(keyCode);\n"
        "                return true;\n"
        "            }\n"
        "            if (event.getAction() == KeyEvent.ACTION_UP) {\n"
        "                SDLActivity.onNativeKeyUp(keyCode);\n"
        "                return true;\n"
        "            }\n"
        "        }\n"
        "        if (keyCode == KeyEvent.KEYCODE_DEL) {\n"
        "            if (event.getAction() == KeyEvent.ACTION_DOWN) {\n"
        "                SDLActivity.onNativeKeyDown(keyCode);\n"
        "                return true;\n"
        "            }\n"
        "            if (event.getAction() == KeyEvent.ACTION_UP) {\n"
        "                SDLActivity.onNativeKeyUp(keyCode);\n"
        "                return true;\n"
        "            }\n"
        "        }\n"
    )
    if old_enter not in text:
        raise ValueError("Unsupported SDLInputConnection.sendKeyEvent layout")
    text = text.replace(old_enter, new_enter, 1)
    text = text.replace(
        "                nativeGenerateScancodeForUnichar('\\b');\n",
        "                SDLActivity.onNativeKeyDown(KeyEvent.KEYCODE_DEL);\n"
        "                SDLActivity.onNativeKeyUp(KeyEvent.KEYCODE_DEL);\n",
    )
    path.write_text(text, encoding="utf-8", newline="\n")


def _patch_sdl_activity(path: Path) -> None:
    """Make repeated SDL text-input shows reliable on current Android IMEs."""

    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    if "imm.restartInput(mTextEdit);" in text:
        return
    old = (
        "            InputMethodManager imm = (InputMethodManager) getContext().getSystemService(Context.INPUT_METHOD_SERVICE);\n"
        "            imm.showSoftInput(mTextEdit, 0);\n\n"
        "            if (imm.isAcceptingText()) {\n"
        "                onNativeScreenKeyboardShown();\n"
        "            }\n"
    )
    new = (
        "            final InputMethodManager imm = (InputMethodManager) getContext()\n"
        "                    .getSystemService(Context.INPUT_METHOD_SERVICE);\n"
        "            // Reset the reused hidden editor before every show. Some Android 13+\n"
        "            // IMEs keep the old InputConnection after hide and ignore the next show.\n"
        "            imm.restartInput(mTextEdit);\n"
        "            // Defer until focus/layout have settled; inline show is ignored while a\n"
        "            // previous hide is still completing on several vendor IMEs.\n"
        "            mTextEdit.post(() -> {\n"
        "                if (mTextEdit.getVisibility() != View.VISIBLE || !mTextEdit.hasFocus()) {\n"
        "                    return;\n"
        "                }\n"
        "                imm.showSoftInput(mTextEdit, InputMethodManager.SHOW_IMPLICIT);\n"
        "                if (imm.isAcceptingText()) {\n"
        "                    onNativeScreenKeyboardShown();\n"
        "                }\n"
        "            });\n"
    )
    if old not in text:
        raise ValueError("Unsupported SDLActivity.ShowTextInputTask layout")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
