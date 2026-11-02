# Step 0.7 — Early Assignment

**Proposed actions (not executed — eval mode):**

1. **Assign TC-8020** to the current user via `jira.edit_issue(TC-8020, assignee=<current-user-account-id>)`
2. **Transition TC-8020 to Assigned** — discover the Assigned transition via `jira.get_transitions(TC-8020)`, then execute `jira.transition_issue(TC-8020, <assigned-transition-id>)`

The issue is currently in **New** status, so the transition to Assigned proceeds.

---

# Step 1 — Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| CVSS | 8.1 (High) |
| Existing comments | _(none)_ |

## Stream Scope Resolution

Issue summary contains stream suffix `[rhtpa-2.2]` → mapped to **2.2.x** stream from Version Streams table. Triage is scoped to the 2.2.x stream. However, all streams are checked for cross-stream impact analysis per Important Rule 4.

## Ecosystem Detection

Library **tokio** is a Rust crate → ecosystem is **Cargo** (read from Ecosystem Mappings in security-matrix.md). Cargo is a source dependency ecosystem → remediation produces **2 tasks** per affected stream (upstream backport + downstream propagation).
