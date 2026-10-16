# OCI Factory Code Review

**Verdict: Request changes.** The proposed recipe change removes the daemon user's access to the configuration directory, breaking the service at runtime.

## Inline comments

`oci/demo/image.yaml:8` — **[blocker]** Source recipe regression: configuration directory access (§3)

The recipe change at `recipes/after/rockcraft.yaml:30` and `:33` removes the daemon service's ability to access `/opt/demo`:
- Directory ownership changes from `584792:584792` to `0:0` (root)
- Directory mode changes from `0750` to `0700`, removing all permissions for non-owner users

The service runs as `_daemon_` (UID 584792, per evidence.md line 7), but with mode 0700 and root ownership, the daemon has no read or execute permission on the directory. The service must open `/opt/demo/server.conf` before listening (evidence.md line 14), and no fallback is provided. This change will cause the service to fail at runtime.

The author's description ("adjusting configuration directory permissions") does not confirm intentional removal. Restore the directory ownership to `584792:584792` and mode to `0750`, or provide explicit confirmation in the PR that this breaking change is intentional and document the service's new startup requirements.

## Gates

- **EOL cap:** ✅ pass — demo-app is from Ubuntu archive; 2026-12-01 within 3 months.
- **deb-manifest:** ✅ pass — present and correctly wired in both recipes.
- **recipe-regression:** ❌ fail — configuration directory ownership and mode prevent service startup.
- **vulnerability-scan:** → not assessed locally (CI-only).
