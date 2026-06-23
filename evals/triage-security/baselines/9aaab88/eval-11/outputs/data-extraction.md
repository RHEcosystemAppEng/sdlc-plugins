# Step 1 — Data Extraction: TC-8021

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-55123 |
| **Issue Key** | TC-8021 |
| **Status** | New |
| **Affected Component** | pscomponent:org/rhtpa-server |
| **Product Version (PSIRT-claimed)** | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| **Affects Versions (Jira field)** | RHTPA 2.1.0, RHTPA 2.1.1 |
| **Vulnerable Library** | tokio |
| **Affected Version Range** | versions before 1.42.0 |
| **Fixed Version** | 1.42.0 |
| **CVSS** | 8.1 (High) |
| **Upstream Fix PR** | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| **Advisory URL** | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| **CVE Record URL** | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| **Due Date** | 2026-08-15 |
| **Existing Comments** | None |

## Custom Fields

| Field | Value |
|-------|-------|
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.1 |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.1]`
- Mapped stream: **2.1.x** (Konflux release repo: `rhtpa-release.0.3.z`)
- Issue is **stream-scoped** to 2.1.x only

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Source repository: rhtpa-backend
- Upstream branch: `release/0.3.z`
