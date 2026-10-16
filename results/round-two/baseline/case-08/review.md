## OCI Factory Local Dry Run Review

**Verdict: Request changes** — Recipe regression: /opt/demo ownership change breaks the configured runtime.

### Inline findings

`recipes/after/rockcraft.yaml:30,33` — [blocker] Recipe regression (§3): The `runtime-config` part changes `/opt/demo` from `584792:584792 mode 0750` to `0:0 mode 0700`. The app runs as `_daemon_` (UID 584792) per the `run-user` field, but with root-owned (0:0), owner-only-writable (0700) directory, the daemon user has no write access to its own config directory. The evidence states "The runtime has no DAC override/search capability, ACL grant, root helper or identity-changing step" and "The configured app must open this file before listening, with no fallback." This breaks the configured runtime. Confirm in the PR that this removal of daemon write access is intentional, or restore the prior ownership and mode.

### Gates

**EOL cap:** n/a — No new track, base or upstream source bump in the demo-app itself (it remains a synthetic Ubuntu archive deb staged by name).

**Deb-manifest:** pass — The recipe includes the required `deb-security-manifest` part (line 21–26).

**Recipe-regression:** fail — The runtime-config ownership and mode change is unresolved; the revision cannot be released above edge.

**Vulnerability-scan:** not-assessed locally — Verify in CI.

### Summary

The trigger commit was bumped from `0000000000000000000000000000000000000010` to `0000000000000000000000000000000000000011`. The recipe recipe `runtime-config` part changed: `/opt/demo` directory ownership shifted from the daemon user (584792:584792, mode 0750) to root (0:0, mode 0700). This is a functional regression that removes the configured app's write access to its own config directory. No other parts, services, packages, version or repositories changed between revisions.
