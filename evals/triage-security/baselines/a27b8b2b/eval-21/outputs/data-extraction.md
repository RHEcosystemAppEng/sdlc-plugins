# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID**: `jira.user_info()` returns the current user.
2. **Assign TC-8020 to current user**: `jira.edit_issue("TC-8020", assignee=<current-user-account-id>)`
3. **Discover transitions**: `jira.get_transitions("TC-8020")` -- select the transition whose target status name is "Assigned".
4. **Transition to Assigned**: `jira.transition_issue("TC-8020", <assigned-transition-id>)` -- the issue is currently in New status, so the transition proceeds.

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-31812 |
| **Issue Key** | TC-8020 |
| **Summary** | CVE-2026-31812 quinn-proto - Panic on large stream counts [rhtpa-2.2] |
| **Status** | New |
| **Vulnerable library** | quinn-proto |
| **Affected version range** | < 0.11.14 |
| **Fixed version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Ecosystem** | Cargo (Rust crate -- quinn-proto) |
| **Affected component** | pscomponent:org/rhtpa-server |
| **Upstream Affected Component** | quinn-proto (customfield_10632) |
| **PSIRT-claimed version** | [rhtpa-2.2] |
| **Stream scope** | 2.2.x (scoped to rhtpa-release.0.4.z) |
| **Affects Versions (Jira)** | RHTPA 2.0.0 |
| **Due date** | 2026-07-15 |
| **Upstream fix PR** | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| **Advisory URL** | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| **CVE record URL** | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| **Existing comments** | None |
| **Deployment context** | upstream (default -- no Deployment Context column in Source Repositories) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in Version Streams configuration (Konflux release repo: `rhtpa-release.0.4.z`). Triage is scoped to this stream only.

## Ecosystem Detection

The library `quinn-proto` is a Rust crate. Per the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem. Cargo is a source dependency ecosystem, so remediation produces two tasks per stream (upstream backport + downstream propagation).
