# OCI Factory Code Review

**Verdict:** Request changes

The proposed revision removes `jq` from stage-packages without evidence that the removal is safe. The author claims it is optional and unused, but the supplied context explicitly states that "there is no application source, runtime inventory, documented tool contract or integration coverage for optional JSON-processing paths" and that "Whether any supported path uses jq cannot be determined from this bundle." This constitutes a potential recipe regression—a removal of a package the prior recipe had—without confirmation that the removal is intentional and supported by the application.

---

## Inline Findings

- `recipes/before/rockcraft.yaml:21` — [blocker] Removal of `jq` package without documented evidence of non-use (§3, recipe regression). Per context.md, usage analysis has not been supplied and the tool may be needed by supported runtime paths. Request the author to either restore `jq` or provide a detailed analysis of all runtime paths to confirm jq is not required.

- `recipes/after/rockcraft.yaml` — [blocker] No corresponding application source, runtime documentation, or entrypoint script evidence provided to substantiate the claim that `jq` can be safely removed. Recipe regression gate cannot pass without such evidence or author confirmation.

---

## Gates

**Gates:** EOL cap ✅ · track naming ✅ · deb-manifest ✅ · recipe-regression ❌ · vulnerability-scan → not assessed locally

- **EOL cap:** ✅ pass — The `end-of-life: '2026-12-01'` is within 3 months of today (2026-10-16), and the track remains on the established SemVer base. No human support plan override is required here.
- **Track naming:** ✅ pass — The `1.2-24.04` track key follows the SemVer pattern (version without patch, hyphen, base version).
- **Deb-manifest:** ✅ pass — The recipe includes the required `deb-security-manifest` part sourced from the canonical rocks-security-manifest repository, wired correctly.
- **Recipe-regression:** ❌ fail — The removal of `jq` from `stage-packages` (recipes/before:21 → absent in recipes/after) without documented confirmation of non-use violates §3. The prior recipe had this entry; the proposed recipe removes it, and the author's claim of optional status cannot be verified from the supplied material (context.md:45–49).
- **Vulnerability-scan:** not assessed locally — Not run during local dry run; verify in CI.

---

## Summary

The change is a commit bump (0000000000000000000000000000000000000012 → 0000000000000000000000000000000000000013) in `oci/demo/image.yaml`, reflecting a source-recipe update that removes `jq` from stage-packages. No other trigger, package, service, part, version, base or repository changes are present. The removal is the only recipe delta between the two supplied snapshots and is not supported by evidence in the bundle.
