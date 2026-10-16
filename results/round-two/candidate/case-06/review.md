# OCI Factory Local Review: demo

**Verdict:** Request changes — the proposed recipe removes a runtime dependency required by the service command.

## Inline findings

`recipes/after/rockcraft.yaml:19-20` — [blocker] The `tini` package has been removed from `stage-packages`, but the enabled service command at `recipes/after/rockcraft.yaml:14` depends on `/usr/bin/tini`. Evidence confirms the proposed filesystem contains no `/usr/bin/tini`, symlink, or alternative tini binary; no transitive dependency provides it. The service will fail at startup. Restore `tini` to `stage-packages` or confirm in the PR that this removal is intentional and the command has been updated. (§3 recipe regression)

## Gates

**Gates:** deb-manifest ✅ · recipe-regression ❌ · EOL cap ✅ · vuln scan → not assessed locally

- **deb-manifest:** pass — security-manifest part present in both recipes
- **recipe-regression:** fail — required runtime dependency `tini` removed; service command unmodified
- **eol-cap:** pass — end-of-life 2026-12-01 within acceptable window; demo-app is archive-sourced, no support plan required
- **vulnerability-scan:** not assessed locally

## Recipe change summary

The source bump (commit 000000000000...000d) removes `tini` from the app part's `stage-packages` list. All other recipe elements (base, services, manifest) are unchanged. The service command remains `/usr/bin/tini -- /usr/bin/demo serve`.
