# Code Review: changes.diff

**Verdict: Request changes.** A service is removed from the recipe without the author's explicit confirmation required by this policy.

## Inline Comments

`oci/demo/image.yaml:5` — [blocker] The proposed recipe at `rocks/new` removes the `demo-info` service that existed in `rocks/old` (recipes/before/rockcraft.yaml:16–19 vs recipes/after/rockcraft.yaml). Per §3, service removal in a source bump requires explicit author confirmation in the PR that the removal is intentional. No such confirmation is present in the supplied discussion; the author only states "Use the other recipe directory." Until confirmed, restore the service or obtain that confirmation in the PR. (§3)

## Recipe Change Summary

Both recipes use base `ubuntu@24.04` and the same application part structure. The only substantial difference is the removal of the `demo-info` service:

- **Before (rocks/old):** Services: `demo` (enabled) and `demo-info` (disabled, command: `/usr/bin/demo --print-version`)
- **After (rocks/new):** Services: `demo` (enabled only)

Parts, packages, and `override-*` scripts are otherwise identical. Version remains `1.2.0`. The deb-security-manifest part is present in both.

## Gates

- **EOL cap:** n/a (application is from Ubuntu archive `demo-app`, not directly-pulled upstream source; §2)
- **Deb-manifest:** ✅ (present and correctly configured in both recipes; §3)
- **Recipe-regression:** ❌ (service removal unconfirmed; §3)
- **Vulnerability-scan:** not-assessed (local review; CI will verify)

## Summary

The diff moves the image trigger from `rocks/old` to `rocks/new` at the same commit. The new recipe removes the `demo-info` service (an on-demand, disabled informational service with no dependency from the primary service). This removal is unconfirmed by the author and is a policy blocker until resolved.
