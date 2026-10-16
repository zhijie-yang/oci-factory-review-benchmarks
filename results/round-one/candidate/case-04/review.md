# OCI Factory Local Review

**Verdict:** Request changes — service removal lacks author confirmation.

## Inline Findings

`oci/demo/image.yaml:9` — [blocker] Service regression detected (§3).

The proposed recipe at `rocks/new/rockcraft.yaml:16` removes the `demo-info` service that exists in the prior recipe at `rocks/old/rockcraft.yaml:16-19`. Per §3 recipe regression rules, this removal must be either restored or confirmed by the PR author as intentional. The context states no such confirmation is present. While evidence.md notes that demo-info was a disabled, on-demand informational service with no dependency from the primary `demo` service, the explicit regression gate requires author acknowledgment.

**Requested action:** Either restore the `demo-info` service in `rocks/new/rockcraft.yaml`, or request the author to confirm in the PR discussion that this removal is intentional.

## Gates

- **EOL cap:** pass — end-of-life 2026-12-01 is within 3 months of today (2026-10-16); no support plan required for archive-sourced app.
- **Deb manifest:** pass — both recipes include the security-manifest part for the deb-based `demo-app` content.
- **Recipe regression:** fail — `demo-info` service removed without documented author intent.
- **Vulnerability scan:** not-assessed — local review; CI run will verify.

## Summary

The trigger diff changes `upload[].directory` from `rocks/old` to `rocks/new` (same commit). Recipe comparison reveals:
- **Removed:** `services.demo-info` (disabled, informational)
- **Retained:** `services.demo`, all parts, base, packages
- **Scope:** services only

No version, base, package, or script changes detected between the recipes.
