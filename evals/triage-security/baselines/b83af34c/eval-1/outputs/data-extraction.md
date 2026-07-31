# Step 0.7 -- Assign and Transition to Assigned

Before extracting CVE data, the following early assignment actions are proposed:

1. **Retrieve the current user's Jira account ID:**
   - Proposed action: `jira.user_info()` to get the current user's account ID.

2. **Assign TC-8001 to the current user:**
   - Proposed action: `jira.edit_issue("TC-8001", assignee=<current-user-account-id>)`
   - This ensures visibility into who is actively triaging the issue.

3. **Discover the Assigned transition:**
   - Proposed action: `jira.get_transitions("TC-8001")` to find the transition whose target status name is "Assigned".
   - Do NOT hardcode a transition ID -- discover it dynamically from the Vulnerability workflow.

4. **Transition TC-8001 from New to Assigned:**
   - Proposed action: `jira.transition_issue("TC-8001", <assigned-transition-id>)`
   - The issue is currently in New status, so the transition to Assigned will proceed.

These actions provide immediate visibility into who is triaging the issue and enable Step 7 (Concurrent Triage Detection) to reliably identify active work.

---

# Step 1 -- Data Extraction

## Parsed CVE Data from TC-8001

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| CVSS | 7.5 (High) |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains `[rhtpa-2.2]`, which maps to the configured **2.2.x** Version Stream (Konflux release repo: rhtpa-release.0.4.z). This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, which is a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

- Ecosystem: **Cargo**
- Category: **Source dependency**
- Remediation tasks per stream: **2** (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`

## Deployment Context

The affected repository (rhtpa-backend) is listed in the Source Repositories table. No Deployment Context column is present in the Source Repositories table, so the default deployment context of `upstream` applies.
