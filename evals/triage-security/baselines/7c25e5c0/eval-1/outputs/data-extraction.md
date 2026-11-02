# Step 0.7 — Early Assignment

Before data extraction, assign the CVE issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID**: `jira.user_info()` → (current user account ID)
2. **Assign issue to current user**: `jira.edit_issue(TC-8001, assignee=<current-user-account-id>)`
3. **Discover target transition**: `jira.get_transitions(TC-8001)` → select transition whose target status name is "Assigned"
4. **Transition to Assigned**: `jira.transition_issue(TC-8001, <assigned-transition-id>)`

The issue is currently in **New** status, so the transition to Assigned proceeds. Assignment provides immediate visibility into who is triaging and enables Step 7 (Concurrent Triage Detection).

---

# Step 1 — Data Extraction

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` → maps to the **2.2.x** stream in Version Streams configuration. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library **quinn-proto** is a Rust crate. Reading the Ecosystem Mappings table from the 2.2.x stream's security-matrix.md:

| Ecosystem | Repository | Lock File | Check Command | Upstream Branch |
|-----------|------------|-----------|---------------|-----------------|
| Cargo | backend | `Cargo.lock` | `git show <tag>:Cargo.lock` | `release/0.4.z` |

Detected ecosystem: **Cargo** (source dependency ecosystem).

Per the ecosystem classification table, Cargo produces **2 tasks per stream**: upstream backport + downstream propagation.
