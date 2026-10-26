# Step 1 -- Data Extraction: TC-8001

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This is a **stream-scoped** issue -- Steps 3-4 are scoped to the 2.2.x stream. Cross-stream impact on 2.1.x is evaluated under Case A.

## Ecosystem Detection

- **Library**: quinn-proto (Rust crate)
- **Ecosystem**: Cargo
- **Category**: Source dependency
- **Lock file**: `Cargo.lock`
- **Check command**: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context Lookup

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | **customer-shipped** |

The affected repository `rhtpa-backend` was found in the Source Repositories table of the CLAUDE.md Security Configuration. Its deployment context is `customer-shipped`.

## Version Impact Analysis

### 2.2.x stream (scoped -- primary analysis)

| Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|---------|-------|-------------|-------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 0.4.9 | v0.4.8 | 0.11.12 | YES | retag of 2.2.1 |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### 2.1.x stream (cross-stream impact -- Case A)

| Version | Build | Backend Tag | quinn-proto | Affected? | Notes |
|---------|-------|-------------|-------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (v0.4.11+) | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (v0.3.12) | NO |

The upstream fix for quinn-proto is already present on the `release/0.4.z` branch (2.2.x stream) as of tag v0.4.11. The `release/0.3.z` branch (2.1.x stream) does not yet have the fix -- all tags ship quinn-proto 0.11.9.

## Affects Versions Correction

- **PSIRT-assigned**: RHTPA 2.0.0 (incorrect -- no 2.0.x stream exists)
- **Correct Affects Versions (2.2.x scope)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
- **Not affected**: RHTPA 2.2.3, RHTPA 2.2.4 (ship quinn-proto 0.11.14, which is the fixed version)

The PSIRT-assigned Affects Versions of "RHTPA 2.0.0" is incorrect. There is no 2.0.x version stream configured. Lock file evidence shows that versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto versions (0.11.9 and 0.11.12), while versions 2.2.3 and 2.2.4 ship the fixed version 0.11.14.
