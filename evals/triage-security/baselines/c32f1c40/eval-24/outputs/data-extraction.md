# Data Extraction — TC-8001

## Step 0 — Validate Project Configuration

Configuration extracted from CLAUDE.md:

| Setting | Value |
|---------|-------|
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

### Source Repositories

The Source Repositories table in Security Configuration has columns: Repository, URL, Local Path. **No Deployment Context column is present.** Per backward compatibility rules (section 1.78), all repositories default to `upstream`.

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream _(defaulted — no Deployment Context column)_ |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Step 0.3 — Matrix Staleness Check

The security-matrix.md Last-Updated timestamp is `2026-06-28T10:00:00Z`. This is within the 14-day threshold. Proceeding without warning.

## Step 0.8 — Assign and Transition to Assigned

**Proposed actions** (not executed — eval mode):

1. Retrieve current user's Jira account ID via `jira.user_info()`.
2. Assign TC-8001 to the current user via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`.
3. Discover available transitions via `jira.get_transitions(TC-8001)` and select the transition whose target status is "Assigned".
4. Transition TC-8001 from New to Assigned via `jira.transition_issue(TC-8001, <assigned-transition-id>)`.

These actions are presented as proposals and have not been executed.

## Step 1 — Parsed CVE Data

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream for Steps 3-8. All versions across all streams are still checked in Step 2 (Important Rule 4).

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** as a supported ecosystem with repository `backend`, lock file `Cargo.lock`, and check command `git show <tag>:Cargo.lock`.

Ecosystem: **Cargo** (source dependency category — produces 2 remediation tasks per stream: upstream backport + downstream propagation).

### Deployment Context Lookup

The affected repository `rhtpa-backend` deployment context is **upstream** (defaulted, because the Source Repositories table does not include a Deployment Context column).

## Step 2 — Version Impact Analysis

### Version Impact Table

Version Impact for CVE-2026-31812 (quinn-proto < 0.11.14):

| Version | Stream | Tag | quinn-proto | Affected? | Notes |
|---------|--------|-----|-------------|-----------|-------|
| 2.1.0 | 2.1.x | v0.3.8 | 0.11.9 | YES | |
| 2.1.1 | 2.1.x | v0.3.12 | 0.11.9 | YES | |
| 2.2.0 | 2.2.x | v0.4.5 | 0.11.9 | YES | |
| 2.2.1 | 2.2.x | v0.4.8 | 0.11.12 | YES | |
| 2.2.2 | 2.2.x | v0.4.9 | -- | YES | retag of 2.2.1 (same as 2.2.1) |
| 2.2.3 | 2.2.x | v0.4.11 | 0.11.14 | NO | |
| 2.2.4 | 2.2.x | v0.4.12 | 0.11.14 | NO | |

### Dependency Chain Context (Step 2.3.5)

```
Dependency chain for quinn-proto:
  backend (workspace) -> quinn-proto
  Type: direct dependency
  Profile: production (quinn-proto is a runtime dependency)

Remediation: bump quinn-proto to >= 0.11.14 in Cargo.lock
```

### Upstream Fix Status (Step 2.5)

The upstream branch `release/0.4.z` for the 2.2.x stream already ships quinn-proto 0.11.14 (evidenced by versions 2.2.3 and 2.2.4 shipping the fix). The upstream fix is already available.

| Stream | Ecosystem | Upstream Branch | Version at HEAD | Fixed? |
|--------|-----------|-----------------|-----------------|--------|
| 2.2.x | Cargo | release/0.4.z | 0.11.14 | YES |
| 2.1.x | Cargo | release/0.3.z | 0.11.9 | NO |

Since the upstream branch for 2.2.x already ships the fix, remediation uses the dependency bump variant (not upstream backport).
