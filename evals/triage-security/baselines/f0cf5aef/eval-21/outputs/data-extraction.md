# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8020

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to stream **2.2.x** in the configured Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will be scoped to this stream only. Case A will check whether other streams (2.1.x) are also affected.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock`
- **Upstream branch**: `release/0.4.z` (for 2.2.x stream)

## Deployment Context Lookup

Repository `rhtpa-backend` is listed in Source Repositories. No explicit Deployment Context column is present, so the default of `upstream` applies.

## Affects Versions Issue

The PSIRT-assigned Affects Version is **RHTPA 2.0.0**, but there is no 2.0.x stream configured in the Version Streams table. This version is incorrect and will need correction in Step 3. The actual affected versions within the 2.2.x stream are determined in Step 2 (Version Impact Analysis).

## Version Impact Analysis Summary

Using the mock lock file data from security-matrix-mock.md:

### Stream 2.2.x (issue scope)

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | **YES** | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | **YES** | Retag of v0.4.8; same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | **NO** | 0.11.14 >= 0.11.14 (fixed) |

### Stream 2.1.x (cross-stream check for Case A)

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | **YES** | 0.11.9 < 0.11.14 |

## Conclusion

- Within the issue's scoped stream (2.2.x): versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 are not affected (already ship the fixed version 0.11.14).
- Cross-stream: the 2.1.x stream is also affected (all versions ship 0.11.9, which is vulnerable). This triggers Case A (cross-stream impact) in Step 8.
- The PSIRT-assigned Affects Version (RHTPA 2.0.0) is incorrect and must be corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2.
