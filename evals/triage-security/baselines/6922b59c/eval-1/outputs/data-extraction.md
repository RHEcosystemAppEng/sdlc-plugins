# Step 0.8 -- Early Assignment Actions

The following actions would be performed on TC-8001 before data extraction:

1. **Assign TC-8001 to the current user**: The issue is currently Unassigned.
   Retrieve current user's account ID via `jira.user_info()`, then assign:
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

2. **Transition TC-8001 from New to Assigned**: The issue is currently in `New` status.
   Discover the Assigned transition dynamically via `jira.get_transitions("TC-8001")`,
   select the transition whose target status name is `"Assigned"`, then execute:
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

No Jira operations were actually performed -- these are the planned actions only.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Due date | 2026-07-15 |
| Assignee | Unassigned |
| Status | New |
| Existing comments | None |

## Remote Links

| Type | URL | Description |
|------|-----|-------------|
| Advisory | https://github.com/advisories/GHSA-2026-qp73-x4mq | GitHub Advisory |
| CVE Record | https://www.cve.org/CVERecord?id=CVE-2026-31812 | CVE Record |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 | Upstream fix PR |

## Stream Scope Resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream
(Konflux release repo: `git.example.com/rhtpa/rhtpa-release.0.4.z`).

This issue is **stream-scoped** to 2.2.x. Steps 3 and 4 will scope corrections to
this stream only. Cross-stream impact on 2.1.x will be handled via Case A in Step 8.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings tables
in both streams' matrices list **Cargo** as the ecosystem for the `backend` repository,
with `Cargo.lock` as the lock file and `git show <tag>:Cargo.lock` as the check command.

Classification: **Source dependency (Cargo)** -- produces 2 remediation tasks per stream
(dependency bump or upstream backport + downstream propagation).

## Deployment Context

The affected repository `rhtpa-backend` is listed in Source Repositories with the
default deployment context of `upstream` (Deployment Context column is absent from the
mock configuration, so default applies).
