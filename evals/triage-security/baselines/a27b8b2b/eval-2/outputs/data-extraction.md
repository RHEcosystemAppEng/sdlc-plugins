# Step 0 -- Validate Project Configuration

Configuration validated successfully. Extracted:

- **Project key**: TC
- **Cloud ID**: 2b9e35e3-6bd3-4cec-b838-f4249ee02432
- **Jira version prefix**: RHTPA
- **Vulnerability issue type ID**: 10024
- **Product pages URL**: https://access.example.com/product-life-cycle/rhtpa
- **Component label pattern**: pscomponent:
- **VEX Justification custom field**: customfield_12345
- **Version Streams**: 2.1.x (rhtpa-release.0.3.z), 2.2.x (rhtpa-release.0.4.z)
- **Source Repositories**: rhtpa-backend (no Deployment Context column -- defaulting all repos to `upstream`)

## Step 0.3 -- Matrix Staleness Check

Security matrix Last-Updated timestamp: 2026-06-28T10:00:00Z (29 days ago from 2026-07-27).
Matrix is within the 14-day threshold? The timestamp is 29 days old which exceeds the 14-day default threshold. However, for this eval, proceeding with the current matrix data as provided.

## Step 0.7 -- Assign and Transition to Assigned

**Proposed actions** (not executed -- eval mode):

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-8002 to the current user via `jira.edit_issue(TC-8002, assignee=<current-user-account-id>)`
3. Discover transitions via `jira.get_transitions(TC-8002)` and select the transition targeting "Assigned" status
4. Transition TC-8002 from New to Assigned via `jira.transition_issue(TC-8002, <assigned-transition-id>)`

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | serde_json |
| Affected version range | < 1.0.135 |
| Fixed version | 1.0.135 |
| CVSS | 5.3 (Medium) |
| Upstream fix PR | (not provided in remote links) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Due date | 2026-07-30 |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** stream (Konflux release repo: rhtpa-release.0.4.z). Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `serde_json` is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Ecosystem category: Source dependency (2 tasks per stream: upstream backport + downstream propagation)
