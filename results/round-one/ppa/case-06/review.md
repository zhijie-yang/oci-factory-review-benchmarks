# OCI Factory Local Review

**Verdict:** Request changes — the proposed recipe removes the `tini` package, which the service command depends on, breaking the runtime.

## Inline findings

`oci/demo/image.yaml:8` — [blocker] Source commit updated to `000000000000000000000000000000000000000d` (§3: Recipe regression)

The prior `rockcraft.yaml` (commit `000000000000000000000000000000000000000c`) stages `tini` at `recipes/before/rockcraft.yaml:21`. The proposed recipe (commit `000000000000000000000000000000000000000d`) removes it at `recipes/after/rockcraft.yaml:19-20`. The service command at `recipes/after/rockcraft.yaml:14` still references `/usr/bin/tini`. According to the frozen evidence, the proposed build supplies no alternative source for `/usr/bin/tini` (no transitive dependency, base layer, manifest output, or part supplies it). Pebble will execute the service command literally, causing runtime failure.

**Request:** Restore the `tini` entry to `stage-packages` in the proposed recipe, or confirm in this review that its removal is intentional (a reference to the upstream commit is not such confirmation).

## Gates

**Gates:** edge-first ✅ · EOL cap ✅ · track naming ✅ · deb-manifest ✅ · recipe-regression ❌ · vulnerability-scan -> not assessed locally

- **edge-first:** track `1.2-24.04` targets `edge` only; no new track or base ✅
- **EOL cap:** main app is staged deb (not upstream-sourced); no CODEOWNERS support plan required; end-of-life 2026-12-01 is within 3 months from 2026-10-16 ✅
- **track naming:** `1.2-24.04` is SemVer (1.2.x, no patch); correctly formatted ✅
- **deb-manifest:** recipe includes `deb-security-manifest` part wired correctly ✅
- **recipe-regression:** `tini` dropped; service command references it but no alternative supplies it ❌
- **vulnerability-scan:** not assessed locally; verify in CI

## Summary

Trigger commit changed from `000000000000000000000000000000000000000c` to `000000000000000000000000000000000000000d`. Source recipe dropped `tini` package from `stage-packages` while the service command remains unchanged and depends on `/usr/bin/tini`. No alternative source (transitive dependency, base, manifest, or other part) supplies this executable in the proposed build. This breaks the service at runtime.
