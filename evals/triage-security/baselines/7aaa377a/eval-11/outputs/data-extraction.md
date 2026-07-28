# Step 0.7 — Assign and Transition to Assigned

**Proposed actions** (require confirmation before execution):

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8021 to the current user:**
   ```
   jira.edit_issue("TC-8021", assignee=<current-user-account-id>)
   ```

3. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8021")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition TC-8021 to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8021", <assigned-transition-id>)
   ```

---

# Step 1 — Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |
| Issue links | None |
| Assignee | Unassigned |
| Status | New |

## Stream Scope Resolution

The issue summary contains the stream suffix `[rhtpa-2.1]`, which maps to the **2.1.x** version stream in the Version Streams table:

| Stream | Konflux Release Repo | Local Path |
|--------|----------------------|------------|
| 2.1.x | git.example.com/rhtpa/rhtpa-release.0.3.z | /home/dev/repos/rhtpa-release.0.3.z |

**Issue stream scope**: 2.1.x (scoped to a single stream)

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the Ecosystem Mappings table for the 2.1.x stream, the ecosystem is **Cargo** (source dependency). This determines:

- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Remediation task structure: 2 tasks per stream (upstream backport + downstream propagation)

## Custom Fields

| Custom Field | Value |
|---|---|
| customfield_10632 (Upstream Affected Component) | tokio |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-server |
| customfield_10832 (Stream) | rhtpa-2.1 |

## Deployment Context Lookup

Source repository: rhtpa-backend. No Deployment Context column is present in the Source Repositories table — defaulting to `upstream`.
