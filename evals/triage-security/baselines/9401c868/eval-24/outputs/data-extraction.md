# Step 0 -- Validate Project Configuration

## Configuration Extraction

The following values were extracted from the project CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: _(not configured)_
- **PS Component custom field**: _(not configured)_
- **Stream custom field**: _(not configured)_
- **ProdSec contact email**: _(not configured)_
- **ProdSec Jira account ID**: _(not configured)_
- **Embargo policy URL**: _(not configured)_

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

**Deployment Context column**: absent from the Source Repositories table. Per backward compatibility rules, all repositories default to `upstream`. The Coordination Guidance subsection will be omitted entirely from remediation task descriptions.

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md Last-Updated timestamp is `2026-06-28T10:00:00Z`. Today is 2026-10-08. The matrix is approximately 102 days old, which exceeds the 14-day default threshold. In a live triage, a staleness warning would be presented with options to refresh, proceed, or stop. For this eval, proceeding with the current matrix data.

## Step 0.5 -- Jira Access Initialization

Jira MCP access would be initialized per the shared jira-access-strategy.md protocol. For this eval, Jira operations are simulated.

## Step 0.7 -- Assign and Transition to Assigned

Before extracting CVE data, perform early assignment actions on TC-8001:

1. **Retrieve current user's Jira account ID**: `jira.user_info()` to obtain the current user's account ID.
2. **Assign the issue to the current user**: `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)`
3. **Discover available transitions**: `jira.get_transitions("TC-8001")` -- select the transition whose target status name is "Assigned".
4. **Transition to Assigned**: TC-8001 is currently in New status. `jira.transition_issue("TC-8001", <assigned-transition-id>)`

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the configured **2.2.x** stream (Konflux release repo: rhtpa-release.0.4.z). This issue is **stream-scoped** to 2.2.x. Steps 3-8 are scoped to this stream, while cross-stream impact on 2.1.x is evaluated in Step 8 Case A.

### Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, the ecosystem is **Cargo**. Cargo is a **source dependency** ecosystem per the classification table, which means remediation produces **two tasks per stream**: a dependency bump task (when upstream fix is available) or upstream backport task (when not), plus a downstream propagation subtask.

### Deployment Context Lookup

The affected repository is **rhtpa-backend** (matched from component label pscomponent:org/rhtpa-server). The Source Repositories table does not include a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. Since the column is absent, no Coordination Guidance subsection will be added to remediation task descriptions.

## Step 1.5 -- External CVE Data Enrichment

In a live triage, the MITRE CVE API and OSV.dev API would be queried for structured version ranges. For this eval, the Jira description data is used as the authoritative fix threshold:

- **Fix threshold**: 0.11.14 (quinn-proto versions before 0.11.14 are affected)
- **Source**: Jira description (cross-validation with external APIs not performed in this eval)

## Step 1.7 -- Embargo Check

No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped entirely.

## Step 2 -- Version Impact Analysis

### Aggregated Supportability Matrix

Using mock lock file data for quinn-proto at each pinned backend tag:

**Stream 2.1.x (rhtpa-release.0.3.z):**

| Version | Build | Backend Tag | quinn-proto version | Affected? | Notes |
|---------|-------|-------------|---------------------|-----------|-------|
| 2.1.0 | 0.3.8 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | 0.3.12 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

**Stream 2.2.x (rhtpa-release.0.4.z):**

| Version | Build | Backend Tag | quinn-proto version | Affected? | Notes |
|---------|-------|-------------|---------------------|-----------|-------|
| 2.2.0 | 0.4.5 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | 0.4.8 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | 0.4.9 | v0.4.8 | 0.11.12 | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 0.4.11 | v0.4.11 | 0.11.14 | NO | >= 0.11.14 (fixed) |
| 2.2.4 | 0.4.12 | v0.4.12 | 0.11.14 | NO | >= 0.11.14 (fixed) |

### Combined Version Impact Table

| Version | quinn-proto | Affected? | Notes |
|---------|-------------|-----------|-------|
| 2.1.0 | 0.11.9 | YES | |
| 2.1.1 | 0.11.9 | YES | |
| 2.2.0 | 0.11.9 | YES | |
| 2.2.1 | 0.11.12 | YES | |
| 2.2.2 | -- | YES | retag of 2.2.1 |
| 2.2.3 | 0.11.14 | NO | |
| 2.2.4 | 0.11.14 | NO | |

### Upstream Fix Status

| Stream | Ecosystem | Upstream Branch | Latest Tag Version | Fixed? |
|--------|-----------|-----------------|-------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |

The upstream fix IS available on release/0.4.z (stream 2.2.x). This means the 2.2.x remediation uses the **dependency bump** template (straightforward `cargo update`) rather than the upstream backport template.

The upstream fix is NOT available on release/0.3.z (stream 2.1.x). If preemptive tasks are created for 2.1.x, they use the **upstream backport** template.

### Step 3 -- Affects Versions Correction

- **Current (PSIRT-assigned)**: RHTPA 2.0.0
- **Proposed (lock-file-verified, scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

RHTPA 2.0.0 does not correspond to any configured version stream and is incorrect. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are NOT affected.

### Step 4 -- Duplicate/Sibling Check

Upstream Affected Component custom field is not configured. Steps 4.3 (cross-CVE overlap) and 7 (concurrent triage detection) are skipped entirely. Step 4.4 (preemptive task reconciliation) would search for existing preemptive tasks matching CVE-2026-31812.

### Step 5 -- Version Lifecycle Check

The Product pages URL (https://access.example.com/product-life-cycle/rhtpa) would be fetched to verify that affected versions are still within support lifecycle. For this eval, all versions are assumed to be within support.

### Step 6 -- Already Fixed Check

No resolved sibling Vulnerability issues found for CVE-2026-31812. Proceeding to remediation.

### Step 7 -- Concurrent Triage Detection

Upstream Affected Component custom field is not configured. Step 7 is skipped entirely.

### Step 7.5 -- Release Jira Orchestration

In a live triage, the release Epic and release Task would be found or created for each affected stream. For this eval, release Jira operations are simulated.
