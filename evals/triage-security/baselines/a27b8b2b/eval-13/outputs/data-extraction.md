# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8001 to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

3. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
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

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to this stream for Steps 3 and 4 (Affects Versions correction and duplicate check). However, per Important Rule 4, all versions from all streams are checked in Step 2 (Version Impact Analysis).

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in security-matrix.md, this maps to the **Cargo** ecosystem.

Cargo is classified as a **source dependency** ecosystem per the classification table:

| Category | Ecosystems | Remediation tasks per stream |
|---|---|---|
| Source dependency | Cargo, npm | 2 -- upstream backport + downstream propagation |

This means remediation will create **two tasks** per affected stream: an upstream backport task and a downstream propagation subtask with a Blocks dependency.

## Deployment Context Lookup

The Source Repositories table in the CLAUDE.md does not have a Deployment Context column. Per backward compatibility rules, all repositories default to `upstream`. No Coordination Guidance subsection will be included in remediation task descriptions.
