# Data Extraction -- TC-8003

## Step 0 -- Validate Project Configuration

Configuration validated from CLAUDE.md (claude-md-security-config.md):

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured |
| PS Component field | Not configured |
| Stream custom field | Not configured |
| ProdSec contact email | Not configured |
| ProdSec Jira account ID | Not configured |
| Embargo policy URL | Not configured |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream (default -- no Deployment Context column) |

## Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z` (25 days ago as of 2026-07-23).

The matrix is older than the 14-day staleness threshold. In a live triage, the user would be warned and asked to refresh, proceed, or stop. For this eval, proceeding with current data.

## Step 1 -- Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (Konflux release repo: rhtpa-release.0.4.z). This issue is **scoped** to stream 2.2.x.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**. This matches the Ecosystem Mappings table in both streams' security-matrix.md, which list Cargo with lock file `Cargo.lock` and check command `git show <tag>:Cargo.lock`.

### Deployment Context

Source repository `rhtpa-backend` has deployment context: **upstream** (default, since no Deployment Context column is present in Source Repositories).

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- external APIs not called in eval mode)

Using Jira description data as authoritative:
- Affected range: versions before 0.11.14
- Fixed version: 0.11.14

## Step 1.7 -- Embargo Check

Embargo policy URL is not configured in Security Configuration. Step 1.7 skipped.

## Step 2 -- Version Impact Analysis

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | quinn-proto | Affected? | Notes |
|---------|--------|-------------|-----------|-------|
| 2.1.0 | 2.1.x | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |
| 2.2.4 | 2.2.x | 0.11.14 | NO | fixed at 0.11.14 |

### Dependency Chain Context

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Ecosystem: Cargo
  Lock file: Cargo.lock
  Profile: production (assumed -- quinn-proto is a QUIC protocol library)
```

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Check Command |
|--------|-----------|-----------------|---------------|
| 2.1.x | Cargo | release/0.3.z | git show <tag>:Cargo.lock |
| 2.2.x | Cargo | release/0.4.z | git show <tag>:Cargo.lock |

The latest tags for each stream show:
- 2.1.x (v0.3.12): quinn-proto 0.11.9 -- NOT fixed upstream on release/0.3.z
- 2.2.x (v0.4.12): quinn-proto 0.11.14 -- FIXED upstream on release/0.4.z (as of v0.4.11+)
