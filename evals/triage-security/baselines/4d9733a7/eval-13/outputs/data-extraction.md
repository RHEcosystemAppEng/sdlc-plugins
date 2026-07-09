# Step 1 -- Data Extraction for TC-8001

## Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID**: `jira.user_info()`
2. **Assign TC-8001 to current user**: `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)`
3. **Discover transitions**: `jira.get_transitions("TC-8001")` -- select the transition whose target status is "Assigned"
4. **Transition to Assigned**: `jira.transition_issue("TC-8001", <assigned-transition-id>)` -- issue is currently in New status, so the transition proceeds

## Extracted CVE Data

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
| Upstream fix PR | quinn-rs/quinn#2048 (https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | GHSA-2026-qp73-x4mq (https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

### Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** stream in Version Streams configuration. Triage is scoped to the 2.2.x stream.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The 2.2.x stream's Ecosystem Mappings table lists **Cargo** as a supported ecosystem with Lock File `Cargo.lock` and Check Command `git show <tag>:Cargo.lock`. Ecosystem: **Cargo**.
