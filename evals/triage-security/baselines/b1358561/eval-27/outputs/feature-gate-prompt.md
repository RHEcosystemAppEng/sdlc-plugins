# Feature-Gated Dependency: VEX Justification Prompt (TC-8051)

Shown to the engineer after the version impact table (Step 2.3.5, dependency scope decision tree) and **before** any remediation tasks are created.

---

> The vulnerable dependency `rustls` is gated behind the `tls-rustls` feature, which is not enabled by default. Recommended VEX justification:
> **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. Skip remediation — apply VEX justification and close as not affected
> 2. Proceed with remediation — create tasks despite the feature gate
>
> Choose (1/2):

---

## Supporting evidence shown with the prompt

| Item | Detail |
|------|--------|
| CVE | CVE-2026-99002 (rustls < 0.23.5, CVSS 8.1 High). Certificate validation bypass with custom certificate verifiers. |
| Stream scope | 2.2.x (`[rhtpa-2.2]`) |
| Versions with rustls in Cargo.lock | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4. All at rustls 0.23.4. |
| Dependency type | Direct, `optional = true` in backend/Cargo.toml |
| Gating feature | `tls-rustls = ["dep:rustls"]` (non-default) |
| Default features | `default = ["tls-native"]`, which uses native-tls. rustls is not compiled into the default product build. |
| Other streams | 2.1.x does not contain rustls, so there is no cross-stream impact |
| VEX field | customfield_12345 (configured in Security Configuration) |

## What each choice does (after a separate confirmation gate before any Jira mutation)

**Option 1: skip remediation (VEX close)**
- Mark 2.2.0–2.2.4 as not affected with VEX justification "Vulnerable Code not in Execute Path". No other in-scope version is affected, so the whole issue goes to Case C.
- Proposed Jira actions, each confirmed before running:
  1. Comment saying no supported 2.2.x version ships rustls in its default execute path. rustls 0.23.4 is in Cargo.lock only as an optional dependency behind the non-default `tls-rustls` feature. Includes the version impact table and the triage-security Comment Footnote.
  2. Transition TC-8051 to Closed with resolution "Not a Bug".
  3. Set customfield_12345 to "Vulnerable Code not in Execute Path".
  4. Add the `ai-cve-triaged` label and post the summary comment, @mentioning the reporter.

**Option 2: proceed with remediation**
- Case B for 2.2.x. Correct Affects Versions to RHTPA 2.2.0–2.2.4. Create the standard two Cargo remediation tasks: a rustls bump to >= 0.23.5 on `release/0.4.z` (dependency bump or upstream backport, depending on the upstream fix check), plus downstream propagation in rhtpa-release.0.4.z, linked with Blocks.
- No `dev-dependency` label and no priority override. These are standard tasks.
- Link the tasks to TC-8051 with Depend, and to the release Task from Step 7.5 if there is one.

_Awaiting engineer choice (1/2). No Jira mutations have been performed._
