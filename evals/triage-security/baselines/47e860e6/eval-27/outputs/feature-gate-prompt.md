# Feature-Gated Dependency: VEX Justification Prompt (TC-8051)

This prompt is shown to the engineer after the version impact table (Step 2.3.5, dependency scope decision tree) and **before** any remediation tasks are created.

---

> The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification:
> **Vulnerable Code not in Execute Path**.
>
> Evidence:
> - CVE-2026-99002: rustls < 0.23.5 (fixed in 0.23.5), CVSS 8.1 (High)
> - Stream in scope: 2.2.x (`[rhtpa-2.2]`). Versions 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3 and 2.2.4 all lock rustls **0.23.4** in `Cargo.lock`
> - `backend/Cargo.toml`: `rustls = { version = "0.23.4", optional = true }`, enabled only by `tls-rustls = ["dep:rustls"]`
> - `default = ["tls-native"]`. The shipped product uses native-tls, and `tls-rustls` is not a default feature
> - 2.1.x: rustls not present, so not affected
>
> Options:
> 1. Skip remediation: apply VEX justification and close as not affected
> 2. Proceed with remediation: create tasks despite the feature gate
>
> Choose (1/2):

---

## What each option does

**Option 1: Skip remediation (close as not affected)**

All in-scope 2.2.x versions are feature-gated and no other in-scope version is affected, so the whole issue follows Case C. Every proposed Jira change still needs its own confirmation:

1. Comment on TC-8051 with the version impact table and this rationale: rustls 0.23.4 is present in 2.2.x `Cargo.lock` only as an optional dependency behind the non-default `tls-rustls` feature, so the default product build never compiles or runs the vulnerable code. The comment includes the triage-security Comment Footnote.
2. Set the VEX Justification field (`customfield_12345`) to **Vulnerable Code not in Execute Path**.
3. Transition to Closed with resolution **Not a Bug**.
4. Add the `ai-cve-triaged` label and post the post-triage summary, with an @mention of the reporter and the footnote.

**Option 2: Proceed with remediation**

Create standard Case B remediation tasks for the 2.2.x stream. These have no `dev-dependency` label and no priority override. Cargo is a source dependency, so that means 2 tasks:

1. Upstream: bump rustls to >= 0.23.5 in rhtpa-backend on `release/0.4.z`. rustls is a direct dependency, so this is a straight version bump in `backend/Cargo.toml` and `Cargo.lock`. If a `release/0.4.z` HEAD check (Step 2.5) shows the fix is already there, this becomes a dependency-bump task instead.
2. Downstream propagation: update the backend tag reference in rhtpa-release.0.4.z. This task is blocked by task 1.

Both tasks link to TC-8051 with "Depend" and to the release Task from Step 7.5 with "Blocks", if one is active.

No preemptive or cross-stream tasks are needed, because 2.1.x is not affected.

*Waiting for the engineer's choice. No Jira changes have been made.*
