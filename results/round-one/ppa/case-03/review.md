# Code Review: demo image trigger update

**Verdict:** Request changes — Recipe regression gate fails: `build-marker` part removal lacks PR-author confirmation.

## Inline Comments

`oci/demo/image.yaml:8` — [blocker] Source commit bumps from prior `0000000000000000000000000000000000000006` to `0000000000000000000000000000000000000007`, and the proposed recipe drops the `build-marker` part that the prior recipe had (recipes/before:27–28 vs recipes/after). §3 requires that until the part is restored or the PR author confirms removal is intentional, the revision stays at edge. The upstream commit message states the removal is intentional, but the PR description contains only "Update the source commit"—no explicit author ratification of the part removal. Please confirm in the PR thread that dropping `build-marker` is intentional.

## Gates

**eol-cap** ✅ · **deb-manifest** ✅ · **recipe-regression** ❌ · **vulnerability-scan** → not assessed locally

- **eol-cap**: PASS – Track `1.2-24.04` with end-of-life `2026-12-01` satisfies the 3-month cap (fixture date: 2026-10-16). Main application is archived deb, not upstream-sourced.
- **deb-manifest**: PASS – Recipe includes `deb-security-manifest` part (canonical/rocks-security-manifest) as required for deb staging.
- **recipe-regression**: FAIL – `build-marker` part (prior recipe lines 27–28) is removed in proposed recipe with no PR-author confirmation per §3.
- **vulnerability-scan**: not assessed locally; verify in CI.

## Summary

Commit bump to proposed recipe removes `build-marker` nil part. Evidence notes removal has no functional impact. Upstream commit message documents intent. PR description does not confirm author agrees. Per policy, explicit author confirmation is required before proceeding.
