# Step 0.7 -- Early Assignment Actions

The following Jira mutations are proposed (not executed) for TC-8001:

## 1. Assign to Current User

**Proposed action:** Assign TC-8001 to the current user.

- Current assignee: Unassigned
- Operation: `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)`
- Rationale: Provides immediate visibility into who is actively triaging this CVE and enables Step 7 (Concurrent Triage Detection) to identify active work.

The current user's Jira account ID would be retrieved via `jira.user_info()`.

## 2. Transition to Assigned Status

**Proposed action:** Transition TC-8001 from New to Assigned.

- Current status: New
- Target status: Assigned
- Operation: First `jira.get_transitions("TC-8001")` to discover the transition ID for the "Assigned" target status, then `jira.transition_issue("TC-8001", <assigned-transition-id>)`
- Rationale: The issue is in New status, so the transition proceeds. If the issue were already in Assigned or a later status, the transition would be skipped (but assignment in step 1 still proceeds).

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
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x** (scoped issue -- Steps 3-4 apply only to this stream; cross-stream impact checked via Case A)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Remediation task count per stream: 2 (upstream fix + downstream propagation)

## Deployment Context

- Affected repository: rhtpa-backend
- Deployment Context column: absent from Source Repositories table
- Deployment context: defaults to `upstream` (but coordination guidance omitted per backward-compatibility rule)
