# Step 1 -- Data Extraction for TC-8020

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | [rhtpa-2.2] | Summary suffix |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`. This maps to the **2.2.x** stream
in the Version Streams table from Security Configuration:

- Stream suffix: `[rhtpa-2.2]`
- Mapped stream: `2.2.x`
- Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`

The issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will apply to the 2.2.x stream
only; other affected streams (2.1.x) will be handled via Case A cross-stream impact.

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation tasks per stream: 2 (upstream backport or dependency bump + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

- Affected repository (from component label): rhtpa-backend
- Source Repositories table match: rhtpa-backend
- Deployment Context column: not present in fixture Source Repositories table (no Deployment Context column)
- Default: `upstream`

## Affects Versions Discrepancy (preliminary)

PSIRT assigned **RHTPA 2.0.0** as the Affects Version. The Version Streams table
does not include a 2.0.x stream -- the configured streams are 2.1.x and 2.2.x.
This means the PSIRT-assigned Affects Version is incorrect and will need correction
in Step 3.

## Version Impact Table (from mock lock file data)

Using the mock lock file data from the security matrix:

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | Fixed version |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | Fixed version |

## Summary

- CVE-2026-31812 affects quinn-proto versions before 0.11.14.
- The issue is scoped to stream 2.2.x. Within that stream, versions 2.2.0, 2.2.1, and 2.2.2 are affected.
- Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and are NOT affected.
- Stream 2.1.x (outside the issue's scope) is also affected (both 2.1.0 and 2.1.1 ship 0.11.9).
- The PSIRT-assigned Affects Version (RHTPA 2.0.0) is incorrect and does not match any configured stream.
