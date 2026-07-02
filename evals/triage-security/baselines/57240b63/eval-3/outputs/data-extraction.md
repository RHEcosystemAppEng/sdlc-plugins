# Step 1 -- Data Extraction: TC-8003

## Step 0 -- Configuration Validated

| Config Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component field | Not configured |
| PS Component field | Not configured |
| Stream field | Not configured |
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

The security-matrix.md timestamp is `2026-06-28T10:00:00Z` (4 days ago as of 2026-07-02). This is within the 14-day freshness threshold. Proceeding without staleness warning.

## Step 0.7 -- Assign and Transition

PROPOSAL: Assign TC-8003 to current user and transition from New to Assigned status.

## Extracted CVE Data

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
| Assignee | Unassigned |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** in the Version Streams table. This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

Library `quinn-proto` is a Rust crate. From the 2.2.x stream's Ecosystem Mappings table:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | Cargo.lock | `git show <tag>:Cargo.lock` | release/0.4.z |

Ecosystem: **Cargo** (source dependency)

## Deployment Context Lookup

The Source Repositories table has no Deployment Context column. Defaulting rhtpa-backend to `upstream`.

## Step 1.5 -- External CVE Data Enrichment

(Simulated -- no external API calls per eval constraints)

Using Jira description data as the authoritative fix threshold:
- Affected range: versions before 0.11.14
- Fixed version: **0.11.14**

## Step 1.7 -- Embargo Check

No Embargo policy URL configured in Security Configuration. Skipping embargo check.

## Version Impact Analysis (Step 2)

### Stream 2.2.x (issue-scoped stream)

Using mock lock file data from security-matrix-mock.md:

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | 0.11.12 | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Stream 2.1.x (cross-stream analysis)

| Version | Build Tag | quinn-proto version | Affected? | Notes |
|---------|-----------|---------------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Summary

Affected versions in scoped stream (2.2.x): RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2
Not affected in scoped stream: RHTPA 2.2.3, RHTPA 2.2.4
Cross-stream affected (2.1.x): RHTPA 2.1.0, RHTPA 2.1.1
