# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info() -> current user account ID
   ```

2. **Assign TC-8051 to the current user:**
   ```
   jira.edit_issue("TC-8051", assignee=<current-user-account-id>)
   ```

3. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8051")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8051", <assigned-transition-id>)
   ```

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99002 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | rustls |
| Affected version range | < 0.23.5 |
| Fixed version | 0.23.5 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/rustls/rustls/pull/2100 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99002 |
| Due date | 2026-08-01 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream
in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `rustls` is a Rust crate. Based on the Ecosystem Mappings table
in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

Cargo is classified as a **source dependency** ecosystem, which produces **two** remediation
tasks per stream (upstream backport + downstream propagation).

## Deployment Context Lookup

The affected component `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`.
The Source Repositories table in the CLAUDE.md does not include a Deployment Context column.
Per backward compatibility rules, the deployment context defaults to `upstream`.
