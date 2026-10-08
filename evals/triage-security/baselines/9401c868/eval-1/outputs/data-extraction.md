# Step 0.7 -- Early Assignment Actions

## Assign Issue to Current User

**Action**: Retrieve current user's Jira account ID via `jira.user_info()`, then assign TC-8001:

```
jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
```

**Rationale**: TC-8001 is currently Unassigned. Assigning immediately provides visibility into who is actively triaging this CVE and enables concurrent triage detection (Step 7).

## Transition to Assigned Status

**Action**: Discover the target transition dynamically:

```
jira.get_transitions("TC-8001")
```

Select the transition whose target status name is `"Assigned"`. Do not hardcode a transition ID -- Vulnerability issues use a different Jira workflow than Task issues.

```
jira.transition_issue("TC-8001", <assigned-transition-id>)
```

**Rationale**: TC-8001 is currently in `New` status. Transitioning to `Assigned` signals active triage and enables Step 7 (Concurrent Triage Detection) to reliably identify active work.

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
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (no comments) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` which maps to the **2.2.x** version stream (Konflux release repo `rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x

## Ecosystem Detection

**Ecosystem**: Cargo (quinn-proto is a Rust crate)

The 2.2.x stream's Ecosystem Mappings table configures Cargo with:
- Repository: backend
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`

**Ecosystem classification**: Source dependency (Cargo) -- 2 tasks per stream when remediation is needed (upstream backport or dependency bump + downstream propagation).

## Deployment Context

Repository `rhtpa-backend` deployment context: `upstream` (default -- no Deployment Context column present in Source Repositories table).
