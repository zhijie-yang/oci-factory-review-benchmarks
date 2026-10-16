# OCI Factory Local Review

**Verdict:** Approve. The recipe-regression gate passes with documented intent; all other locally-checkable gates pass.

## Inline findings

### `oci/demo/image.yaml:4` — [nit] Recipe parts reduction documented (§3)

The source bump from `000000000000000000000000000000000a` to `000000000000000000000000000000000b` drops the `build-marker` part. The skill requires recipe regressions (dropped `parts:` or `services:` entries) to be confirmed intentional by the author before approval.

**Evidence:** The frozen upstream commit message states *'Intentionally remove the unused build-marker part.'* and the PR author explicitly confirms: *'I confirm that removing build-marker is intentional. It is an empty nil part with no outputs or users; please retain its removal in this source update.'* The synthetic evidence confirms build-marker is a nil part with no source, packages, scripts or output, and no other part has an ordering dependency on it. The removal changes neither the installed filesystem nor the service execution contract.

This is not a blocker: the regression is intentional and isolated.

---

## Gates

**Gates:** edge-first ✅ · EOL cap ✅ · track naming ✅ · deb-manifest ✅ · recipe-regression ✅ · one-image ✅ · vuln scan → not assessed locally; verify in CI

- **edge-first:** Not a new track, base or rock; an existing SemVer track (`1.2-24.04`) receives a source bump within the same version range. ✅
- **EOL cap:** Track is `1.2-24.04` (Ubuntu 24.04 LTS); EOL is `2026-12-01` (~45 days from freeze date). The main application (`demo-app`) is a staged Ubuntu archive deb, not upstream-sourced; no EOL cap restriction applies. ✅
- **track naming:** `1.2-24.04` follows SemVer format correctly (major.minor-base), omitting patch as required. ✅
- **deb-manifest:** Recipe uses `stage-packages: [demo-app]` and includes the mandated `deb-security-manifest` part per §3 spec. ✅
- **recipe-regression:** The `build-marker` part is dropped; the author confirms intentionality and upstream sources the removal. Evidence confirms no runtime impact. ✅
- **one-image:** Only `oci/demo/` is touched. ✅
- **vuln scan:** Not assessed locally; run passes in CI before merging.

---

## Summary

The trigger bumps a single OCI image's source commit within an existing, stable release track. The underlying recipe removes an unused nil part (`build-marker`) per explicit upstream and author intent. No other recipe, release policy, or documentation changes are present. All local gates pass.
