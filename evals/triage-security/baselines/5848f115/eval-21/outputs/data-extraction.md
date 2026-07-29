# Step 1 -- Data Extraction

## Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description |
| Fixed version | 0.11.14 | Description |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | quinn-rs/quinn#2048 | Remote links |
| Advisory URL | GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comments |
| Upstream Affected Component | quinn-proto | customfield_10632 |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. From the security-matrix.md Ecosystem Mappings table for the 2.2.x stream, the ecosystem is **Cargo** (lock file: `Cargo.lock`, check command: `git show <tag>:Cargo.lock`).

Cargo is classified as a **source dependency** ecosystem. Per the ecosystem classification table, this produces **2 remediation tasks per stream** (upstream backport + downstream propagation).

## Deployment Context Lookup

The affected repository `rhtpa-backend` is found in the Source Repositories table. No explicit Deployment Context column is present, so it defaults to `upstream`.

## Affects Versions Analysis (PSIRT-claimed vs. Actual)

The PSIRT-assigned Affects Version is **RHTPA 2.0.0**. However, no 2.0.x stream exists in the configured Version Streams. This is incorrect and will need correction in Step 3.

## Version Impact Analysis (Step 2)

Using the mock lock file data from the security matrix, the quinn-proto versions by tag are:

### Stream 2.1.x (rhtpa-release.0.3.z) -- outside issue scope but analyzed for cross-stream awareness

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Version | Build Tag | quinn-proto Version | Affected? | Rationale |
|---------|-----------|---------------------|-----------|-----------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 (fix threshold) |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 (fix threshold) |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | Retag of v0.4.8 -- same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fix threshold) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fix threshold) |

## Summary

- **Scoped stream**: 2.2.x
- **Affected versions in scope**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Not affected versions in scope**: RHTPA 2.2.3, RHTPA 2.2.4 (ship quinn-proto 0.11.14, the fix version)
- **Cross-stream impact**: Stream 2.1.x is also fully affected (all versions ship quinn-proto 0.11.9)
- **PSIRT Affects Versions are incorrect**: RHTPA 2.0.0 does not correspond to any configured stream; must be corrected to RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (the affected versions within the 2.2.x scope)
- **Fix was introduced in**: Build 0.4.11 (version 2.2.3), which ships quinn-proto 0.11.14
