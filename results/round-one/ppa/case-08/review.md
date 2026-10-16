# OCI Factory Code Review

**Verdict:** Request changes. The proposed recipe changes make `/opt/demo` unreadable to the runtime process, breaking application startup.

## Findings

### `recipes/after/rockcraft.yaml:30, 33` — [blocker] Runtime permission regression (§3)

The source bump modifies the `runtime-config` part's `override-build` script to change `/opt/demo` from `584792:584792` mode `0750` to `0:0` mode `0700`. The evidence confirms the app must open `/opt/demo/server.conf` before listening, with no fallback. At runtime, the service runs as `_daemon_` (UID 584792) and cannot search a 0700 directory owned by root, causing startup failure.

**Requested action:** Restore the prior ownership and permissions, or confirm in the PR that the permission change is intentional and the app's configuration logic has changed to handle root-owned paths at runtime.

## Gates

- **eol-cap:** ✅ pass — `demo-app` is a synthetic Ubuntu archive package; no upstream-sourced support plan is required.
- **deb-manifest:** ✅ pass — Present and properly configured (`canonical/rocks-security-manifest`).
- **recipe-regression:** ✅ pass — Both `app` and `deb-security-manifest` parts are retained; only `runtime-config` script is modified.
- **vulnerability-scan:** ⚠ not assessed locally — Vulnerability scans are CI-only; verify in CI run.

## Summary

The diff is a single-commit bump from `0000000000000000000000000000000000000010` to `0000000000000000000000000000000000000011` on the established `1.2-24.04` edge-only track. The trigger file remains `oci/demo/image.yaml` targeting `canonical/demo-rock` at `rocks/demo` with stable EOL date `2026-12-01`. The recipe changes are limited to two lines in the `runtime-config` build script: directory permissions (`0750` → `0700`) and ownership (`584792:584792` → `0:0`). Per the frozen evidence, this change breaks the application's access to its configuration file at runtime, making it a blocker.
