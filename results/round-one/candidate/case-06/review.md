# OCI Factory Code Review

**Verdict:** Request changes — The proposed recipe removes the `tini` package without updating the service command that depends on it, creating a runtime failure.

## Findings

### Recipe Regression — `tini` runtime dependency removed [blocker]

`recipes/after/rockcraft.yaml:20` — The `tini` package has been dropped from `stage-packages`, but `recipes/after/rockcraft.yaml:14` still executes the service command `/usr/bin/tini -- /usr/bin/demo serve`. Per evidence.md, the prior image contained `/usr/bin/tini` at that path, and the proposed image will not have it—no alternative source supplies the binary.

**Action required:** Either restore the `tini` package in `stage-packages`, or update the service `command` to remove the dependency. If this removal is intentional, the author must confirm in the PR and justify the runtime behavior change.

## Gates

- **EOL cap:** n/a — No support plan evaluation applies to this local review; context.md confirms no plan has been accepted.
- **Deb manifest:** pass — The recipe correctly includes the `deb-security-manifest` part (recipe line 21–26).
- **Recipe regression:** fail — Package removal breaks the service command.
- **Vulnerability scan:** not-assessed — Local review does not include vulnerability scanning; verify in CI.

## Recipe change summary

The source bump (commit `000000000000000000000000000000000000000c` → `000000000000000000000000000000000000000d`) changes only the `stage-packages` list in the `app` part: `tini` has been removed. The service command, run-user, and all other recipe elements are unchanged.
