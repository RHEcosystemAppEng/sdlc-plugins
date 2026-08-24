# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8020 |
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Remote Links

| Type | URL |
|------|-----|
| GitHub Advisory | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE Record | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream in the Security Configuration Version Streams table (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **scoped** to the 2.2.x stream. Steps 3 and 4 will apply scoped logic (Affects Versions correction limited to 2.2.x versions; cross-stream impact reported via Case A if other streams are also affected).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table in the security matrix for both streams lists **Cargo** as a configured ecosystem with:

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x) / `release/0.4.z` (2.2.x)

Ecosystem classification: **Source dependency** -- this means remediation produces **2 tasks per stream** (upstream backport + downstream propagation).

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table. No Deployment Context column is present in the configuration, so the default context is `upstream`.

## Version Impact Analysis (Step 2)

Using the security matrix mock lock file data for quinn-proto:

| Version | Stream | Tag | quinn-proto version | Affected? | Notes |
|---------|--------|-----|---------------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Summary

- **2.1.x stream**: All versions (2.1.0, 2.1.1) are affected -- they ship quinn-proto 0.11.9 which is below the fix threshold 0.11.14.
- **2.2.x stream**: Versions 2.2.0, 2.2.1, and 2.2.2 are affected. Versions 2.2.3 and 2.2.4 already ship the fixed version (0.11.14) and are NOT affected.

### Affects Versions Mismatch

The PSIRT-assigned Affects Versions field contains `RHTPA 2.0.0`, which does not match any configured version stream (there is no 2.0.x stream). This is incorrect and must be corrected in Step 3 to reflect the actually affected versions within the issue's scoped stream (2.2.x): `RHTPA 2.2.0`, `RHTPA 2.2.1`, `RHTPA 2.2.2`.
