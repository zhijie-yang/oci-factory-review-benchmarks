# OCI Factory Code Review: demo/image.yaml

**Verdict:** `Request changes` — Recipe snapshots are unavailable; recipe-regression and deb-manifest gates cannot be assessed locally.

---

## Summary

The diff updates `oci/demo/image.yaml` to bump the source commit from `0000000000000000000000000000000000000018` to `0000000000000000000000000000000000000019` in the canonical/demo-rock repository (directory `rocks/demo`). The track `1.2-24.04`, release risk, and EOL date remain unchanged. Per the frozen context, this is a SemVer track on Ubuntu 24.04, edge-only targeting, no support plan has been accepted, and no CVE/vulnerability entries are modified.

**Comparison status:** `not-assessed` — Source recipes unavailable; cannot determine actual recipe deltas or assess recipe-regression or deb-manifest gates.

---

## Static Gate Assessment

### Gate: EOL cap (§2)
**Status:** `fail`

The image declares an `end-of-life` of `2026-12-01` (lines 8, changes.diff). Per frozen context.md (line 12), no accepted support plan or human CODEOWNERS approval has been provided. The §2 rule states: *"if the main application is built from a directly-pulled upstream source … and no support plan has been accepted by a human in CODEOWNERS, end-of-life is at most today + 3 months."*

Today is 2026-10-16 (context.md:3). `2026-12-01` is 46 days away, which exceeds today + 3 months. This violates the EOL cap gate.

**Inline finding:**
- `oci/demo/image.yaml:8` — [blocker] EOL date `2026-12-01` exceeds the maximum allowed cap (today 2026-10-16 + 3 months) without an accepted support plan on file (§2).

---

### Gate: Recipe-regression (§3)
**Status:** `not-assessed`

The prior rockcraft.yaml snapshot (`recipes/before/rockcraft.yaml`) is not supplied. Cannot verify whether the new commit removes any `parts:` or `services:` entries. Per the skill (§3), a missing recipe blocks this gate assessment.

---

### Gate: Deb-manifest (§3)
**Status:** `not-assessed`

The proposed rockcraft.yaml snapshot (`recipes/after/rockcraft.yaml`) is not supplied. Cannot verify whether the recipe adds `.deb` content (via `stage-packages` or build/overlay scripts) or includes the required security-manifest part. The frozen context (lines 33–41) documents that demo-app is a fictional deb staged by name, but the actual recipe structure is unavailable.

---

### Gate: Track naming (§2)
**Status:** `pass`

Track `1.2-24.04` follows the SemVer convention: version (`1.2`) and base (`24.04`). No new or modified tracks are introduced by this diff.

---

### Gate: Edge-first (§2)
**Status:** `pass`

The track targets `- edge` risk only (changes.diff:14). This is consistent with the edge-first rule for SemVer tracks on an established base.

---

### Gate: Vulnerability scan
**Status:** `not-assessed`

Vulnerability scan is CI-only and cannot run locally (skill: *Local dry run*, end of §1).

---

## Findings

### Category: eol-cap
**Severity:** blocker

**Message:**  
The declared `end-of-life` date of `2026-12-01` exceeds the maximum of today + 3 months (2026-10-16 + 90 days ≈ 2027-01-14) required by §2 EOL cap, because no human-approved support plan is on file in CODEOWNERS. Provide a documented support plan or reduce the EOL date to comply with the gate.

**Evidence:**
- `changes.diff:12` — end-of-life declaration
- `context.md:12` — no accepted support plan recorded

---

## Conclusion

This review identifies a gate failure (**EOL cap**) and two unassessable gates (**Recipe-regression** and **Deb-manifest**) due to missing recipe snapshots. Under §1 guidance, a blocker finding triggers `Request changes`. Locally-checkable gates (edge-first, track naming) pass. Offline assessment is limited; resolve the EOL cap and provide recipe snapshots for a complete review.
