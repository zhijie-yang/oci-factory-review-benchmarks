# OCI Factory Code Review

**Verdict: Request changes**

The proposed source revision includes an EOL extension that exceeds the allowed 3-month cap without an accepted support plan, and introduces a package repository without sufficient provenance evidence. Both issues require clarification.

---

## Inline Findings

**`oci/demo/image.yaml:8` — [blocker] EOL cap violation (§2)**

The end-of-life date is extended to 2027-04-16 (~6 months forward from today). Per §2, without an accepted support plan in `CODEOWNERS`, `end-of-life` must not exceed today + 3 months. The application (demo-app 1.2.0) is staged from the Ubuntu archive, not built from an upstream source, so no upstream support rationale applies. Either reduce the EOL to comply with the cap, or provide an accepted support plan for approval.

**`recipes/after/rockcraft.yaml:27–29` — [blocker] PPA provenance unspecified (§3)**

The proposed recipe adds a package repository declaration (`canonical-demo/stable` PPA). Per §3, this must be flagged as potentially upstream-sourced. No apt candidate/origin report is supplied to establish which shipped packages, if any, come from the PPA vs. the Ubuntu archive. Clarify the package provenance: which packages (if any) will be selected from the PPA?

---

## Recipe Comparison

**Changed categories:** repositories, version (EOL only)

**Prior recipe** (commit `0000000000000000000000000000000000000002`):
- Parts: `app` (nil plugin, stage-packages: demo-app), `deb-security-manifest`
- Services: `demo` (override: replace, command: /usr/bin/demo serve, startup: enabled)
- Packages: demo-app (Ubuntu archive)
- No package repositories declared

**Proposed recipe** (commit `0000000000000000000000000000000000000003`):
- Parts: `app`, `deb-security-manifest` (unchanged)
- Services: `demo` (unchanged)
- Packages: demo-app (archive + PPA, provenance unspecified)
- Added: `package-repositories` section with `canonical-demo/stable` PPA

**Assessment:** No parts or services removed; no regression detected in content or runtime behavior. PPA addition is the only recipe change. Deb-security-manifest requirement is met. EOL extension and PPA provenance remain blockers.

---

## Gates

- **EOL cap:** ❌ fail — 6-month extension exceeds 3-month cap without accepted support plan
- **Deb-manifest:** ✅ pass — security-manifest part present and correctly configured
- **Recipe-regression:** ✅ pass — no parts, services, or core packages removed
- **Vulnerability-scan:** → not assessed locally; verify in CI
