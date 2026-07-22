# Step 1 -- Data Extraction for TC-8020

## Step 0 -- Configuration Validation

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
| Upstream Affected Component custom field | customfield_10632 |
| PS Component custom field | Not configured |
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

Matrix `Last-Updated` timestamp: `2026-06-28T10:00:00Z` (24 days ago as of 2026-07-22).

This exceeds the 14-day staleness threshold. In a live triage, the engineer would
be warned and given options to refresh, proceed, or stop. For this analysis, we
proceed with the current matrix data.

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component (label) | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream
in the Version Streams table. This issue is **scoped** to stream 2.2.x only.

Steps 3 and 4 will apply only to versions within the 2.2.x stream. Cross-stream
impact on the 2.1.x stream will be handled via Case B (cross-stream impact comment
and potential preemptive remediation tasks).

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Checking the Ecosystem
Mappings table for stream 2.2.x:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |
| RPM | -- | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | -- |

Detected ecosystem: **Cargo** (Rust crate). Lock file: `Cargo.lock`. Check command:
`git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`.

## Deployment Context Lookup

Source repository `rhtpa-backend` is listed in Source Repositories. The Deployment
Context column is absent, so defaulting to **upstream**.

## Step 1.5 -- External CVE Data Enrichment (simulated)

In a live triage, the MITRE CVE API and OSV.dev API would be queried for
CVE-2026-31812. Since this is a simulated triage, we use the Jira description
data as the authoritative fix threshold:

| Source | Affected range | Fixed version |
|--------|----------------|---------------|
| Jira description | < 0.11.14 | 0.11.14 |

Fix threshold for version impact analysis: **0.11.14**

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Step 1.7 is
skipped entirely.

## Step 2 -- Version Impact Analysis

### Dependency versions by tag (from mock lock file data)

| Tag | quinn-proto version |
|-----|---------------------|
| `v0.3.8` (2.1.0) | 0.11.9 |
| `v0.3.12` (2.1.1) | 0.11.9 |
| `v0.4.5` (2.2.0) | 0.11.9 |
| `v0.4.8` (2.2.1) | 0.11.12 |
| `v0.4.9` (2.2.2) | (retag of v0.4.8) |
| `v0.4.11` (2.2.3) | 0.11.14 |
| `v0.4.12` (2.2.4) | 0.11.14 |

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Stream | Version | Build Tag | quinn-proto | Affected? | Notes |
|--------|---------|-----------|-------------|-----------|-------|
| 2.1.x | 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.x | 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.x | 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.x | 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.x | 2.2.3 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.x | 2.2.4 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Affects Versions Correction (Step 3)

PSIRT-assigned Affects Versions: `RHTPA 2.0.0`

This is incorrect. There is no 2.0.x stream in the Version Streams configuration.
Based on the version impact analysis and stream scoping (issue scoped to 2.2.x):

- Current: `[RHTPA 2.0.0]`
- Proposed: `[RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]`

Versions 2.2.3 and 2.2.4 are NOT affected (ship quinn-proto 0.11.14, the fixed
version). Versions from the 2.1.x stream are excluded because this issue is
scoped to 2.2.x only.
