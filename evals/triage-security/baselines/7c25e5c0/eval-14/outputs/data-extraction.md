# Step 0.7 — Early Assignment

Before data extraction, the following actions are performed:

1. **Assign CVE issue TC-8005** to the current user via `jira.edit_issue(TC-8005, assignee=<current-user-account-id>)`
2. **Transition to Assigned**: retrieve available transitions via `jira.get_transitions(TC-8005)`, select the transition whose target status is "Assigned", and execute `jira.transition_issue(TC-8005, <assigned-transition-id>)`

The issue is currently in New status, so both assignment and transition proceed.

# Step 1 — Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-40215 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | openssl-libs |
| Affected version range | < 3.0.7-28.el9_4 |
| Fixed version | 3.0.7-28.el9_4 |
| CVSS | 7.1 (High) |
| Advisory URL | https://access.redhat.com/errata/RHSA-2026:4021 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-40215 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` → maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `openssl-libs` is an RPM system package. The Ecosystem Mappings table for the 2.2.x stream lists:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| RPM | — | `rpms.lock.yaml` | `git show <tag>:rpms.lock.yaml` | — |

**Detected ecosystem**: RPM (system package)

RPM is classified as a **system package ecosystem** in the ecosystem classification table. Remediation creates a single task per stream (Konflux release repo fix), not the two-task upstream+downstream flow used for source dependency ecosystems.
