# Step 0 -- Validate Project Configuration

## Configuration Extracted

| Parameter | Value |
|-----------|-------|
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

### Source Repositories -- Deployment Context

The Source Repositories table in CLAUDE.md does **not** include a Deployment Context column:

| Repository | URL | Local Path |
|------------|-----|------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend |

Per backward compatibility rules, all repositories default to `upstream` deployment context. Since the Deployment Context column is absent entirely, coordination guidance will be **omitted** from remediation task descriptions.

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

## Step 0.3 -- Matrix Staleness Check

The security-matrix.md contains `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. This is within the 14-day threshold (5 days ago as of 2026-07-03). Proceeding without staleness warning.

## Step 0.7 -- Assign and Transition to Assigned

**Proposed actions** (require Jira access):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8001 to the current user:
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
3. Discover the "Assigned" transition dynamically:
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned".
4. Transition TC-8001 from New to Assigned:
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

The issue is currently in **New** status, so the transition to Assigned will proceed.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`). This issue is **scoped** to the 2.2.x stream only.

Steps 3 and 4 will be scoped to the 2.2.x stream. However, Version Impact Analysis (Step 2) still checks all streams to detect cross-stream impact (Case B).

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the security-matrix.md, the matching ecosystem is **Cargo**:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Investigation method: Lock file inspection via `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`

## Deployment Context Lookup

The affected repository (rhtpa-backend, identified from the component label `pscomponent:org/rhtpa-server`) was looked up in the Source Repositories table. The Deployment Context column is **absent** from the table. Per backward compatibility rules, the deployment context defaults to `upstream`. However, since the column is entirely absent (not just empty for this row), **no Coordination Guidance subsection** will be added to remediation task descriptions.
