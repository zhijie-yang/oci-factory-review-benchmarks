## Code Review: OCI Factory LOCAL Dry Run

**Verdict:** Request changes

The proposed source bump removes `jq` from the application rock's `stage-packages` list. While the PR author describes it as an optional tool, no usage analysis or confirmation that no code path depends on it has been provided.

---

## Inline Findings

`oci/demo/image.yaml:4` — [blocker] recipe regression: `jq` removal unconfirmed (§3)

The prior recipe includes `jq` in `app.stage-packages` (recipes/before/rockcraft.yaml:21), and the proposed recipe removes it (recipes/after/rockcraft.yaml:21 omitted). Per §3 recipe regression rules, a parts/packages removal must either be restored or the author must confirm in the PR that the removal is intentional. 

The supplied discussion calls `jq` an "optional convenience tool" but acknowledges that:
- No explicit jq invocation appears in the supplied recipes
- No application source, runtime inventory or documented tool contract was provided
- No integration coverage analysis was supplied
- Whether any supported execution path uses jq cannot be determined from this bundle

This does not constitute confirmation that no code path depends on `jq`. The author must affirmatively verify and commit that no runtime behavior, entrypoint logic, override scripts or supported user scenario depends on it before this removal can be approved.

---

## Gates

- **EOL cap:** pass — established track, 2026-12-01 is ~1.4 months out (within 3-month policy for already-onboarded rocks)
- **Track naming:** pass — `1.2-24.04` is correct SemVer format
- **Edge-first:** pass — release restricted to `edge` only
- **Deb-manifest:** pass — correctly configured and present
- **Recipe-regression:** fail — unconfirmed `jq` removal
- **Vulnerability scan:** not assessed locally; verify in CI

---

## Recipe Change Summary

**Prior recipe:** `canonical/demo-rock` @ `0000000000000000000000000000000000000012` / `rocks/demo/rockcraft.yaml`  
**Proposed recipe:** `canonical/demo-rock` @ `0000000000000000000000000000000000000013` / `rocks/demo/rockcraft.yaml`

**Changes:**
- **Packages:** `jq` removed from `app.stage-packages`

All other recipe content is unchanged: base, services, parts (except package list), and scripts remain identical.
