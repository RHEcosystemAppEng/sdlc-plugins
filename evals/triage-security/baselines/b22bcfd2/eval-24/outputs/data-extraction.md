# Step 0 -- Validate Project Configuration

## Configuration Extraction

The following values were extracted from the project CLAUDE.md:

| Config Field | Value |
|---|---|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| Upstream Affected Component custom field | _(not configured)_ |
| PS Component custom field | _(not configured)_ |
| Stream custom field | _(not configured)_ |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |
| Embargo policy URL | _(not configured)_ |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories -- Deployment Context

The Source Repositories table in the project CLAUDE.md does **not** include a Deployment Context column. Per backward compatibility rules (section 1.78), all repositories default to `upstream`.

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream _(default -- no Deployment Context column)_ |

No Deployment Context column exists in the Source Repositories table. The triage proceeds normally without generating Coordination Guidance subsections in remediation task descriptions. Backward compatibility is maintained -- existing behavior is unaffected.

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md file contains `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`.

- Current date: 2026-07-01
- Last updated: 2026-06-28 (3 days ago)
- Threshold: 14 days

The matrix is within the 14-day threshold. Proceeding without staleness warning.

## Step 0.5 -- Jira Access Initialization

_(Skipped -- eval prohibits external API calls.)_

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Skipping Step 1.7 entirely.

---

# Step 1 -- Data Extraction

## Vulnerability Issue: TC-8001

**Source**: Mock Jira issue data from `vuln-issue-standard.md`

### Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary text |
| Affected component | pscomponent:org/rhtpa-server | Labels (matches pattern `pscomponent:`) |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | < 0.11.14 | Description: "versions before 0.11.14" |
| Fixed version | 0.11.14 | Description: "Fixed version: 0.11.14" |
| CVSS | 7.5 (High) | Description |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Remote links |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq | Remote links |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 | Remote links |
| Due date | 2026-07-15 | Issue `duedate` field |
| Existing comments | _(none)_ | Issue comment history |
| Reporter | _(not specified in mock data)_ | Issue `reporter` field |

### Stream Scope Resolution

The issue summary contains a stream suffix: `[rhtpa-2.2]`

- Parsed suffix: `rhtpa-2.2` maps to stream **2.2.x**
- Matched to Version Streams table: stream 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x only**

Since the issue is scoped to stream 2.2.x, Steps 2-8 are scoped to the 2.2.x stream. However, per Important Rule 4, all supported versions across all streams are checked in the version impact table.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Consulting the Ecosystem Mappings table from the security-matrix.md:

- Stream 2.2.x Ecosystem Mappings lists: **Cargo** (Repository: backend, Lock File: `Cargo.lock`)
- Stream 2.1.x Ecosystem Mappings lists: **Cargo** (Repository: backend, Lock File: `Cargo.lock`)

Detected ecosystem: **Cargo** (source dependency ecosystem)

This means remediation will create **two** tasks: an upstream backport task and a downstream propagation subtask.

### Deployment Context Lookup

The affected repository from the component label `pscomponent:org/rhtpa-server` maps to `rhtpa-backend`.

Looking up deployment context for `rhtpa-backend` in the Source Repositories mapping:
- Deployment Context column is **absent** from the Source Repositories table
- Default: **upstream**

Deployment context recorded: `upstream` (default due to absent column).

### Step 1.5 -- External CVE Data Enrichment

_(Skipped -- eval prohibits external API calls via WebFetch. Using Jira description data as the fix threshold.)_

Fix threshold for version impact analysis: **0.11.14** (from Jira description).
