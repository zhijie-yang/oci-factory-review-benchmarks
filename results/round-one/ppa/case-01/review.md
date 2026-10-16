# OCI Factory Code Review: demo rock

**Verdict:** Request changes — The EOL cap is violated; a support plan is required or the end-of-life date must be reduced.

---

## Inline findings

`oci/demo/image.yaml:8` — **[blocker]** EOL cap violation (§2). The main application is upstream-sourced (staged via the Ubuntu archive package `demo-app`). Per §2 EOL cap (MUST), `end-of-life` is at most today (2026-10-16) + 3 months. The proposed date **2027-04-16** is ~6 months from today, exceeding the cap. No accepted support plan or human CODEOWNERS approval is cited in context. Request: either reduce `end-of-life` to 2027-01-16 or earlier, or provide a support plan for maintainer review and approval.

`recipes/after/rockcraft.yaml:27–29` — **[nit]** PPA provenance advisory (§3). The proposed recipe adds `package-repositories` with a PPA declaration. Per §3 guidance, this flags the rock as potentially upstream-sourced. The context notes: "No apt candidate/origin report is supplied for the proposed revision, so the declaration does not tell which, if any, shipped packages would be selected from the PPA." For transparency, the PR should document which shipped packages (if any) are sourced from the PPA `canonical-demo/stable` versus the Ubuntu archive. This does not block the review but clarifies maintainer intent.

---

## Gates

- **eol-cap**: ❌ fail — EOL date violates the 3-month cap for upstream-sourced rocks without an accepted support plan.
- **deb-manifest**: ✅ pass — The recipe correctly declares the `deb-security-manifest` part (both snapshots).
- **recipe-regression**: ✅ pass — No `parts` or `services` entries were dropped. Both recipes include `app` and `deb-security-manifest` parts and the `demo` service.
- **vulnerability-scan**: → not assessed locally; verify in CI.

---

## Summary

The trigger updates the demo rock from commit `0000000000000000000000000000000000000002` to `0000000000000000000000000000000000000003` and extends end-of-life from 2026-12-01 to 2027-04-16 while remaining on track `1.2-24.04` at `edge` risk. The recipe change in the proposed commit is the addition of a PPA repository declaration. The version remains 1.2.0 and the base is unchanged (ubuntu@24.04).

**Comparison note**: Recipe comparison was assessed using the supplied snapshots; both recipes have identical `parts` and `services` structures, with the only code difference being the PPA declaration addition.
