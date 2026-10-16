# OCI Factory Code Review

**Verdict:** Request changes. Recipe regression: jq removal lacks confirmed intentional removal with supporting analysis.

## Inline findings

`recipes/before/rockcraft.yaml:21` — [blocker] Recipe regression: `stage-packages` entry `jq` is removed in the proposed recipe but the author has not provided usage analysis confirming no supported path depends on it. Per §3, removal of a `parts:` or `services:` entry during a source bump requires either restoring the entry or the author's explicit confirmation with supporting evidence (an assertion that it is optional is not sufficient). (§3)

`oci/demo/image.yaml:8` — [nit] EOL cap: `end-of-life: 2026-12-01` is 97 days from today (2026-10-16). Per §2, when a rock is upstream-sourced (the `app` part has no source; demo-app is a deb) and no support plan has been accepted by a human in CODEOWNERS, EOL is at most today + 3 months. The context confirms no support plan has been accepted. Request a support plan to justify this EOL date. (§2)

## Gates

**Gates:** edge-first ✅ · track naming ✅ · deb-manifest ✅ · recipe-regression ❌ · eol-cap ⚠ · deb-manifest ✅ · vulnerability-scan → not assessed locally

- **edge-first:** Pass. Track `1.2-24.04` targets `edge` risk only.
- **track naming:** Pass. Track `1.2-24.04` follows `<version>-<base>` format (SemVer `1.2.0` → `1.2`).
- **deb-manifest:** Pass. Recipe includes `deb-security-manifest` part from canonical/rocks-security-manifest as required (§3).
- **recipe-regression:** Fail. Proposed recipe removes `jq` from `stage-packages` without confirmed intentional removal and supporting analysis.
- **eol-cap:** Warning. EOL date exceeds recommended cap without accepted support plan; requires human CODEOWNERS approval or a support plan.
- **vulnerability-scan:** Not assessed locally; verify in CI.

## Summary

The proposed commit (0000000000000000000000000000000000000013) removes `jq` from `stage-packages` in the `app` part. The author requests this removal citing it as an optional convenience tool, but has not provided usage analysis confirming no supported path or documented tool contract depends on it. The context notes "whether any supported path uses jq cannot be determined from this bundle." This removal constitutes a recipe regression under §3 and blocks approval until resolved. Additionally, the EOL date requires a support plan per §2 guidelines. Keep at `edge` until both issues are resolved.
