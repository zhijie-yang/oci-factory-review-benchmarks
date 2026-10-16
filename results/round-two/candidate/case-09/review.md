# OCI Factory Code Review

**Verdict:** Request changes — a regression blocker was identified.

## Summary

This change bumps the `demo` rock from commit `0000000000000000000000000000000000000012` to `0000000000000000000000000000000000000013` within the established `1.2-24.04` track on `edge` risk. The recipe diff shows removal of `jq` from `stage-packages`.

## Inline Findings

`recipes/before/rockcraft.yaml:21` — `recipes/after/rockcraft.yaml:20` — [blocker] Package removal regression: `jq` is dropped from the `app` part's `stage-packages` (line 21 → removed). The PR author claims this is an optional convenience tool, but context.md states there is no supplied usage analysis, no runtime inventory, and no application source to confirm whether any supported runtime path depends on it. The supplied material provides no evidence that this removal is safe. Per §3 (recipe regression), this requires either restoration of the package or explicit confirmation from the author that the removal is intentional. Restore `jq` or confirm in the PR.

## Gates

- **deb-manifest:** ✅ pass — `deb-security-manifest` part is present and correctly wired per §3 MUST.
- **eol-cap:** n/a — no external upstream source detected; `demo-app` is staged from the Ubuntu archive by name, not compiled from an external repository.
- **recipe-regression:** ❌ fail — `jq` removed from `stage-packages`; awaiting author confirmation or restoration per §3.
- **vulnerability-scan:** not-assessed locally — no CVE entries affected; static rules in §1 apply; vulnerability scan runs in CI only.

## Detailed Assessment

### §1 Security & vulnerability gating
No CVE entries, `ignored-vulnerabilities` fields, or `.trivyignore` files are added, removed, or modified per context assumptions. No findings.

### §2 Release policy
- **Edge-first:** n/a — established track, not new.
- **EOL cap:** n/a — no upstream-sourced application; `demo-app` is staged from Ubuntu archive.
- **Track naming:** ✅ `1.2-24.04` is correctly formatted (SemVer omits patch).
- **Suspected regression:** ❌ Regression detected; edge-only release holds until resolved.

### §3 Source recipe (`rockcraft.yaml`)
Both recipes are available. Comparison is assessed.

**Recipe changes:** Package removal only.
- **Parts:** No addition/removal/reordering.
- **Services:** No changes.
- **Packages/slices:** `jq` removed from `app` part `stage-packages`.
- **Scripts:** No changes.
- **Version:** No change (stays `1.2.0`).

**Deb security manifest:** ✅ Present and correctly configured.

**Recipe regression:** ❌ The `jq` package is removed from `stage-packages` without explanation. Context.md explicitly notes that there is no application source, no runtime inventory, and no usage analysis supplied. The author's claim that jq is "optional" cannot be verified from the bundle. Per §3, this removal is a regression blocker unless the author confirms removal is intentional. The removal is not documented in commit context, and no evidence shows whether any supported path uses jq.

### §4 Documentation
Not touched by diff; no review required.

### §5 CI / GitHub Actions
Not touched by diff; no review required.

## Action Required

1. Restore `jq` in the recipe, or
2. Provide explicit confirmation in the PR that this removal is intentional, with evidence that no supported runtime path uses jq (e.g., analysis of the application source or integration tests).

Until resolution, the revision remains on `edge` only (§2 regression hold).
