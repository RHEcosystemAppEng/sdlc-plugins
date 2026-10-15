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

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the configured Version Stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`). This issue is **stream-scoped** to 2.2.x.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The ecosystem is **Cargo**.

From the 2.2.x stream's Ecosystem Mappings:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Classification: **Source dependency** -- produces 2 remediation tasks per affected stream (upstream fix + downstream propagation).

## Deployment Context Lookup

The Source Repositories table does **not** have a Deployment Context column. Per backward compatibility rules, coordination guidance is omitted entirely from remediation task descriptions.

## Version Impact Analysis (Step 2)

### Supportability Matrix (aggregated from both streams)

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Version | Build | Build Date | backend tag |
|---------|-------|------------|-------------|
| 2.1.0 | 0.3.8 | 2025-09-15 | v0.3.8 |
| 2.1.1 | 0.3.12 | 2025-11-20 | v0.3.12 |

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Version | Build | Build Date | backend tag | Notes |
|---------|-------|------------|-------------|-------|
| 2.2.0 | 0.4.5 | 2025-12-03 | v0.4.5 | |
| 2.2.1 | 0.4.8 | 2026-02-05 | v0.4.8 | |
| 2.2.2 | 0.4.9 | 2026-02-23 | v0.4.8 | backend retag of 2.2.1 |
| 2.2.3 | 0.4.11 | 2026-03-23 | v0.4.11 | |
| 2.2.4 | 0.4.12 | 2026-05-04 | v0.4.12 | |

### Dependency Version Extraction (Step 2.3)

quinn-proto versions extracted from `Cargo.lock` at each pinned backend tag:

| Tag | quinn-proto version |
|-----|---------------------|
| v0.3.8 | 0.11.9 |
| v0.3.12 | 0.11.9 |
| v0.4.5 | 0.11.9 |
| v0.4.8 | 0.11.12 |
| v0.4.9 | (retag of v0.4.8) |
| v0.4.11 | 0.11.14 |
| v0.4.12 | 0.11.14 |

### Version Impact Table (Step 2.4)

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed version |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed version |

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |

### Affects Versions Correction (Step 3)

Issue is scoped to stream 2.2.x. Only versions from the 2.2.x stream are proposed.

Affected versions in 2.2.x: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

**Proposed correction:**
- Current: [RHTPA 2.0.0]
- Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

The PSIRT-assigned version "RHTPA 2.0.0" is incorrect -- there is no 2.0.x stream in the configured Version Streams. The lock file analysis shows versions 2.2.0, 2.2.1, and 2.2.2 ship vulnerable quinn-proto (< 0.11.14) within this issue's scoped stream.

### Cross-Stream Impact (Case A)

This issue is scoped to 2.2.x, but 2.1.x versions (2.1.0, 2.1.1) are also affected. Since no sibling CVE Jira exists for the 2.1.x stream (based on available data), preemptive remediation tasks are proposed for 2.1.x.
