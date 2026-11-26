# Feature-Gated Dependency – VEX Justification Prompt (TC-8051)

Dependency scope decision tree (Step 2.3.5) classified rustls as a **feature-gated optional dependency**: declared in `[dependencies]` with `optional = true` in backend/Cargo.toml and only enabled by the non-default `tls-rustls` feature (`default = ["tls-native"]`). Affects all in-scope versions 2.2.0–2.2.4 (rustls 0.23.4 < 0.23.5); 2.1.x does not ship rustls.

Prompt presented to the engineer before any remediation task creation:

---

> The vulnerable dependency `rustls` is gated behind the `tls-rustls`
> feature, which is not enabled by default. Recommended VEX justification:
> **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. Skip remediation — apply VEX justification and close as not affected
> 2. Proceed with remediation — create tasks despite the feature gate
>
> Choose (1/2):

---

## Context for the decision

| Item | Value |
|---|---|
| CVE | CVE-2026-99002 (CVSS 8.1 High) — rustls certificate validation bypass |
| Library / range | rustls < 0.23.5 (fixed in 0.23.5) |
| Shipped version | rustls 0.23.4 in Cargo.lock of 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4 |
| Gate | `tls-rustls = ["dep:rustls"]` — non-default |
| Default TLS backend | `tls-native` (native-tls) |
| Recommended VEX justification | Vulnerable Code not in Execute Path |
| VEX custom field | customfield_12345 |

## Consequences of each choice

**Option 1 — Skip remediation (VEX close):**
Since every in-scope 2.2.x version would be marked not affected and no other stream ships rustls, the whole issue falls under Case C. After separate confirmation of each Jira mutation:
1. Comment on TC-8051 with the version impact table, the feature-gate rationale, and the Comment Footnote.
2. Transition TC-8051 to Closed, resolution "Not a Bug".
3. Set customfield_12345 (VEX Justification) = "Vulnerable Code not in Execute Path".
4. Add the `ai-cve-triaged` label and post the post-triage summary (with reporter @mention and footnote).

**Option 2 — Proceed with remediation:**
Case B for stream 2.2.x. Create standard remediation tasks (no `dev-dependency` label, no priority override). That means 2 Cargo tasks: an upstream backport, or a dependency bump if Step 2.5 shows release/0.4.z already ships rustls >= 0.23.5, plus downstream propagation in rhtpa-release.0.4.z. Link them to TC-8051 with "Depend", and link upstream to downstream with "Blocks". Correct Affects Versions to RHTPA 2.2.0–2.2.4 in Step 3.

Awaiting engineer choice. No Jira mutations performed.
