# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8006

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.1 | Summary suffix `[rhtpa-2.1]` |
| Affects Versions (Jira field) | RHTPA 2.1.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS score | 7.5 (High) | Description text |
| Upstream fix PR | Not provided | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links (GHSA) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links (cve.org) |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | None | Issue comments |
| Status | New | Issue status field |
| Assignee | Unassigned | Issue assignee field |

## Stream Scope Resolution

- **Summary suffix**: `[rhtpa-2.1]`
- **Mapped stream**: 2.1.x (matches Version Streams table row: Stream `2.1.x`, Konflux Release Repo `git.example.com/rhtpa/rhtpa-release.0.3.z`)
- **Issue stream scope**: 2.1.x only -- Steps 3-8 are scoped to this single stream

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Classification**: Source dependency
- **Remediation task count per stream**: 2 (upstream backport or dependency bump + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.3.z` (for the 2.1.x stream)

## Deployment Context Lookup

- **Affected repository**: rhtpa-backend (derived from pscomponent:org/rhtpa-server)
- **Deployment context**: upstream (default -- Deployment Context column absent in Source Repositories table)

## Existing Issue Links

- **Related**: TC-8001 (outward link, link ID 1990401) -- CVE-2026-31812 quinn-proto [rhtpa-2.2]

## Version Impact Analysis (from mock lock file data, scoped to 2.1.x stream)

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES |
| 2.1.1 | v0.3.12 | 0.11.9 | YES |

Both versions in the 2.1.x stream ship quinn-proto 0.11.9, which is below the fix threshold of 0.11.14. All versions in this stream are affected.

## Cross-stream impact (for Case A analysis)

The 2.2.x stream is outside TC-8006's scope. For reference:

| Version | Build Tag | quinn-proto version | Affected? (< 0.11.14) |
|---------|-----------|--------------------|-----------------------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES |
| 2.2.1 | v0.4.8 | 0.11.12 | YES |
| 2.2.2 | v0.4.9 | (retag of v0.4.8) | YES (same as 2.2.1) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO (fixed) |

Stream 2.2.x is already tracked by sibling TC-8001 (In Progress), so no preemptive remediation is needed for that stream.
