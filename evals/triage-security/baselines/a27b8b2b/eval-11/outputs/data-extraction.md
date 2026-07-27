# Step 0.7 -- Early Assignment

Before extracting CVE data, the following early assignment actions are performed
on TC-8021:

1. **Retrieve current user's Jira account ID**:
   ```
   jira.user_info()
   ```
   Result: current user account ID retrieved (e.g., `557058:current-user-id`).

2. **Assign TC-8021 to the current user**:
   ```
   jira.edit_issue("TC-8021", assignee=<current-user-account-id>)
   ```
   The issue was previously Unassigned; now assigned to the current user.

3. **Discover the target transition dynamically**:
   ```
   jira.get_transitions("TC-8021")
   ```
   Select the transition whose target status name is `"Assigned"`. Do NOT hardcode
   a transition ID -- Vulnerability issues use a different Jira workflow than Tasks.

4. **Transition TC-8021 to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8021", <assigned-transition-id>)
   ```
   TC-8021 is now in Assigned status, providing immediate visibility into who is
   actively triaging the issue and enabling Step 7 (Concurrent Triage Detection).

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Due date | 2026-08-15 |
| Existing comments | None |
| Existing issue links | None |
| Upstream Affected Component | tokio (customfield_10632) |
| PS Component | pscomponent:org/rhtpa-server (customfield_10669) |
| Stream | rhtpa-2.1 (customfield_10832) |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the
**2.1.x** stream in the Version Streams configuration. Triage is scoped to the
2.1.x stream only.

## Ecosystem Detection

The vulnerable library **tokio** is a Rust crate. Based on the Ecosystem Mappings
table in the 2.1.x stream's security-matrix.md, the ecosystem is **Cargo**.

Cargo is classified as a **source dependency** ecosystem per the ecosystem
classification table, which means remediation produces **two tasks** per stream:
upstream backport + downstream propagation with Blocks dependency.

## Deployment Context Lookup

The Source Repositories table in the Security Configuration does not include a
Deployment Context column. All repositories default to `upstream` per backward
compatibility rules.
