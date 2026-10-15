# Step 0.7 — Early Assignment Actions

Before extracting CVE data, perform the following early assignment actions:

1. **Assign the CVE issue to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

2. **Discover the target transition dynamically:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned".

3. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

---

# Step 1 — Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (scoped) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Ecosystem | Cargo (Rust crate — detected from library name and Ecosystem Mappings table) |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Reporter | (from Jira issue reporter field) |
| Deployment context | upstream (default — no Deployment Context column in Source Repositories) |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to stream 2.2.x, but all supported versions (including 2.1.x) are checked for cross-stream impact analysis per Rule 4.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table in each stream's security-matrix.md lists Cargo as a configured ecosystem. Cargo is a **source dependency ecosystem**, which means remediation produces **two tasks per affected stream**: an upstream backport task and a downstream propagation subtask.
