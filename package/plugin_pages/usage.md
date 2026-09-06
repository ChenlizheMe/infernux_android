# Android Platform

![Build workflow](media/overview.png)

Build Android Players for ARM64 devices and x64 emulators. The package owns target registration, toolchain diagnostics, Android host templates and APK/AAB export. Large reusable dependencies belong to the Hub's Android Platform Kit, not individual projects.

## Before building

Infernux 0.4.0 on Windows or Linux, Hub Android compatibility, and an Infernux source checkout with its submodules. Set INFERNUX_SOURCE_ROOT to that checkout. This version still builds the Android native host from engine sources; the plugin alone is not a source-free Android build SDK.

## Shared dependencies

Install **Android compatibility** in **Hub → Installations** before importing the plugin. The editor keeps Import disabled until the shared kit is installed. This prerequisite is deliberate, not an import-time download of SDKs. The kit is distributed through the Hub release channel separately from this plugin's Release assets; plugin publication does not publish the kit.

The current kit uses JDK 17, Gradle 8.12, Android API 36, build-tools 36.0.0, CMake 3.30.5, NDK 29.0.14206865 and both Android CPython 3.13 target runtimes. The plugin's requirements.txt installs pinned host-side pybind11 on import. An emulator and AVD are separate from a physical-device build.

## Build and install

Select android-arm64 for a physical ARM64 device or android-x64-emulator for an x64 emulator. Development builds default to APK; release builds default to AAB. The Player requires Vulkan; there is no OpenGL ES fallback. The minimum application API is 26.

For a development APK, use `adb install -r path/to/game.apk`. Updating an installed game requires a compatible signing key. Do not uninstall an existing game just to hide a signature mismatch.

## Signing and storage

A release AAB remains unsigned unless signing is configured. Set INFERNUX_ANDROID_KEYSTORE, INFERNUX_ANDROID_KEY_ALIAS, INFERNUX_ANDROID_KEYSTORE_PASSWORD, and optionally INFERNUX_ANDROID_KEY_PASSWORD (defaults to the keystore password). Never commit passwords or keystores.

Gradle caches use Shared/Cache/Gradle under Hub, or the project's Cache/Gradle for standalone launches. Debug signing state uses Shared/State/Android or the project's State/Android. Clearing caches must not discard signing keys. Explicit GRADLE_USER_HOME and ANDROID_USER_HOME remain authoritative.

## Troubleshooting

Disabled Import means Hub Android compatibility is not installed or incomplete. Missing source checkout, SDK, CPython or Gradle diagnostics must be fixed before building. If the Hub channel does not yet contain a compatible kit, this plugin Release cannot replace it.
