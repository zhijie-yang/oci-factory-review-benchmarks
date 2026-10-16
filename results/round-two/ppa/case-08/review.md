# OCI Factory Local Review

**Verdict:** Request changes. The proposed recipe changes directory ownership and permissions in a way that breaks the application at runtime.

## Findings

### `recipes/after/rockcraft.yaml:30` — [blocker] Runtime permission regression (§3)

The proposed recipe changes `/opt/demo` from mode `0750` owned by `584792:584792` (the `_daemon_` run-user) to mode `0700` owned by `0:0` (root). The application runs as `_daemon_` (UID 584792) and must open `/opt/demo/server.conf` before listening, with no fallback. Root ownership of the target directory denies the run-user write/search permission. This is a runtime failure, not a configuration adjustment.

Evidence: 
- **Before** (line 30): `install -d -m 0750 "$CRAFT_PART_INSTALL/opt/demo"` with `chown 584792:584792` (line 33)
- **After** (line 30): `install -d -m 0700 "$CRAFT_PART_INSTALL/opt/demo"` with `chown 0:0` (line 33)
- **Runtime**: Application runs as `_daemon_` (UID 584792); no DAC override, ACL grant, or root helper exists (evidence.md:9–10)
- **Behavior**: Server cannot open `/opt/demo/server.conf` (owned by root, in a root-only readable directory); startup fails

**Requested action:** Restore the prior ownership (`584792:584792`) and permissions (`0750`), or provide justification for the application no longer needing write/search access to its own config directory at runtime.

## Gates

- **one-image:** ✅ Single upload item touched
- **edge-first:** ✅ No new tracks; edge risk only
- **EOL cap:** ✅ End-of-life is within 3 months; no upstream-sourced parts beyond security-manifest
- **track naming:** ✅ Track `1.2-24.04` follows SemVer convention (1.2 omits patch)
- **deb-manifest:** ✅ Recipe declares `deb-security-manifest` part (required; deb content present via `stage-packages`)
- **recipe-regression:** ✅ No parts or services dropped; only configuration changes within existing parts
- **vulnerability scan:** → not assessed locally; verify in CI
