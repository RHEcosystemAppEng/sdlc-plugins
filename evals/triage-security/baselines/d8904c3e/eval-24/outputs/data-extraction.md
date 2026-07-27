# Step 1 -- Data Extraction: TC-8001

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
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Remediation tasks per stream**: 2 (upstream backport + downstream propagation)
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context

The Source Repositories table in CLAUDE.md does not have a Deployment Context column. Per backward compatibility rules, all repos default to `upstream`. Coordination guidance is omitted from remediation task descriptions.

## Affects Versions Mismatch

The PSIRT-assigned Affects Versions field is **RHTPA 2.0.0**, but there is no 2.0.x version stream configured. Lock file analysis (Step 2) determines the correct affected versions.

## Version Impact Analysis

Using the security matrix mock data for quinn-proto versions by pinned source tag:

| Version | Stream | Source Tag | quinn-proto | Affected? | Notes |
|---------|--------|------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 2.2.x | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Summary

- **2.1.x stream**: ALL versions affected (2.1.0, 2.1.1) -- outside issue scope
- **2.2.x stream** (issue scope): versions 2.2.0, 2.2.1, 2.2.2 are affected; 2.2.3 and 2.2.4 are fixed
- **Corrected Affects Versions**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2 (for the scoped 2.2.x stream)
- **Cross-stream impact**: 2.1.x stream is also fully affected (Case A applies)

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Version at HEAD (latest tag) | Fixed? |
|--------|-----------|-----------------|------------------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.11+) | YES |
