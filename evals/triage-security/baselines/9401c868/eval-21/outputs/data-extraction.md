# Data Extraction for TC-8020

## Step 0 -- Validate Project Configuration

Validated project configuration from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: customfield_10632 (configured)

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md contains `Last-Updated: 2026-06-28T10:00:00Z`. As of 2026-10-08, this is 102 days old, exceeding the 14-day staleness threshold.

> Security matrix was last updated on 2026-06-28 (102 days ago). The matrix may not reflect recent releases.

For this eval, proceeding with the current matrix data.

## Step 0.7 -- Assign and Transition to Assigned

Before data extraction, the issue is assigned and transitioned:

1. **Retrieve current user's Jira account ID**: `jira.user_info()` (simulated)
2. **Assign TC-8020 to current user**: `jira.edit_issue(TC-8020, assignee=<current-user-account-id>)`
3. **Discover target transition**: `jira.get_transitions(TC-8020)` -- select the transition whose target status name is "Assigned"
4. **Transition to Assigned**: TC-8020 is currently in "New" status, so transition proceeds: `jira.transition_issue(TC-8020, <assigned-transition-id>)`

## Step 1 -- Extracted CVE Data

| Field | Value | Source |
|-------|-------|--------|
| CVE ID | CVE-2026-31812 | Labels, summary |
| Affected component | pscomponent:org/rhtpa-server | Label matching `pscomponent:` pattern |
| Product version (PSIRT-claimed) | rhtpa-2.2 | Summary suffix `[rhtpa-2.2]` |
| Affects Versions (Jira field) | RHTPA 2.0.0 | Jira `versions` field |
| Vulnerable library | quinn-proto | Description text |
| Affected version range | versions before 0.11.14 (< 0.11.14) | Description text |
| Fixed version | 0.11.14 | Description text |
| CVSS | 7.5 (High) | Description text |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) | Remote links |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) | Remote links |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) | Remote links |
| Due date | 2026-07-15 | Jira `duedate` field |
| Existing comments | None | Issue comment history |
| Upstream Affected Component | quinn-proto | customfield_10632 |

### Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue is **stream-scoped** to 2.2.x only
- Steps 3 and 4 will scope to versions within 2.2.x; Case A will check cross-stream impact on 2.1.x

### Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Remediation tasks per stream: 2 (upstream backport or dependency bump + downstream propagation)

### Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)

## Step 1.5 -- External CVE Data Enrichment (simulated)

External APIs queried:
1. MITRE CVE API: `https://cveawg.mitre.org/api/cve/CVE-2026-31812`
2. OSV.dev API: `https://api.osv.dev/v1/vulns/CVE-2026-31812`

Cross-validation result: agreement with Jira description data.
- **Enriched fix threshold**: quinn-proto >= 0.11.14
- **Affected range**: versions before 0.11.14

## Step 2 -- Version Impact Analysis

Using pinned commit tags from the supportability matrix and mock lock file data:

### Stream 2.1.x (rhtpa-release.0.3.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.1.0 | v0.3.8 | 0.11.9 | YES | < 0.11.14 |
| 2.1.1 | v0.3.12 | 0.11.9 | YES | < 0.11.14 |

### Stream 2.2.x (rhtpa-release.0.4.z)

| Version | Build Tag | quinn-proto | Affected? | Notes |
|---------|-----------|-------------|-----------|-------|
| 2.2.0 | v0.4.5 | 0.11.9 | YES | < 0.11.14 |
| 2.2.1 | v0.4.8 | 0.11.12 | YES | < 0.11.14 |
| 2.2.2 | v0.4.9 | -- | YES | retag of 2.2.1 (same as v0.4.8) |
| 2.2.3 | v0.4.11 | 0.11.14 | NO | ships fixed version |
| 2.2.4 | v0.4.12 | 0.11.14 | NO | ships fixed version |

All version checks used pinned commit tags from the supportability matrix (per Important Rule 13). Retag version 2.2.2 carries forward the result from 2.2.1 (per Important Rule 5).

### Upstream Fix Status (Step 2.5)

| Stream | Ecosystem | Upstream Branch | Version at latest tag | Fixed? |
|--------|-----------|-----------------|----------------------|--------|
| 2.1.x | Cargo | release/0.3.z | 0.11.9 (at v0.3.12) | NO |
| 2.2.x | Cargo | release/0.4.z | 0.11.14 (at v0.4.12) | YES |

For stream 2.2.x, the upstream branch already ships the fixed version (0.11.14 at v0.4.11+), so remediation uses the **dependency bump** variant.
For stream 2.1.x, the upstream branch does NOT yet ship the fix, so remediation would require an **upstream backport** task.

## Affects Versions Correction (Step 3)

- Current (PSIRT-assigned): `[RHTPA 2.0.0]`
- RHTPA 2.0.0 does not correspond to any version in the supportability matrix -- incorrect
- Scoped to stream 2.2.x per issue suffix `[rhtpa-2.2]`

Proposed correction:
```
Current: [RHTPA 2.0.0] -> Proposed: [RHTPA 2.2.0, RHTPA 2.2.1, RHTPA 2.2.2]
```

Versions 2.2.3 and 2.2.4 are excluded because they ship the fixed quinn-proto 0.11.14. Stream 2.1.x versions are excluded from this issue's Affects Versions because they belong to a different stream scope.
