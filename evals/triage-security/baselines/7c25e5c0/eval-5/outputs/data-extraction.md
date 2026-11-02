# Step 0.7 — Early Assignment

Before data extraction, the following early assignment actions are performed:

1. **Assign TC-8005** to the current user via `jira.edit_issue(TC-8005, assignee=<current-user-account-id>)`
2. **Transition TC-8005 to Assigned** — discover the Assigned transition via `jira.get_transitions(TC-8005)`, then execute `jira.transition_issue(TC-8005, <assigned-transition-id>)`. The issue is currently in New status, so the transition proceeds.

# Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] → scoped to 2.2.x stream |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | versions before 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| Upstream fix PR | _(none — RPM system package, fix via errata)_ |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| CVSS | 7.1 (High) |
| Existing comments | _(none)_ |

## Ecosystem Detection

The library **openssl-libs** is an RPM system package — not a Cargo crate or npm package. The Ecosystem Mappings table in the 2.2.x stream's security-matrix.md lists:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

**Detected ecosystem: RPM** (system package). This means:
- Version extraction uses `rpms.lock.yaml` data
- Remediation creates a **single task** (Konflux release repo fix), not the two-task upstream+downstream flow used for source dependency ecosystems

## Stream Scope

Issue summary contains `[rhtpa-2.2]` → scoped to the **2.2.x** stream. Only versions from the 2.2.x supportability matrix will be analyzed.

## Deployment Context

The affected repository rhtpa-backend is looked up in the Source Repositories table. No Deployment Context column is present in the configuration, so the default `upstream` is used.
