# OCI Factory Code Review: demo rock

**Verdict:** Approve, with recipe-regression gate not assessed due to unavailable source snapshots.

## Summary

The proposed change updates the source commit in `oci/demo/image.yaml` from commit `0000000000000000000000000000000000000018` to `0000000000000000000000000000000000000019`, within the established `1.2-24.04` edge-only track on Ubuntu 24.04. No version, track, base, documentation, or policy changes are present in the trigger diff.

## Locally-Checkable Gates

**Gates:** edge-first ✅ · EOL cap ✅ · track naming ✅ · deb-manifest not-assessed · recipe-regression not-assessed · vuln scan → not-assessed locally

## Inline Findings

### Recipe comparison unavailable
`oci/demo/image.yaml` triggers a source commit update. Per §3 (Source recipe), the reviewer must fetch and compare `rockcraft.yaml` at both commits under `canonical/demo-rock` at `rocks/demo/` to assess for recipe regressions and deb-manifest compliance. Neither snapshot is available in this offline bundle.

- **Impact:** Recipe-regression and deb-manifest gates cannot be assessed.
- **Required action:** Verify locally before push, or provide recipe snapshots in CI logs. The review gates remain at not-assessed until evidence is available.

## Assessment Details

1. **Edge-first (§2):** The track `1.2-24.04` is an established track with only edge risk targeted; edge-first does not apply. ✅

2. **EOL cap (§2):** The `end-of-life: '2026-12-01'` (today + 1 month, 15 days) satisfies the 3-month cap without requiring a support plan. ✅

3. **Track naming (§2):** The track key `1.2-24.04` follows the correct `<version>-<base>` pattern for SemVer 1.2.x. ✅

4. **Deb-manifest (§3):** Cannot verify. Recipes not provided.

5. **Recipe regression (§3):** Cannot verify. Recipes not provided. A source bump warrants inspection of both recipes to detect dropped parts, services, or concerning package/script changes. Re-request this assessment with recipe evidence.

## Gates Summary

| Gate | Status | Reasoning |
|------|--------|-----------|
| edge-first | pass | Established track, edge-only already in place |
| EOL cap | pass | 2026-12-01 is within 3-month cap from 2026-10-16 |
| track naming | pass | 1.2-24.04 follows SemVer `<version>-<base>` pattern |
| deb-manifest | not-assessed | Source recipes unavailable |
| recipe-regression | not-assessed | Source recipes unavailable |
| vulnerability-scan | not-assessed | CI-only gate, local review does not assess |

---

**Next steps:** If proceeding to push, the source recipes should be reviewed locally or CI logs should be examined to confirm the recipe-regression and deb-manifest gates before merging.
