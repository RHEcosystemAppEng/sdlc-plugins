# Data Extraction: TC-8002

## Step 0.7 — Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user** — `jira.user_info()` to get the current user's Jira account ID.
2. **Assign TC-8002** — `jira.edit_issue(TC-8002, assignee=<current-user-account-id>)` to assign the issue to the current user.
3. **Discover Assigned transition** — `jira.get_transitions(TC-8002)` to find the transition whose target status is "Assigned". Do not hardcode a transition ID.
4. **Transition to Assigned** — `jira.transition_issue(TC-8002, <assigned-transition-id>)` since the issue is currently in New status.

## Step 0.3 — Matrix Staleness Check

The security-matrix.md has `<!-- Last-Updated: 2026-06-28T10:00:00Z -->`. This is within the 14-day threshold (5 days ago as of 2026-07-03). No staleness warning is displayed. Proceeding silently.

## Parsed CVE Data (Step 1)

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-28940 |
| Jira Issue Key | TC-8002 |
| Issue Type | Vulnerability |
| Status | New |
| Affected Component | pscomponent:org/rhtpa-server |
| Product Version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable Library | serde_json |
| Affected Version Range | versions before 1.0.135 (i.e., < 1.0.135) |
| Fixed Version | 1.0.135 |
| CVSS Score | 5.3 (Medium) |
| Due Date | 2026-07-30 |
| Assignee | Unassigned (prior to Step 0.7 assignment) |
| Advisory URL | https://github.com/advisories/GHSA-2026-j9r2-m5vk |
| CVE Record URL | https://www.cve.org/CVERecord?id=CVE-2026-28940 |
| Additional Reference | https://rustsec.org/advisories/RUSTSEC-2026-0019.html |
| Existing Comments | None |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream (Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Per Important Rule 4, all supported versions across all streams are checked for version impact assessment.

## Ecosystem Detection

- **Ecosystem**: Cargo (serde_json is a Rust crate)
- **Lock File**: `Cargo.lock`
- **Check Command**: `git show <tag>:Cargo.lock | grep -A2 'name = "serde_json"'`
- **Source Repository**: backend (rhtpa-backend)
- **Upstream Branch (2.1.x)**: `release/0.3.z`
- **Upstream Branch (2.2.x)**: `release/0.4.z`

## Deployment Context

- **Repository**: rhtpa-backend
- **Deployment context**: upstream (default -- no Deployment Context column in Source Repositories table)

## Vulnerability Description

A stack overflow vulnerability in serde_json. Versions before 1.0.135 are vulnerable to unbounded recursion when deserializing deeply nested JSON input. An attacker can craft a JSON payload with thousands of nested arrays or objects causing a process crash. The fix (1.0.135) introduces a configurable recursion limit defaulting to 128 levels of nesting.

## Embargo Check

CVSS 5.3 (Medium) is below the embargo threshold (7.0). No Embargo policy URL is configured in Security Configuration. Step 1.7 is skipped.
