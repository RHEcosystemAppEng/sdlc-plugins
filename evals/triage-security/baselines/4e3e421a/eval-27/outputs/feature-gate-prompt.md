# Feature-Gated Dependency: VEX Justification Prompt (TC-8051)

Presented to the engineer after Step 2.3.5, before any remediation tasks are created
(dependency scope decision tree, feature-gated optional dependencies).

---

> The vulnerable dependency `rustls` (0.23.4, affected range < 0.23.5, CVE-2026-99002)
> is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended
> VEX justification: **Vulnerable Code not in Execute Path**.
>
> Evidence:
> - `backend/Cargo.toml` (v0.4.5+): `rustls = { version = "0.23.4", optional = true }`
> - `[features] default = ["tls-native"]`, so the default build uses `native-tls`
> - `tls-rustls = ["dep:rustls"]` is the only feature that turns on rustls
> - Affected in-scope versions (lock file): 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4
> - 2.1.x: rustls is not present, so it is not affected
>
> Options:
> 1. Skip remediation: apply VEX justification and close as not affected
> 2. Proceed with remediation: create tasks despite the feature gate
>
> Choose (1/2):

---

## What each choice leads to

**Option 1: Skip remediation**
- All in-scope 2.2.x versions are marked not affected. No other stream is affected either
  (2.1.x has no rustls), so the issue goes to **Case C**.
- After confirmation: add a comment with the version impact table and feature-gate
  rationale (including the Comment Footnote), transition TC-8051 to Closed with
  resolution **Not a Bug**, and set VEX Justification (`customfield_12345`) to
  **Vulnerable Code not in Execute Path**.
- Post-triage: add the `ai-cve-triaged` label and post the summary comment that
  @mentions the reporter.

**Option 2: Proceed with remediation**
- **Case B** for stream 2.2.x. Standard remediation tasks are created with no
  `dev-dependency` label and no priority override. Cargo is a source dependency, so
  2 tasks are created: an upstream backport or dependency bump to rustls >= 0.23.5 on
  `release/0.4.z`, plus downstream propagation in rhtpa-release.0.4.z (blocked by the
  first).
- Step 3 would correct Affects Versions from RHTPA 2.2.0 to RHTPA 2.2.0, 2.2.1, 2.2.2,
  2.2.3, and 2.2.4.

Note: "Vulnerable Code not Present" could also be argued, because rustls is not compiled
in under default features. The skill's feature-gate rule recommends
**Vulnerable Code not in Execute Path**, so that is the value proposed. The engineer may
override it.

No Jira mutation was made. The engineer's choice is awaited.
