# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Assignee | engineer-a@example.com |
| Status | In Progress |
| Labels | CVE-2026-31812, pscomponent:org/rhtpa-server, ai-cve-triaged |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in Security Configuration. This issue is **scoped** to the 2.2.x stream only (Konflux release repo: `rhtpa-release.0.4.z`).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is a source dependency ecosystem. Per the ecosystem classification table, this produces **2 remediation tasks per stream**: upstream backport + downstream propagation.

## Existing Issue Links

| Link Type | Issue | Summary | Status |
|-----------|-------|---------|--------|
| Depend | TC-8100 | Backport quinn-proto fix to >= 0.11.14 on release/0.4.z [rhtpa-2.2] | In Progress |
| Depend | TC-8101 | Propagate quinn-proto bump to rhtpa-server release branch [rhtpa-2.2] | Open |

## Existing Comments

1. **Description digest comment**: `sha256-md:a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2` (posted 2026-07-01T10:00:00Z by sdlc-workflow/triage-security)
2. **Post-triage summary**: Documents version impact (RHTPA 2.2.0/2.2.1 affected, 2.2.2+ not affected), actions taken (Affects Versions corrected, ai-cve-triaged label added, remediation tasks TC-8100/TC-8101 created, transitioned to In Progress). Posted 2026-07-01T10:01:00Z.

## Version Impact (from security-matrix mock data)

| Version | Build Tag | quinn-proto version | Affected? |
|---------|-----------|---------------------|-----------|
| RHTPA 2.2.0 | v0.4.5 | 0.11.9 | YES (< 0.11.14) |
| RHTPA 2.2.1 | v0.4.8 | 0.11.12 | YES (< 0.11.14) |
| RHTPA 2.2.2 | v0.4.9 | 0.11.12 (retag of v0.4.8) | YES (< 0.11.14) |
| RHTPA 2.2.3 | v0.4.11 | 0.11.14 | NO (>= 0.11.14) |
| RHTPA 2.2.4 | v0.4.12 | 0.11.14 | NO (>= 0.11.14) |

Note: The prior triage summary states RHTPA 2.2.2 is "not affected" -- the lock file data shows v0.4.9 is a retag of v0.4.8 (which ships 0.11.12, still below 0.11.14). This is a data point from the matrix but does not change the triage outcome since RHTPA 2.2.2 was already superseded by 2.2.3+.
