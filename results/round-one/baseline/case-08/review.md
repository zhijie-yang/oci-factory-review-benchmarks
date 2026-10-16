# OCI Factory Code Review

**Verdict:** Request changes

The proposed source update introduces a recipe regression that breaks runtime functionality. The `/opt/demo` directory permission and ownership changes prevent the demo service from accessing its required configuration file.

## Inline comments

`recipes/after/rockcraft.yaml:30` — [blocker] Permission mode changed from `0750` to `0700` prevents the _daemon_ user (UID 584792) from accessing the directory. The service runs as _daemon_ and must read `/opt/demo/server.conf` at startup with no fallback (§3 recipe regression).

`recipes/after/rockcraft.yaml:33` — [blocker] Ownership changed from `584792:584792` (daemon user) to `0:0` (root). Combined with mode `0700`, the daemon service can no longer access `/opt/demo` at runtime (§3 recipe regression).

## Gates

**Gates:** deb-manifest ✅ · recipe-regression ❌ · eol-cap n/a · vulnerability-scan → not assessed locally

- **deb-manifest:** ✅ pass — Rock properly includes `deb-security-manifest` part (required for stage-packages content).
- **recipe-regression:** ❌ fail — Source bump drops runtime access to configuration directory for the service user; prior recipe had `0750` with daemon ownership, enabling the service to function.
- **eol-cap:** n/a — No support plan acceptance is claimed; end-of-life date (2026-12-01) is within the 3-month window from freeze date (2026-10-16), meeting the statutory cap.
- **vulnerability-scan:** not assessed locally — Static checks pass; full scan requires CI execution.

## Summary

The source commit bump modifies `runtime-config` part permissions in `rockcraft.yaml`. The proposed changes alter `/opt/demo` from `584792:584792 0750` to `0:0 0700`, removing execute permission and changing ownership from the service user to root. This breaks the service's ability to read its mandatory configuration file at runtime.
