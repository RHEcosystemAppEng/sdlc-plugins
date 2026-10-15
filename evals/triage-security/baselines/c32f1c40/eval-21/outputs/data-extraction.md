# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: customfield_10632 (configured per eval prompt)
- **Version Streams**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Source Repositories**: rhtpa-backend (no Deployment Context column -- defaults to `upstream`)

# Step 0.8 -- Assign and Transition to Assigned

**Proposed actions (not executed -- eval prohibits external calls):**

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8020 to current user via `jira.edit_issue(TC-8020, assignee=<current-user-account-id>)`
3. Discover transitions via `jira.get_transitions(TC-8020)` and select the transition whose target status is "Assigned"
4. Transition TC-8020 from New to Assigned via `jira.transition_issue(TC-8020, <assigned-transition-id>)`

# Step 1 -- Data Extraction

**Issue**: TC-8020
**Source fixture**: vuln-issue-standard.md

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | quinn-proto |

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream.

### Ecosystem detection

The vulnerable library `quinn-proto` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem. Cargo is a source dependency ecosystem, which means remediation produces two tasks per stream (upstream backport + downstream propagation).

### Deployment context lookup

The affected repository (rhtpa-backend, identified from the pscomponent:org/rhtpa-server label) is found in the Source Repositories table. The Deployment Context column is absent from the Source Repositories table, so the deployment context defaults to `upstream`.

# Step 2 -- Version Impact Analysis

## Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14)

Since the issue is scoped to `[rhtpa-2.2]`, the primary analysis covers the 2.2.x stream. However, per Important Rule 4, all supported versions are checked (including 2.1.x for cross-stream impact detection in Case A).

### 2.2.x stream (in-scope)

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | 0.11.12 < 0.11.14 |
| 2.2.2 | v0.4.8 | -- | YES | retag of 2.2.1; same as 2.2.1 |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | 0.11.14 >= 0.11.14 (fixed) |

### 2.1.x stream (cross-stream check)

| Version | Tag | quinn-proto | Affected? | Notes |
|---------|-----|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | 0.11.9 < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | 0.11.9 < 0.11.14 |

### Summary

- **2.2.x stream**: versions 2.2.0, 2.2.1, 2.2.2 are affected; versions 2.2.3, 2.2.4 are not affected
- **2.1.x stream**: all versions (2.1.0, 2.1.1) are affected -- relevant for Case A cross-stream impact

## Step 3 -- Affects Versions Correction

**Current (PSIRT-assigned)**: RHTPA 2.0.0
**Proposed (lock-file-verified, scoped to 2.2.x)**: RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2

The PSIRT-assigned version (RHTPA 2.0.0) is incorrect. Based on lock file analysis at pinned commits from security-matrix.md, the affected versions within the 2.2.x stream are 2.2.0, 2.2.1, and 2.2.2. Versions 2.2.3 and 2.2.4 ship quinn-proto 0.11.14 (the fixed version) and are not affected.

Proposed correction:
> Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]

Jira version IDs would be discovered dynamically via `getJiraIssueTypeMetaWithFields` (not hardcoded).
