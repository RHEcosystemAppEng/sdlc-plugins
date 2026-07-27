# Step 0 -- Validate Project Configuration

## Extracted Configuration

| Parameter | Value |
|-----------|-------|
| Project key | TC |
| Cloud ID | 2b9e35e3-6bd3-4cec-b838-f4249ee02432 |
| Jira version prefix | RHTPA |
| Vulnerability issue type ID | 10024 |
| Product pages URL | https://access.example.com/product-life-cycle/rhtpa |
| Component label pattern | pscomponent: |
| VEX Justification custom field | customfield_12345 |
| ProdSec contact email | _(not configured)_ |
| ProdSec Jira account ID | _(not configured)_ |
| Embargo policy URL | _(not configured)_ |
| Upstream Affected Component field | _(not configured)_ |
| PS Component field | _(not configured)_ |
| Stream custom field | _(not configured)_ |

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

### Source Repositories

| Repository | URL | Deployment Context |
|------------|-----|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | upstream _(default -- no Deployment Context column)_ |

## Step 0.3 -- Matrix Staleness Check

Completed silently -- both streams have matrix files with Last-Updated timestamps within the 14-day threshold. No staleness warning was displayed. See outputs/staleness-check.md for details.

## Step 0.5 -- JIRA Access Initialization

_(Skipped per eval rules -- no external tools)_

## Step 0.7 -- Assign and Transition to Assigned

**Proposed actions** (not executed per eval rules):
1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8001 to the current user via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
3. Discover the "Assigned" transition ID via `jira.get_transitions(TC-8001)` -- select the transition whose target status name is "Assigned" (do not hardcode transition ID)
4. Transition TC-8001 from New to Assigned via `jira.transition_issue(TC-8001, <assigned-transition-id>)`

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Reporter | _(not specified in fixture)_ |

### Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.2]`
- Mapped to stream: **2.2.x** (matches Version Streams table entry for 2.2.x)
- Issue stream scope: **scoped to 2.2.x stream**

### Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Remediation task structure: 2 tasks per stream (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

### Deployment Context Lookup

- Affected repository (from component label): rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)
