# OCI Factory Code Review

**Verdict:** Request changes. A service removal without author confirmation is a recipe regression blocker (§3).

## Findings

### Recipe regression [blocker] (§3)

`recipes/after/rockcraft.yaml:11-19` — The `demo-info` service is removed from the proposed recipe. The prior recipe (`recipes/before/rockcraft.yaml:16-19`) declares this service with `startup: disabled`. Per the skill's recipe regression rule, dropping a `services:` entry requires either restoration or explicit PR-author confirmation in the PR discussion that the removal is intentional. The context confirms: "No PR-author confirmation of the demo-info service removal is present." The removal must be justified by the author in the PR before this can be approved.

## Changes detected

- **services:** demo-info removed
- **parts:** none
- **packages:** none
- **scripts:** none
- **version:** none
- **repositories:** none

## Gate assessments

**Gates:** eol-cap ✅ · deb-manifest ✅ · recipe-regression ❌ · vulnerability-scan → not assessed locally

- **eol-cap:** PASS. End-of-life is 2026-12-01, within 3 months of 2026-10-16. The main application is the demo-app deb from Ubuntu archive, not directly upstream-sourced, so the cap applies and is satisfied.
- **deb-manifest:** PASS. The recipe includes a correctly-wired `deb-security-manifest` part sourced from `https://github.com/canonical/rocks-security-manifest` on the main branch.
- **recipe-regression:** FAIL. The `demo-info` service is removed without PR-author confirmation, violating §3.
- **vulnerability-scan:** not-assessed. Local review does not execute vulnerability scans; verify in CI.

## Summary

The trigger diff changes `upload.directory` from `rocks/old` to `rocks/new` at the same commit. The recipe snapshots differ only in the removal of the `demo-info` service. According to evidence, this was an on-demand disabled service using the same binary as the primary service, with no dependency relationship. However, without author confirmation of intentional removal, this constitutes a recipe regression and must be resolved before approval.
