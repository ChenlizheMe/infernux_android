# Infernux Android Platform

[简体中文](README.zh-CN.md) · [Releases](https://github.com/ChenlizheMe/infernux_android/releases) · [Infernux](https://github.com/ChenlizheMe/Infernux)

![Android build workflow](package/plugin_pages/media/overview.png)

Build Android Players for ARM64 devices and x64 emulators. The package owns target registration, precompiled native Players, SDL host files and APK/AAB export. Large reusable dependencies belong to the Hub's Android Platform Kit, not individual projects.

## At a glance

| Item | Value |
| --- | --- |
| Package | `infernux/platform-android` |
| Plugin version | 0.2.0 |
| Engine compatibility | ==0.4.0 |
| Target | `android-arm64 / android-x64-emulator` |
| Build host | Windows or Linux |
| Rendering | Android Player / Vulkan |

## Install

1. Open your project in Infernux 0.4.0 and open the Plugins panel.
2. Select Infernux Android Platform in the official list, then import and enable it. Install Hub Android compatibility first; otherwise Import stays disabled.
3. Open the build settings and select the target. Resolve the reported prerequisites before exporting.

If your editor's bundled catalog predates this repository, add `https://github.com/ChenlizheMe/infernux_android` as a GitHub plugin source, or import `infernux.platform-android.inxpkg` from [Releases](https://github.com/ChenlizheMe/infernux_android/releases/latest). GitHub's automatic source ZIP is the author repository, not the installable plugin artifact.

## Requirements

Install Infernux 0.4.0, Android compatibility in Hub, and the complete Android platform plugin. The plugin includes precompiled ARM64/x86_64 Player libraries and SDL Java host files. Normal APK/AAB exports do not require an engine source checkout, Git submodules, CMake, or host-side pybind11.

## Shared dependencies

Install **Android compatibility** in **Hub → Installations** before importing the plugin. The editor keeps Import disabled until the shared kit is installed. This prerequisite is deliberate, not an import-time download of SDKs. The kit is distributed through the Hub release channel separately from this plugin's Release assets; plugin publication does not publish the kit.

The current kit uses JDK 17, Gradle 8.12, Android API 36, build-tools 36.0.0, NDK 29.0.14206865 and both Android CPython 3.13 target runtimes. An emulator and AVD are separate from a physical-device build.

## Build and install

Select android-arm64 for a physical ARM64 device or android-x64-emulator for an x64 emulator. Development builds default to APK; release builds default to AAB. The Player requires Vulkan; there is no OpenGL ES fallback. The minimum application API is 26.

For a development APK, use `adb install -r path/to/game.apk`. Updating an installed game requires a compatible signing key. Do not uninstall an existing game just to hide a signature mismatch.

## Signing and storage

A release AAB remains unsigned unless signing is configured. Set INFERNUX_ANDROID_KEYSTORE, INFERNUX_ANDROID_KEY_ALIAS, INFERNUX_ANDROID_KEYSTORE_PASSWORD, and optionally INFERNUX_ANDROID_KEY_PASSWORD (defaults to the keystore password). Never commit passwords or keystores.

Gradle caches use Shared/Cache/Gradle under Hub, or the project's Cache/Gradle for standalone launches. Debug signing state uses Shared/State/Android or the project's State/Android. Clearing caches must not discard signing keys. Explicit GRADLE_USER_HOME and ANDROID_USER_HOME remain authoritative.

## Troubleshooting

Disabled Import means Hub Android compatibility is not installed or incomplete. Resolve SDK, CPython, Gradle or incomplete plugin payload diagnostics before building; use a plugin release matching engine 0.4.0. If the Hub channel does not yet contain a compatible kit, this plugin Release cannot replace it.

## Develop and package

The engine's Android CMake configuration now exposes `prebuild_android_player`
for release engineering. It builds the native host and engine with one SDL target
and writes the ABI-specific libraries directly to
`package/editor/infernux_android/player/<abi>/jniLibs/`, with shared SDL Java sources
under `player/java/`. Screen orientation is supplied through the game's manifest,
not compiled into the host. After building both ABIs in Release configuration, the CMake target
`package_android_plugin` creates the final `.inxpkg` and release manifest.
`native/build.py` is a maintainer-only cross-build entry point; it never runs
when users install the plugin or export games.

Only `package/` becomes the InxPackage payload. The outer README, SVG illustration sources, release automation and build scripts remain repository files. In-editor documentation is separate, under `package/plugin_pages/`.

```text
package/
  inx_package.json
  editor/infernux_android/
  plugin_pages/
package.py
release.py
README.md
README.zh-CN.md
```

Run `python package.py dist/infernux.platform-android.inxpkg` to package locally. This standalone script uses only Python's standard library and does not require an engine installation. Build outside package/, then place the files to ship inside package/ before packaging.

Maintainers run `python release.py v0.2.0` to create the archive and its release manifest. Pushing a matching version tag publishes both files through GitHub Actions. The editor uses that manifest to select a compatible release.

## License

[MIT](LICENSE). Third-party SDKs and the engine runtime keep their own licenses; they are not relicensed by this plugin.
