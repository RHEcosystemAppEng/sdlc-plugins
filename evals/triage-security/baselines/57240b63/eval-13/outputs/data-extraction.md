# Step 1 -- Data Extraction: TC-8001

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels: `CVE-2026-31812`; Summary text |
| Affected component | `pscomponent:org/rhtpa-server` | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 (versions before 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links (quinn-rs/quinn#2048) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GitHub Advisory) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (CVE Record) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comment history |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x**
- Matches configured Version Stream: `2.2.x` at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue is **scoped** to stream 2.2.x only

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- From stream 2.2.x Ecosystem Mappings:
  - Repository: backend
  - Lock File: `Cargo.lock`
  - Check Command: `git show <tag>:Cargo.lock`
  - Upstream Branch: `release/0.4.z`

## Deployment Context Lookup

- Affected repository: rhtpa-backend (from component label `pscomponent:org/rhtpa-server`)
- Source Repositories table has **no Deployment Context column**
- Default: `upstream` (for internal extraction use)
- Coordination Guidance subsection: **omitted** from task descriptions (column absent = backward compatibility)

## Configuration Extracted (Step 0)

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | `pscomponent:` |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured (Step 4.3 and Step 7 skipped) |
| PS Component field | Not configured |
| Stream field | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured (skip @mentions) |
| Embargo policy URL | Not configured (Step 1.7 skipped) |

## Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Matrix Staleness Check (Step 0.3)

- Both streams share a single mock matrix file with `Last-Updated: 2026-06-28T10:00:00Z`
- Current date: 2026-07-02
- Age: 4 days (within the 14-day threshold)
- Result: **Not stale** -- proceed without warning
