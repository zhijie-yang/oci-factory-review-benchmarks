# OCI Factory Code Review

**Verdict:** Approve. The recipe patch-version update is supported by the existing track, maintains required build components, and satisfies all locally-assessable gates.

## Summary

This change bumps the demo-rock recipe from v1.2.0 to v1.2.1 within the established `1.2-24.04` track on Ubuntu 24.04. The trigger commit advances from `...0016` to `...0017` to select the updated recipe snapshot. No parts, services, packages, build scripts or runtime behavior are altered; the change is version-only with a matching source-tag update.

## Inline findings

None.

## Recipe comparison

**Prior recipe:** `recipes/before/rockcraft.yaml` (commit `...0000000000000000000000000000000000000016`)
**Proposed recipe:** `recipes/after/rockcraft.yaml` (commit `...0000000000000000000000000000000000000017`)

**Changes between recipes:**
- `version`: `1.2.0` → `1.2.1` (recipe version line 4)
- `source-tag`: `v1.2.0` → `v1.2.1` (app part, line 21)

**No changes to:**
- `parts` structure: `app` and `deb-security-manifest` unchanged
- `services`: `demo` service definition identical
- Build and stage packages: `gcc`, `make`, `libc6` unchanged
- Override scripts: `override-prime: gen_manifest` unchanged
- Base and build-base: `ubuntu@24.04` stable

## Gate assessment

**EOL cap:** ✅ Pass. The track `1.2-24.04` has end-of-life 2026-12-01 (within 3 months of 2026-10-16). No support plan extension is requested or required for this patch release.

**Deb manifest:** ✅ Pass. The recipe includes the required `deb-security-manifest` part (lines 27–32), properly sourced from `https://github.com/canonical/rocks-security-manifest` with `override-prime: gen_manifest`.

**Recipe regression:** ✅ Pass. No parts, services or packages are removed. The patch-version source-tag update does not alter the build interface or package closure per supplied evidence.

**Vulnerability scan:** Not assessed locally (CI responsibility).

**One-image check:** ✅ Pass. Only `oci/demo/image.yaml` is modified.

## Recommendation

Approve for merge.
