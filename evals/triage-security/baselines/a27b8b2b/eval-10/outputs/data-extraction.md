# Step 0.7 -- Early Assignment

Before extracting CVE data, the issue is assigned to the current user and
transitioned to Assigned status for triage visibility.

**Proposed actions:**

1. **Retrieve current user account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8020 to the current user:**
   ```
   jira.edit_issue("TC-8020", assignee=<current-user-account-id>)
   ```

3. **Discover available transitions:**
   ```
   jira.get_transitions("TC-8020")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8020", <assigned-transition-id>)
   ```

This step provides immediate visibility into who is triaging the issue and
enables Step 7 (Concurrent Triage Detection) to identify active work.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0, RHTPA 2.2.1 |
| Due date | 2026-08-15 |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Existing comments | None |
| Upstream Affected Component (customfield_10632) | tokio |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-server |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the
**2.2.x** stream in the Version Streams table. This issue is scoped to the
2.2.x stream for Steps 3-8.

## Ecosystem Detection

The vulnerable library **tokio** is a Rust crate. Based on the Ecosystem
Mappings table in the 2.2.x stream's security-matrix.md, this maps to the
**Cargo** ecosystem.

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.4.z`
- Ecosystem category: **Source dependency** -- produces 2 remediation tasks per stream (upstream backport + downstream propagation)

## Deployment Context

The Source Repositories table does not include a Deployment Context column.
All repositories default to `upstream`. The Coordination Guidance subsection
will be omitted from remediation task descriptions (backward compatibility).
