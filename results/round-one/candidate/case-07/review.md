# OCI Factory Code Review

**Verdict:** Request changes. The proposed recipe removes a critical runtime dependency, causing application startup failure.

## Findings

`recipes/after/rockcraft.yaml:30` — **[blocker]** Recipe regression: removed `libgomp1_libs` slice (§3)

The prior recipe stages `libgomp1_libs` in the `runtime-libraries` part; the proposed recipe removes it. Per evidence.md, this slice is the only source of `libgomp.so.1` in the prior rootfs. The service command (`/usr/bin/demo serve --engine parallel`, `recipes/before/rockcraft.yaml:14`) requires loading the parallel engine, which has an ELF DT_NEEDED dependency on `libgomp.so.1`. Removing this slice leaves the library unresolved at runtime, causing the application to fail at startup.

The author states the source update reduces staged slices, but removal of a mandatory runtime dependency is a regression, not an optimization. Confirm whether the `--engine parallel` option has been removed upstream or superseded, or restore the `libgomp1_libs` slice.

## Gates

- **EOL cap:** n/a (no direct upstream source in app part, support plan not required)
- **Deb-manifest:** pass (deb-security-manifest part present and correctly wired)
- **Recipe-regression:** fail (mandatory library removed)
- **Vulnerability-scan:** not-assessed locally

## Changes

- packages (libgomp1_libs removed from staged slices)
