# Step 1 -- Data Extraction

## Issue: TC-8001

Extracted from Vulnerability issue TC-8001.

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
| CVE Record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table row for `git.example.com/rhtpa/rhtpa-release.0.4.z`)
- Issue is **scoped** to the 2.2.x stream

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Remediation task count per stream: 2 (upstream backport/dependency bump + downstream propagation)

## Affects Versions Mismatch (Preliminary)

The PSIRT-assigned Affects Versions value `RHTPA 2.0.0` does not correspond to any
version in the configured Version Streams (2.1.x and 2.2.x). This will need correction
in Step 3 after the version impact analysis confirms which versions are actually affected.

## Version Impact Data (from mock lock file data)

Using the quinn-proto versions from the security matrix mock data:

| Version | Stream | Build Tag | quinn-proto version | Affected? (< 0.11.14) | Notes |
|---------|--------|-----------|---------------------|------------------------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | ships fixed version |

## Summary

- **Affected versions in scoped stream (2.2.x)**: 2.2.0, 2.2.1, 2.2.2
- **Not affected in scoped stream (2.2.x)**: 2.2.3, 2.2.4
- **Cross-stream impact (2.1.x)**: 2.1.0, 2.1.1 are also affected (Case A applies for scoped issue)
- **Affects Versions correction needed**: RHTPA 2.0.0 (wrong) -> RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (scoped to 2.2.x stream)
