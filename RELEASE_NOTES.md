# 0.2.10 — Infernux 0.4.2

- Rebuild the precompiled Player payload against the current 0.4.2 native
  bindings (the previous payload lacked `game_presentation_ready`, which made
  the Android Player exit during first-frame prewarm).
- Allow generated Android host projects below non-ASCII Windows paths by
  setting `android.overridePathCheck=true` in the host template.
- Keep the package engine requirement >=0.4.2.

# 0.2.9 — Infernux 0.4.2 revision 2

- Publish the exporter and precompiled Player payload built with Infernux 0.4.2-v2.
- Preserve the exact engine-release check for precompiled runtimes.
- Keep the package engine requirement >=0.4.2.
- Publish new immutable artifacts; earlier package releases remain unchanged.
