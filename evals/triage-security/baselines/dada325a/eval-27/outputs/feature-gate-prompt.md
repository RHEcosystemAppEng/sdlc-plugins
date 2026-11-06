# Feature-Gated Dependency: VEX Justification Prompt (TC-8051)

Shown to the engineer after Step 2.3.5. Per the dependency scope decision tree, this must come **before** any remediation tasks are created.

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
| CVE | CVE-2026-99002 (CVSS 8.1 High): rustls certificate validation bypass |
| Affected range / fix | rustls < 0.23.5 / fixed in 0.23.5 |
| Stream in scope | 2.2.x (`[rhtpa-2.2]`) |
| Versions with rustls in Cargo.lock | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4. All at rustls 0.23.4 |
| Dependency type | Direct, `optional = true` in backend/Cargo.toml |
| Gating feature | `tls-rustls = ["dep:rustls"]` |
| Default features | `default = ["tls-native"]`, which does **not** include `tls-rustls` |
| Shipped TLS backend | native-tls (via default `tls-native`) |
| Other streams | 2.1.x: rustls not present, so not affected |
| VEX field | customfield_12345 (configured) |

## Outcome of each choice

**Option 1: Skip remediation (recommended)**
- Mark 2.2.0–2.2.4 as not affected, with VEX justification **Vulnerable Code not in Execute Path**.
- No other in-scope versions are affected, and 2.1.x is not affected (Component not Present). The overall result is **Case C**: close TC-8051 as **Not a Bug**, set customfield_12345 = "Vulnerable Code not in Execute Path", and post a closure comment with the version impact table, the feature-gate rationale and the Comment Footnote. Each Jira mutation needs separate confirmation.
- No remediation tasks are created. Before closing, check that the shipped Konflux build does not enable `tls-rustls`, for example with `--features tls-rustls` or `--all-features` in the build config.

**Option 2: Proceed with remediation**
- **Case B** for the 2.2.x stream, Cargo source dependency: create 2 tasks, a dependency bump or upstream backport (rustls to >= 0.23.5, direct dep in backend/Cargo.toml) and a downstream Konflux propagation task blocked by the first. The choice between bump and backport depends on the upstream `release/0.4.z` status.
- These are standard remediation tasks: **no** `dev-dependency` label and **no** priority override.
- Correct Affects Versions to RHTPA 2.2.0–2.2.4 (Step 3).
- No Case A cross-stream tasks, because 2.1.x is not affected.
