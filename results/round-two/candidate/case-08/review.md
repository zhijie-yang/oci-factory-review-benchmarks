# OCI Factory Local Review

**Verdict:** Request changes. The recipe change removes read/execute access from the run-user, breaking the application at runtime.

---

## Inline findings

`oci/demo/image.yaml:8` — **[blocker] Recipe regression: /opt/demo inaccessible at runtime (§3)**

The proposed commit modifies `rocks/demo/rockcraft.yaml` to change `/opt/demo` ownership from `584792:584792` (the run-user _daemon_) to `0:0` (root) and tighten permissions from `0750` to `0700`. 

According to the supplied evidence, the application must open `/opt/demo/server.conf` at startup with no fallback. The run-user _daemon_ has no DAC override or root helper, so _daemon_ cannot read or execute a root-owned 0700 directory. The application will fail to start.

**Before:** `/opt/demo` is `584792:584792 mode 0750` — readable and executable by the owner (_daemon_).

**After:** `/opt/demo` is `0:0 mode 0700` — inaccessible to _daemon_.

This is a concrete regression in runtime behavior: compare `recipes/before/rockcraft.yaml:30,33` to `recipes/after/rockcraft.yaml:30,33`. The PR description ("adjusting configuration directory permissions") does not confirm this breaking change as intentional per §3 guidance.

---

## Gates

- **eol-cap:** n/a — No upstream-sourced parts; version remains 1.2.0 within 1.2.x.
- **deb-manifest:** pass — The recipe includes the required security-manifest part; stage-packages declares demo-app.
- **recipe-regression:** fail — The /opt/demo ownership and permissions change breaks app access to its config file.
- **vulnerability-scan:** not assessed locally — Verify in CI.

---

## Changes assessed

- scripts (override-build permission and ownership edits)

## Summary

The recipe changes are limited to the `runtime-config` part's override-build script, modifying directory setup but no parts, services, or packages. The comparison is fully assessed via the supplied snapshots. However, the permissions/ownership change is a blocker regression.
