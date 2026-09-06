# Infernux Android Platform 0.2.0

Official platform package for Infernux ==0.4.0.

- Ships precompiled ARM64 and x86_64 native Players plus the SDL Java host.
- Assembles APK/AAB exports without engine sources, CMake or native compilation.
- Reads each game's orientation policy at runtime.
- Includes English and Simplified Chinese documentation with a build workflow illustration.
- Ships an installable InxPackage and the engine's compatible-release manifest.

## Requirements

Install Infernux 0.4.0, Android compatibility in Hub, and the complete Android platform plugin. The plugin includes precompiled ARM64/x86_64 Player libraries and SDL Java host files. Normal APK/AAB exports do not require an engine source checkout, Git submodules, CMake, or host-side pybind11.

Install Android compatibility through Hub before importing. The large Android Platform Kit is distributed separately through the Hub channel; this release does not include that kit.

Download the .inxpkg asset to install the plugin. The automatic source archives are for plugin development. See the README for setup, output and troubleshooting details.
