# Infernux Android Platform 0.1.0

Official platform package for Infernux >=0.4.0,<0.5.

- Registers android-arm64 / android-x64-emulator and its platform build integration.
- Includes English and Simplified Chinese documentation with a build workflow illustration.
- Ships an installable InxPackage and the engine's compatible-release manifest.

## Requirements

Infernux 0.4.0 on Windows or Linux, Hub Android compatibility, and an Infernux source checkout with its submodules. Set INFERNUX_SOURCE_ROOT to that checkout. This version still builds the Android native host from engine sources; the plugin alone is not a source-free Android build SDK.

Install Android compatibility through Hub before importing. The large Android Platform Kit is distributed separately through the Hub channel; this release does not include that kit.

Download the .inxpkg asset to install the plugin. The automatic source archives are for plugin development. See the README for setup, output and troubleshooting details.
