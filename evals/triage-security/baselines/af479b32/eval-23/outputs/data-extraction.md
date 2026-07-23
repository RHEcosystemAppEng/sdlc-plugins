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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

From the 2.2.x stream's Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

## Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to the source repository **rhtpa-backend**.

From the Source Repositories table in CLAUDE.md:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | **customer-shipped** |

Deployment context for rhtpa-backend: **customer-shipped**

This deployment context will be used in Step 8 (Remediation) to generate coordination guidance in remediation task descriptions.

## Version Impact Analysis

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Build | Backend Tag | quinn-proto | Affected? | Notes |
|---------|--------|-------|-------------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.3.8 | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.3.12 | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.4.5 | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.4.8 | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | 0.4.9 | v0.4.8 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | 2.2.x | 0.4.11 | v0.4.11 | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | 0.4.12 | v0.4.12 | 0.11.14 | NO | fixed version |

### Affects Versions Correction

The PSIRT-assigned Affects Versions is **RHTPA 2.0.0**, which is incorrect -- there is no 2.0.x stream configured. The issue is scoped to stream 2.2.x.

Proposed correction (scoped to 2.2.x stream):

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

### Cross-Stream Impact

The issue is scoped to 2.2.x, but the version impact analysis reveals that stream **2.1.x** is also affected:

- 2.1.0: quinn-proto 0.11.9 (affected)
- 2.1.1: quinn-proto 0.11.9 (affected)

This triggers Case B (cross-stream impact) in Step 8: preemptive remediation tasks will be created for the 2.1.x stream.
