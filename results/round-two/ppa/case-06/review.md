# OCI Factory Code Review

**Verdict:** Request changes — Recipe regression detected: tini package removed but service still depends on it.

## Inline findings

`recipes/after/rockcraft.yaml:19–20` — [blocker] The proposed recipe removes `tini` from `stage-packages`, but the service command on line 14 still explicitly invokes `/usr/bin/tini`. The supplied evidence confirms that tini is not present in the final filesystem and is supplied by no other means. This is a runtime failure: Pebble will not be able to execute the service. Restore `tini` to `stage-packages` or update the service command to not depend on it. (§3 recipe regression)

## Gates

**Gates:** eol-cap n/a · deb-manifest ✅ · recipe-regression ❌ · vuln scan → not assessed locally

- **eol-cap:** n/a — No upstream-sourced part with new commits; version stays within 1.2.x.
- **deb-manifest:** ✅ — The deb-security-manifest part is correctly declared and configured per specification.
- **recipe-regression:** ❌ — The source bump (commit 000c → 000d) drops the `tini` package from stage-packages. The service still requires it; this must be resolved before merging.
- **vuln scan:** not-assessed locally — Vulnerability scanning is CI-only; verify the latest run passes before approval.

## Summary

The trigger diff updates the commit hash from 000c to 000d in `oci/demo/image.yaml`. The source recipes differ in `parts.app.stage-packages`: the proposed recipe removes `tini`, while the unchanged service command still depends on `/usr/bin/tini`. This is a recipe regression that breaks the service at runtime.
