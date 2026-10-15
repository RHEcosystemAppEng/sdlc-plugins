# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. This maps to the **Cargo** ecosystem per the Ecosystem Mappings tables in both streams' `security-matrix.md`.

- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Category: **Source dependency**
- Remediation tasks per stream: **2** (upstream fix + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories with deployment context defaulting to **upstream** (no Deployment Context column present in the table).

## Verification

All critical fields successfully parsed:
- CVE ID: CVE-2026-31812
- Library: quinn-proto
- Affected range: < 0.11.14
- Fixed version: 0.11.14

No missing critical fields. Proceeding with triage.
