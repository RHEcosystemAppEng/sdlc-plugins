# Feature-Gated Dependency — VEX Justification Prompt

Issue: TC-8051 — CVE-2026-99002 (rustls < 0.23.5), stream 2.2.x

Shown to the engineer after the version impact table (Step 2.3.5 dependency scope decision tree) and **before** any remediation tasks are created:

---

> "The vulnerable dependency `rustls` is gated behind the `tls-rustls`
> feature, which is not enabled by default. Recommended VEX justification:
> **Vulnerable Code not in Execute Path**.
>
> Options:
> 1. Skip remediation — apply VEX justification and close as not affected
> 2. Proceed with remediation — create tasks despite the feature gate
>
> Choose (1/2):"

---

## Supporting evidence presented with the prompt

| Item | Evidence |
|------|----------|
| Affected versions (by lock file) | 2.2.0, 2.2.1, 2.2.2 (retag of 2.2.1), 2.2.3, 2.2.4 — all rustls 0.23.4 |
| Dependency type | Direct, `optional = true` in `backend/Cargo.toml` |
| Enabling feature | `tls-rustls = ["dep:rustls"]` (non-default) |
| Default features | `default = ["tls-native"]` → native-tls; does NOT include `tls-rustls` |
| Other streams | 2.1.x does not contain rustls — no cross-stream impact |
| VEX field | `customfield_12345` (configured) |

## Outcome of each option

- **Option 1 (Skip remediation)**: Because every in-scope (2.2.x) version is feature-gated and no other stream is affected, this leads to Case C — after explicit confirmation, comment on TC-8051 with the version impact table and rationale (with the Comment Footnote), transition to Closed with resolution "Not a Bug", and set `customfield_12345` = **Vulnerable Code not in Execute Path**.
- **Option 2 (Proceed with remediation)**: Case B for stream 2.2.x — create standard remediation tasks (Cargo source dependency → 2 tasks: upstream backport or dependency bump to rustls >= 0.23.5 on `release/0.4.z`, plus blocked downstream propagation to `rhtpa-release.0.4.z`), with **no** `dev-dependency` label and **no** priority override.

No Jira mutation is performed until the engineer chooses and confirms.
