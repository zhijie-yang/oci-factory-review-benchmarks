# OCI Factory Code Review

**Verdict:** Approve. The proposed commit refactors a shell override-build without dropping parts, services, or functionality; all locally-checkable gates pass.

## Inline Findings

`oci/demo/image.yaml:8` — Source bump from prior commit `0000000000000000000000000000000000000014` to `0000000000000000000000000000000000000015`. The referenced `rockcraft.yaml` refactors the `metadata` part's override-build script, extracting a variable for the installation path. Evidence confirms both scripts produce identical output, ownership, and file mode; no parts or services are removed (§3). The recipe-regression gate passes.

## Gates

**Gates:** deb-manifest ✅ · recipe-regression ✅ · eol-cap ✅ · comparison ✅

- **deb-manifest:** The `deb-security-manifest` part is present, correctly sourced and wired (§3). Pass.
- **recipe-regression:** No parts (`app`, `deb-security-manifest`, `metadata`) or services (`demo`) are dropped in the source bump. Pass.
- **eol-cap:** The track `1.2-24.04` is established (not new) and remains on edge only per context. The `end-of-life: '2026-12-01'` date is ~1.5 months from the review freeze, within the 3-month window for edge releases. No upstream-compiled application requires an accepted support plan. Pass.
- **vulnerability-scan:** Not assessed locally; verify in CI.

## Summary

The proposed revision updates the trigger commit to a recipe containing an internal shell-variable refactor in the `metadata` part's override-build. Functionally equivalent behavior is supplied as evidence. No parts, services, repositories, or documented configuration are changed; the version remains `1.2.0` and track `1.2-24.04` is edge-only per context.
