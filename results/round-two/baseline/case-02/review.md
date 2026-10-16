# Code Review: demo rock

**Verdict:** Request changes — EOL cap exceeded; requires support plan approval.

## Inline findings

`oci/demo/image.yaml:13` — [blocker] **EOL cap violation (§2)**  
The proposed `end-of-life: '2027-04-16'` extends 6 months from today (2026-10-16), exceeding the 3-month maximum mandated for upstream-sourced rocks without an accepted human support plan in CODEOWNERS. The app part builds directly from canonical/demo-rock (recipes/after/rockcraft.yaml:19–21), making this upstream-sourced. Per §2 release policy, either reduce the EOL to 2027-01-16 (today + 3 months) and request a tracking ticket, or obtain explicit support plan approval documented in CODEOWNERS before proceeding.

## Gates

**Gates:** one-image ✅ · edge-first ✅ · EOL cap ❌ · track naming ✅ · deb-manifest ✅ · recipe-regression ✅ · vulnerability scan → not assessed locally

## Details

- **No recipe regression detected.** The source version bump from 1.2.0 to 1.2.1 is a patch update; services, parts, and build/stage packages are unchanged (compare recipes/before/rockcraft.yaml and recipes/after/rockcraft.yaml).
- **Deb security manifest present.** The recipe correctly includes the mandatory `deb-security-manifest` part sourced from canonical/rocks-security-manifest.
- **Trigger change.** The commit advances from 0000...0004 to 0000...0005 to select the new recipe. The track `1.2-24.04` is correctly named (SemVer without patch, base OS).
