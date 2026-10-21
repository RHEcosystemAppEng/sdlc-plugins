# Step 0.8 -- Early Assignment Actions

Before proceeding with data extraction, the following assignment actions would be
performed on TC-8001:

1. **Retrieve current user's Jira account ID** via `jira.user_info()`.
2. **Assign TC-8001 to the current user** via `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`.
3. **Discover the Assigned transition** via `jira.get_transitions(TC-8001)` -- select the transition whose target status name is "Assigned".
4. **Transition TC-8001 from New to Assigned** via `jira.transition_issue(TC-8001, <assigned-transition-id>)`.

The issue is currently in **New** status and **Unassigned**, so both the assignment
and the status transition apply. This provides immediate visibility that the issue
is being actively triaged and enables Step 7 (Concurrent Triage Detection) to
identify active work on this component.

No Jira operations were actually performed -- these are the proposed actions.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (current Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS score | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Issue status | New |
| Assignee | Unassigned |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** stream in the Version Streams table:

- Stream suffix: `[rhtpa-2.2]` maps to stream `2.2.x`
- Konflux Release Repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Local Path: `/home/dev/repos/rhtpa-release.0.4.z`

The issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will be scoped to this
stream, while the full version impact analysis (Step 2) covers all streams to
detect cross-stream impact.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings
table for both streams lists **Cargo** as a configured ecosystem:

- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Tasks per stream: 2 (upstream backport or dependency bump + downstream propagation)

## Deployment Context

The affected repository `rhtpa-backend` is listed in the Source Repositories table.
The Source Repositories table does **not** include a Deployment Context column, so
coordination guidance will be omitted from remediation task descriptions (backward
compatibility behavior).

## Configuration Notes

The following optional Security Configuration fields are **not configured**:
- ProdSec contact email -- skip silently
- ProdSec Jira account ID -- skip @mentions silently
- Upstream Affected Component custom field -- Step 4.3 (cross-CVE overlap) and Step 7 (concurrent triage) will be skipped
- PS Component custom field -- not applicable without Upstream Affected Component
- Stream custom field -- not applicable without Upstream Affected Component
- Embargo policy URL -- Step 1.7 (embargo check) will be skipped entirely

The following optional field **is** configured:
- VEX Justification custom field: customfield_12345 (used in Case C close scenarios)
