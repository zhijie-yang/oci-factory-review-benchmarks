# OCI Factory Local Review

**Verdict:** Request changes — the proposed EOL end-date exceeds the 3-month cap without an approved support plan.

## Findings

`oci/demo/image.yaml:13` — [blocker] EOL cap violation (§2). The `end-of-life` date 2027-04-16 is 6 months from today (2026-10-16), exceeding the 3-month maximum. Context states: "There is no accepted support plan or human CODEOWNERS approval of one." A support plan must be accepted by a human in CODEOWNERS before a longer EOL can be set. Update the date to 2027-01-16 or less, or open a parallel discussion with maintainers to accept a support plan.

`recipes/after/rockcraft.yaml:27–29` — [nit] PPA opacity (§3). The new `package-repositories` section declares `canonical-demo/stable` but context notes: "No apt candidate/origin report is supplied for the proposed revision, so the declaration does not tell which, if any, shipped packages would be selected from the PPA." This is informational; clarify in the PR description which packages are expected to be sourced from the PPA and why the change is necessary. Not a blocker, but transparency aids review.

## Gate Summary

- **eol-cap:** ❌ fail — exceeds 3-month cap without approved support plan  
- **deb-manifest:** ✅ pass — `deb-security-manifest` part present and correctly wired  
- **recipe-regression:** ✅ pass — no parts or services dropped between revisions  
- **vulnerability-scan:** → not assessed locally; verify in CI  

## Recipe Changes

- **repositories:** PPA `canonical-demo/stable` added to `package-repositories`  
- **version:** `end-of-life` extended from 2026-12-01 to 2027-04-16  

## Summary

The source bump (commit 0000000000000000000000000000000000000003) introduces a PPA and extends the EOL window. Recipe structure is sound: both `app` and `deb-security-manifest` parts are retained, and no regression is detected. However, the EOL date violates the 3-month cap (§2) without documented support-plan acceptance. Request changes to cap the EOL at 2027-01-16 or provide evidence of an approved support plan from CODEOWNERS.
