# Step 0.7 -- Assign and Transition to Assigned

Before extracting CVE data, assign the issue and transition it to Assigned status
to provide visibility into who is actively triaging.

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8004 to the current user:**
   ```
   jira.edit_issue("TC-8004", assignee=<current-user-account-id>)
   ```

3. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8004")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8004", <assigned-transition-id>)
   ```

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.8 |
| Fixed version | 0.4.8 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| Existing comments | None |
| Reporter | _(extracted from Jira issue reporter field)_ |

## Stream Scope Resolution

The issue summary "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames"
has **no stream suffix** in brackets. Therefore, this issue is treated as
**unscoped** -- it covers all configured version streams.

All streams will be analyzed:
- **2.1.x** (Konflux release repo: rhtpa-release.0.3.z)
- **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)

## Ecosystem Detection

The vulnerable library **h2** is a Rust crate. Based on the Ecosystem Mappings
tables in both streams' security-matrix.md, h2 maps to the **Cargo** ecosystem.

Cargo is classified as a **source dependency** ecosystem, which means remediation
produces two tasks per affected stream: an upstream backport task and a downstream
propagation subtask (with Blocks dependency).

## Deployment Context Lookup

The Source Repositories table in CLAUDE.md does not have a Deployment Context
column. Per backward compatibility rules, all repositories default to `upstream`.
No Coordination Guidance subsection will be added to remediation task descriptions.
