# Step 1 -- Data Extraction: TC-8020

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Issue Key | TC-8020 |
| Summary | CVE-2026-55123 tokio - Use-after-free in task abort [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Stream Suffix | [rhtpa-2.2] |
| Stream Scope | 2.2.x (mapped to rhtpa-release.0.4.z) |
| Vulnerable Library | tokio |
| Affected Version Range | versions before 1.42.0 |
| Fixed Version | 1.42.0 |
| CVSS | 8.1 (High) |
| Affects Versions (PSIRT) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Due Date | 2026-08-15 |
| Assignee | Unassigned |
| Labels | CVE-2026-55123, pscomponent:org/rhtpa-server |
| Upstream Fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE Record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Existing Comments | None |
| Existing Issue Links | None |

## Ecosystem Detection

- **Ecosystem**: Cargo (Rust crate)
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Source Repository**: backend (rhtpa-backend)

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). Triage is scoped to this stream for Affects Versions correction (Step 3) and remediation task creation (Case A). Cross-stream impact analysis (Case B) covers stream 2.1.x as well.
