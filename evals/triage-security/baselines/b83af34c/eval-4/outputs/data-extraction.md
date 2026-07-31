# Data Extraction — TC-8004

## Step 1: Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(none — no stream suffix in summary)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | versions before 0.4.8 |
| Fixed version | 0.4.8 |
| Upstream fix PR | [hyperium/h2#812](https://github.com/hyperium/h2/pull/812) |
| Advisory URL | [GHSA-2026-kv8p-r3n7](https://github.com/advisories/GHSA-2026-kv8p-r3n7) |
| CVE record URL | [CVE-2026-33501](https://www.cve.org/CVERecord?id=CVE-2026-33501) |
| Due date | 2026-08-01 |
| Existing comments | None |
| CVSS | 7.5 (High) |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" contains **no stream suffix** in brackets. Per the skill's Stream scope resolution rules (Step 1), this issue is treated as **unscoped** — it covers all configured version streams.

- Configured streams from Security Configuration Version Streams table:
  - 2.1.x (rhtpa-release.0.3.z)
  - 2.2.x (rhtpa-release.0.4.z)
- Issue stream scope: **unscoped — analyze all streams**

All versions across both 2.1.x and 2.2.x streams will be checked in Step 2.

## Ecosystem Detection

- Library: h2 (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Classification: Source dependency ecosystem -> 2 remediation tasks per affected stream (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

- Affected repository: rhtpa-backend
- Source Repositories table entry: rhtpa-backend -> URL: https://github.com/rhtpa/rhtpa-backend
- Deployment Context column: absent from Source Repositories table (no Deployment Context column configured)
- Result: coordination guidance will be omitted (backward compatibility)
