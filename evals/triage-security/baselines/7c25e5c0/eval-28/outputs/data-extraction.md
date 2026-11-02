# Step 0.7 — Early Assignment

**Proposed actions (not executed — eval mode):**

1. **Assign TC-8060** to the current user via `jira.edit_issue(TC-8060, assignee=<current-user-account-id>)`
2. **Transition TC-8060 to Assigned** — discover the Assigned transition dynamically via `jira.get_transitions(TC-8060)`, then `jira.transition_issue(TC-8060, <assigned-transition-id>)`

The issue is currently in **New** status, so the transition proceeds.

---

# Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-99010 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.5 |
| Fixed version | 0.4.5 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/hyperium/h2/pull/800 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-99010 |
| Due date | 2026-08-15 |
| Reporter | psirt-analyst (557058:psirt-analyst-mock-id) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` → mapped to stream **2.2.x**.
Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

Library **h2** is a Rust crate. Matched to **Cargo** ecosystem from the 2.2.x stream's Ecosystem Mappings table.

Cargo is a source dependency ecosystem → remediation produces **2 tasks** per stream (upstream backport/bump + downstream propagation).

## Deployment Context

Repository rhtpa-backend: Source Repositories table has no Deployment Context column → default to **upstream**.
