# Data Extraction (Step 1) -- TC-8021

## Parsed CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches component label pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Stream scope | 2.2.x | Mapped from summary suffix `[rhtpa-2.2]` to Version Streams table |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Upstream Affected Component | quinn-proto | customfield_10632 |
| Ecosystem | Cargo | Detected from library name (quinn-proto is a Rust crate); confirmed in Ecosystem Mappings table |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
`2.2.x` version stream in the Security Configuration Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

This issue is **stream-scoped** to the 2.2.x stream. Steps 3 and 4 will apply
scoped behavior (Affects Versions limited to 2.2.x versions, cross-stream
impact checked via Case A).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings
table for both streams lists Cargo as a configured ecosystem with:

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z` (2.2.x stream) / `release/0.3.z` (2.1.x stream)

Classification: **Source dependency** ecosystem -- produces 2 remediation tasks
per affected stream (dependency bump + downstream propagation, since upstream
fix is available).

## Version Impact Analysis (Step 2)

Using mock lock file data for quinn-proto versions by tag:

### Stream 2.1.x (cross-stream, outside issue scope)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Stream 2.2.x (issue's scoped stream)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of v0.4.8; same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Summary

- **2.2.x stream**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions
  2.2.3 and 2.2.4 already ship the fix (quinn-proto 0.11.14).
- **2.1.x stream**: All versions (2.1.0, 2.1.1) are affected. Latest version
  (2.1.1) still ships quinn-proto 0.11.9.

### Upstream Fix Status (Step 2.5)

The fix (quinn-proto 0.11.14) is already present in the latest released
versions of the 2.2.x stream (v0.4.11 and v0.4.12). For the 2.1.x stream,
the latest tag (v0.3.12) still ships quinn-proto 0.11.9 -- the fix has not
been picked up.

## Affects Versions Correction (Step 3)

The issue is scoped to the 2.2.x stream, so only 2.2.x versions are included.

- **Current Affects Versions**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- **Proposed Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

Correction rationale: PSIRT assigned "RHTPA 2.0.0" which does not correspond to
any configured version stream. Lock file analysis at pinned commits confirms
versions 2.2.0 through 2.2.2 ship vulnerable quinn-proto versions. Versions
2.2.3 and 2.2.4 already include the fix and are excluded from Affects Versions.
