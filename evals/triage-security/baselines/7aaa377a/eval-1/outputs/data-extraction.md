# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition it to Assigned status
to provide immediate visibility into who is actively triaging.

**Proposed actions:**

1. **Retrieve current user account ID:**
   ```
   jira.user_info()
   ```
   Result: current user's Jira account ID (e.g., `557058:current-user-id`)

2. **Assign TC-8001 to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
   This ensures the issue shows who is actively triaging it.

3. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned". The transition ID
   is discovered dynamically -- not hardcoded, since Vulnerability issues use a
   different Jira workflow than Task issues.

4. **Transition TC-8001 from New to Assigned:**
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```
   The issue is currently in New status, so the transition proceeds.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

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
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** stream in the configured Version Streams table. The issue is scoped
to stream 2.2.x for Steps 3-8.

However, per Important Rule 4, ALL supported versions across all streams are
checked in the version impact analysis (Step 2).

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the library
name and component context (pscomponent:org/rhtpa-server, a Rust backend service),
the ecosystem is identified as **Cargo**.

The Cargo ecosystem is configured in both streams' Ecosystem Mappings tables:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.3.z` (2.1.x stream), `release/0.4.z` (2.2.x stream)

Cargo is a **source dependency** ecosystem per the classification table. This means
remediation will produce **two tasks per affected stream**: an upstream backport
task and a downstream propagation subtask (with a Blocks dependency).
