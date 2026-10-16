# OCI Factory Code Review: demo image

**Verdict:** Request changes. The proposed EOL date violates the 3-month cap, and the added PPA declaration lacks evidence of package provenance.

## Findings

### EOL cap violation [blocker] (§2)

`oci/demo/image.yaml:8` — The proposed end-of-life date **2027-04-16** exceeds the permitted maximum. Per the EOL cap rule (§2), an application built from a directly-pulled upstream source or (as here) an archived deb without an accepted support plan must have end-of-life at most today + 3 months. Today is 2026-10-16; the cap is 2027-01-16. The proposed date 2027-04-16 is 3 months beyond the limit.

**Action required:** Either provide an accepted human support plan in `CODEOWNERS` (which would lift the cap), or reduce the end-of-life date to 2027-01-16 or earlier.

### Additional package repositories — provenance unclear [blocker] (§3 advisory)

`recipes/after/rockcraft.yaml:27–29` — The source bump introduces a new `package-repositories` declaration (`canonical-demo/stable`). Per §3, this signals potential upstream sourcing and requires clarification. The context states (line 48–49) that no apt candidate/origin report is supplied for the proposed revision, so the declaration does not tell which, if any, shipped packages would be selected from the PPA.

**Action required:** Provide an apt candidate/origin report showing which packages, if any, are sourced from the PPA rather than the Ubuntu archive. If the PPA is unused (no packages come from it), consider removing the declaration.

## Recipe comparison

The source commit `0000000000000000000000000000000000000002` → `0000000000000000000000000000000000000003` is a source bump. Recipe changes:

- **Added:** `package-repositories` declaration with a single PPA entry.
- **Preserved:** `parts` (app, deb-security-manifest), `services` (demo), `base` (ubuntu@24.04).
- **No regression detected:** All prior parts and services remain.

## Gates

- **eol-cap:** ❌ fail — proposed end-of-life exceeds 3-month limit
- **deb-manifest:** ✅ pass — `deb-security-manifest` part present in recipe
- **recipe-regression:** ✅ pass — no parts or services dropped
- **vulnerability-scan:** → not assessed locally (CI-only)

---

**Summary:** The source revision and EOL updates are requested, but the EOL date must be corrected to meet the 3-month cap, and the added PPA requires evidence of actual package sourcing to proceed.
