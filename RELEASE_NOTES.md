# 0.2.20 — Infernux 0.4.3-v8

- Build the complete Player payload from frozen engine commit `e57387c0b65fa0b4838341faafa0572d100e8411`.
- Match the 0.4.3-v8 SDK, including reversed-Z rendering, isolated camera globals and repaired custom sky depth.
- Retain the package engine requirement `>=0.4.3`; precompiled Players require the exact matching engine release.

# 0.2.18 — Infernux 0.4.3-v5 UI shader dependency recovery

- Rebuild from frozen engine commit `ed45567cdceda66bfc7d762a9e0f0bb36c778ebb`.
- Reject only the affected UI draw when a referenced shader is missing; keep the renderer and healthy UI running.
- Resume the material through normal asset publication when its shader is restored, retaining the previous valid program after an invalid save.
- Keep the engine requirement `>=0.4.3` and the exact matching precompiled Player release.

# 0.2.17 — Infernux 0.4.3-v5 Player shutdown fix

- Rebuild both native ABIs from frozen engine commit `de7cc8c8b0ecbfbb7afd8553f256a1fa236f0aaa`.
- Unload native scenes before releasing asset catalogs so component shutdown retains font and other asset references.
- Keep the package engine requirement `>=0.4.3` and exact matching precompiled Player release.

# 0.2.16 — Infernux 0.4.3-v5

- Rebuild both Android Player ABIs (arm64-v8a and x86_64) against Infernux 0.4.3-v5.
- Build from frozen engine commit `f683bfa678eb680748c20be91badb9fe668ec553`.
- Keep the package engine requirement `>=0.4.3`; precompiled Players require the exact matching engine release.

# 0.2.12 — Infernux 0.4.3

- Rebuild the complete Player payload against the final 0.4.3 engine source, including asset import-failure publication.
- Keep the engine requirement >=0.4.3.

# 0.2.11 — Infernux 0.4.3

- Rebuild both precompiled Android ABIs with Infernux 0.4.3.
- Include mobile font, input and particle descriptor-limit repairs.
- Support non-ASCII Windows host paths and compact incremental APK content replacement.
- Keep the package engine requirement >=0.4.3; native payloads require the exact engine release.

- Derive the runtime version from the package/engine identity instead of hard-coding a previous release.

# 0.2.9 — Infernux 0.4.2 revision 2

- Publish the exporter and precompiled Player payload built with Infernux 0.4.2-v2.
- Preserve the exact engine-release check for precompiled runtimes.
- Keep the package engine requirement >=0.4.2.
- Publish new immutable artifacts; earlier package releases remain unchanged.
