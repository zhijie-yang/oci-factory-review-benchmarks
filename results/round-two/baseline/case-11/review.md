# Review: demo/image.yaml (1.2-24.04 edge)

**Verdict:** Approve. The proposed commit updates the recipe from v1.2.0 to v1.2.1 (patch version), with no parts, services, scripts, or package changes. All locally-checkable gates pass.

## Inline comments

`oci/demo/image.yaml:4` — ✅ Commit bumped from `0000000000000000000000000000000000000016` to `0000000000000000000000000000000000000017`, corresponding to source-tag v1.2.0 → v1.2.1 (§3).

## Recipe analysis

### Changed elements
- **version**: 1.2.0 → 1.2.1
- **source-tag**: v1.2.0 → v1.2.1

### Assessed gates
- **eol-cap** ✅ — EOL set to 2026-12-01, which is within 3 months of the frozen date (2026-10-16). No support plan extension requested (§2).
- **deb-manifest** ✅ — Rock adds `stage-packages` (libc6) and includes the required `deb-security-manifest` part sourced from `canonical/rocks-security-manifest` (§3).
- **recipe-regression** ✅ — No parts or services dropped between recipes/before/rockcraft.yaml and recipes/after/rockcraft.yaml. Both retain `app` and `deb-security-manifest` parts, and the `demo` service (§3).
- **track-naming** ✅ — Track key `1.2-24.04` follows SemVer convention (version.minor-base), omitting patch as required (§2).
- **edge-first** ✅ — Release targets `edge` risk only; no concurrent promotion to candidate or stable (§2).

### Vulnerability scan
Not assessed locally; verify in CI.

## Summary

Recipe patch version bump from 1.2.0 to 1.2.1. No package, service, part, script, or permission changes. The established track (1.2-24.04) remains at edge-only release with unchanged EOL of 2026-12-01, confirming no support plan extension was requested.
