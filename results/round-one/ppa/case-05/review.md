# OCI Factory Code Review

**Verdict:** Approve. Local checkable gates pass; source bump removes an intentionally-unused nil part with author confirmation.

---

## Inline Comments

`changes.diff:8` — [nit] source commit updated from `000000000000000000000000000000000000000a` to `000000000000000000000000000000000000000b` (§3)

---

## Recipe Analysis

**Prior:** `canonical/demo-rock` @ `000000000000000000000000000000000000000a` / `rocks/demo/rockcraft.yaml`
**Proposed:** `canonical/demo-rock` @ `000000000000000000000000000000000000000b` / `rocks/demo/rockcraft.yaml`

### Parts comparison

- **Removed:** `build-marker` (lines 27–28, before)
  - Type: nil plugin, no source, no packages, no scripts, no output
  - Dependents: none
  - Author confirmation: PR states removal is intentional; no other part orders on it
  - Evidence: evidence.md confirms nil part, no filesystem or service impact
  - **Conclusion:** Non-breaking, intentional removal; no recipe regression (§3)

- **Retained:** `app` (deb `stage-packages: demo-app`), `deb-security-manifest` (security manifest part)
  - Deb security manifest requirement: satisfied (§3)
  - Base: Ubuntu 24.04, adds deb content via `stage-packages`
  - Manifest source: `https://github.com/canonical/rocks-security-manifest`, `main` branch, correctly wired

### Services & version

- Services: `demo` (override: replace, `/usr/bin/demo serve`, startup: enabled) — unchanged
- Recipe version: `1.2.0` — unchanged
- Image track: `1.2-24.04` — unchanged, correct SemVer format (patch omitted per spec)
- End-of-life: `2026-12-01` (3 months from frozen date 2026-10-16) — within cap, pre-authorized by edge risk

---

## Gates

- **One-image:** ✅ pass — single upload item
- **Edge-first:** ✅ pass — no new track, base, or rock; release already edge-only
- **EOL cap:** ✅ pass — no new upstream-sourced track; end-of-life within 3 months and pre-authorized
- **Track naming:** ✅ pass — existing `1.2-24.04` follows SemVer spec
- **Deb-manifest:** ✅ pass — `deb-security-manifest` part present and correctly sourced
- **Recipe-regression:** ✅ pass — removed `build-marker` is nil with no dependents; author confirms intentional removal
- **Vulnerability scan:** not assessed locally (CI-only)
- **Documentation:** n/a — no changes to `documentation.yaml`
- **CVE justification & .trivyignore:** n/a — no vulnerability entries modified

---

## Summary

Source bump from commit `000000000000000000000000000000000000000a` to `000000000000000000000000000000000000000b` removes an intentionally-unused nil `build-marker` part with confirmed author intent and no impact to runtime or service contract. No recipe regression. Deb security manifest requirement satisfied. All locally-checkable gates pass.
