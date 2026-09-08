# Step 1 -- Data Extraction: TC-8003

## Extracted CVE Metadata

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the
configured Version Stream **2.2.x** (Konflux release repo:
`git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's
Ecosystem Mappings table includes a **Cargo** ecosystem entry with:

- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

Ecosystem category: **Source dependency** (Cargo) -- remediation produces 2
tasks per stream (upstream backport + downstream propagation).

## Version Impact Analysis (Step 2)

Using the supportability matrix for Stream 2 (rhtpa-release.0.4.z / 2.2.x)
and the mock lock file data for quinn-proto:

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Cross-stream impact (2.1.x)

The issue is scoped to 2.2.x, but cross-stream analysis (for Case A)
shows the 2.1.x stream is also affected:

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Affects Versions Assessment

PSIRT assigned: `RHTPA 2.2.0` only.

Based on lock file analysis, the correct scoped Affects Versions for stream
2.2.x should be: `RHTPA 2.2.0, RHTPA 2.2.1` (and 2.2.2 which is a retag
of 2.2.1).

However, since this issue is identified as a duplicate (see duplicate-check.md),
Affects Versions correction is deferred to the surviving issue TC-7999.
