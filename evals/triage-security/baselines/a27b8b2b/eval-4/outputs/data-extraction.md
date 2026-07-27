# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user account ID**: `jira.user_info()` -- obtain the current user's Jira account ID.
2. **Assign TC-8004 to the current user**: `jira.edit_issue("TC-8004", assignee=<current-user-account-id>)`.
3. **Discover the Assigned transition**: `jira.get_transitions("TC-8004")` -- select the transition whose target status name is `"Assigned"`. Do NOT hardcode a transition ID.
4. **Transition to Assigned**: `jira.transition_issue("TC-8004", <assigned-transition-id>)` -- the issue is currently in New status, so the transition proceeds.

TC-8004 is now assigned to the current user with status Assigned.

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-33501 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | _(no stream suffix -- unscoped)_ |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.2.0 |
| Vulnerable library | h2 |
| Affected version range | < 0.4.8 |
| Fixed version | 0.4.8 |
| Ecosystem | Cargo |
| Upstream fix PR | https://github.com/hyperium/h2/pull/812 |
| Advisory URL | https://github.com/advisories/GHSA-2026-kv8p-r3n7 |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-33501 |
| Due date | 2026-08-01 |
| CVSS | 7.5 (High) |
| Existing comments | None |
| Deployment context | upstream (default -- no Deployment Context column in Source Repositories table) |

## Stream Scope Resolution

The issue summary is "CVE-2026-33501 h2 - Memory exhaustion via CONTINUATION frames" -- it contains **no stream suffix** in brackets. Per the Stream scope resolution rules, this issue is treated as **unscoped** -- it covers all configured version streams. The version impact analysis in Step 2 will check ALL versions across ALL streams (2.1.x and 2.2.x).

```
Stream scope: UNSCOPED (no suffix)
Streams to analyze: 2.1.x, 2.2.x (all configured streams)
```

## Ecosystem Detection

The vulnerable library is **h2**, a Rust crate (part of the Hyper/Tokio HTTP ecosystem). Checking the Ecosystem Mappings tables in the security matrix:

- Stream 2.1.x Ecosystem Mappings: Cargo is listed with Lock File `Cargo.lock`
- Stream 2.2.x Ecosystem Mappings: Cargo is listed with Lock File `Cargo.lock`

**Detected ecosystem: Cargo** (source dependency category).

Per the ecosystem classification table, Cargo is a source dependency ecosystem, which produces **2 remediation tasks per affected stream** (upstream backport + downstream propagation).
