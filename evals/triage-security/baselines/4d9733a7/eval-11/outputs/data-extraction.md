# Step 0.7 -- Early Assignment

**Proposed actions:**

1. **Assign TC-8021** to the current user via `jira.edit_issue(TC-8021, assignee=<current-user-account-id>)`
2. **Transition TC-8021 to Assigned** via `jira.transition_issue(TC-8021, <assigned-transition-id>)` (discovered dynamically from `jira.get_transitions(TC-8021)`)

---

# Step 1 -- Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | versions before 1.42.0 (< 1.42.0) |
| Fixed version | 1.42.0 |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| CVSS | 8.1 (High) |

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.1]` -- mapped to stream **2.1.x** from the Version Streams table.

### Ecosystem detection

The library **tokio** is a Rust crate. Ecosystem: **Cargo**.
