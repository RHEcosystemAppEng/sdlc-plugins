# Step 1 -- Data Extraction: TC-8020

## Extracted CVE Data

| Field | Value |
|-------|-------|
| Issue Key | TC-8020 |
| CVE ID | CVE-2026-31812 |
| Summary | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable Library | quinn-proto |
| Affected Version Range | versions before 0.11.14 (< 0.11.14) |
| Fixed Version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due Date | 2026-07-15 |
| Assignee | Unassigned |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Remote Links

| Link | Type |
|------|------|
| [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | GitHub Advisory |
| [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | CVE Record |
| [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Upstream fix PR |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**, which is listed in the Ecosystem Mappings table for both version streams. Lock file: `Cargo.lock`. Check command: `git show <tag>:Cargo.lock`.

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table. Deployment context defaults to `upstream` (no Deployment Context column present in configuration).

## Version Impact Analysis (Step 2)

### Stream 2.2.x (rhtpa-release.0.4.z) -- issue scope

| Product Version | Build Tag | quinn-proto Version | Affected? | Notes |
|-----------------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of v0.4.8 -- same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### Stream 2.1.x (rhtpa-release.0.3.z) -- cross-stream analysis

| Product Version | Build Tag | quinn-proto Version | Affected? | Notes |
|-----------------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

## Affects Versions Assessment

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which does not match any configured version stream (no 2.0.x stream exists). Based on lock file analysis:

- Scoped to stream 2.2.x: affected versions are **RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2**
- Versions 2.2.3 and 2.2.4 ship the fixed version (0.11.14) and are NOT affected
- Cross-stream: 2.1.x versions (2.1.0, 2.1.1) are also affected but belong to a separate stream
