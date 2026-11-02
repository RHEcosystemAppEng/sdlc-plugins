# Step 0 — Configuration Extraction

## Source Repositories with Deployment Context

The Source Repositories table in the CLAUDE.md Security Configuration includes a **Deployment Context** column:

| Repository | URL | Local Path | Deployment Context |
|------------|-----|------------|--------------------|
| rhtpa-backend | https://github.com/rhtpa/rhtpa-backend | /home/dev/repos/rhtpa-backend | customer-shipped |

Extracted mapping: `rhtpa-backend → { url: "https://github.com/rhtpa/rhtpa-backend", deployment_context: "customer-shipped" }`

## Step 0.7 — Early Assignment

**Proposed actions** (not executed — eval prohibits Jira calls):
1. Assign TC-8001 to the current user via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
2. Discover the "Assigned" transition via `jira.get_transitions(TC-8001)`
3. Transition TC-8001 from New → Assigned via `jira.transition_issue(TC-8001, <assigned-transition-id>)`

## Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → stream 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Ecosystem | Cargo (Rust crate) |
| Stream scope | 2.2.x (from summary suffix [rhtpa-2.2]) |

### Deployment Context Lookup

The affected component label `pscomponent:org/rhtpa-server` maps to repository `rhtpa-backend`.

Deployment context for rhtpa-backend: **customer-shipped**

This value is recorded as part of the CVE metadata for use in Step 8 when generating Coordination Guidance in remediation task descriptions.
