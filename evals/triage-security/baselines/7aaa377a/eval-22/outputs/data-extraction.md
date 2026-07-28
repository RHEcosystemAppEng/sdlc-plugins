# Step 0 -- Validate Project Configuration

Configuration extracted from CLAUDE.md:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Upstream Affected Component custom field**: customfield_10632
- **Source Repositories**: rhtpa-backend (no Deployment Context column present -- defaulting all repositories to `upstream`)

### Version Streams

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |
| 2.2.x | git.example.com/rhtpa/rhtpa-release.0.4.z | /home/dev/repos/rhtpa-release.0.4.z |

# Step 0.3 -- Matrix Staleness Check

Security matrix `Last-Updated` timestamp: 2026-06-28T10:00:00Z
Current date: 2026-07-28
Days since last update: 30 days

The matrix is older than the 14-day default threshold.

> Security matrix was last updated on 2026-06-28 (30 days ago). The matrix may not reflect recent releases.
>
> Options:
> 1. **Refresh now** -- re-run matrix population (setup Step 10.6) for this stream
> 2. **Proceed anyway** -- continue triage with the current matrix
> 3. **Stop** -- halt triage so I can investigate

(For eval purposes, proceeding with current matrix data.)

# Step 0.7 -- Assign and Transition to Assigned

Proposed actions (not executed -- eval mode):
1. Retrieve the current user's Jira account ID via `jira.user_info()`
2. Assign TC-8021 to the current user via `jira.edit_issue(TC-8021, assignee=<current-user-account-id>)`
3. Discover available transitions via `jira.get_transitions(TC-8021)` and select the transition whose target status is "Assigned"
4. Transition TC-8021 from New to Assigned via `jira.transition_issue(TC-8021, <assigned-transition-id>)`

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-31812 |
| **Affected component** | pscomponent:org/rhtpa-server |
| **Product version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.0.0 |
| **Vulnerable library** | quinn-proto |
| **Affected version range** | < 0.11.14 |
| **Fixed version** | 0.11.14 |
| **CVSS** | 7.5 (High) |
| **Upstream Affected Component** | quinn-proto (from customfield_10632) |
| **Upstream fix PR** | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| **Advisory URL** | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| **CVE record URL** | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| **Due date** | 2026-07-15 |
| **Existing comments** | None |

### Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream for Steps 3-4, but all streams are analyzed for version impact in Step 2.

### Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for the 2.2.x stream lists **Cargo** as a supported ecosystem with:
- **Repository**: backend
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock`
- **Upstream Branch**: `release/0.4.z`

Ecosystem classification: **Source dependency** (Cargo) -- remediation produces 2 tasks per stream (upstream backport + downstream propagation).

### Deployment Context Lookup

The affected repository `rhtpa-backend` is found in the Source Repositories table. The Deployment Context column is absent from the table, so the deployment context defaults to `upstream`.
