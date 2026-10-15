# Step 0.8 -- Assign and Transition to Assigned

Before data extraction, the following early assignment actions are proposed:

1. **Assign TC-8021 to the current user** -- ensures visibility into who is actively triaging
2. **Transition TC-8021 from New to Assigned** -- the issue is currently in New status, so the Assigned transition applies

These actions would be performed via:
- `jira.edit_issue("TC-8021", assignee=<current-user-account-id>)`
- `jira.get_transitions("TC-8021")` to discover the Assigned transition ID dynamically
- `jira.transition_issue("TC-8021", <assigned-transition-id>)`

> **Note**: No Jira operations were actually performed. These are proposed actions.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.1] |
| Stream scope | rhtpa-2.1 mapped to **2.1.x** stream |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| CVSS | 8.1 (High) |
| Due date | 2026-08-15 |
| Upstream fix PR | [tokio-rs/tokio#7001](https://github.com/tokio-rs/tokio/pull/7001) |
| Advisory URL | [GHSA-2026-tk91-v5pp](https://github.com/advisories/GHSA-2026-tk91-v5pp) |
| CVE record URL | [CVE-2026-55123](https://www.cve.org/CVERecord?id=CVE-2026-55123) |
| Existing comments | None |
| Assignee | Unassigned |
| Issue Links | None |

## Custom Fields

| Custom Field | Value |
|-------------|-------|
| customfield_10632 (Upstream Affected Component) | tokio |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-server |
| customfield_10832 (Stream) | rhtpa-2.1 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.1]`. This maps to the **2.1.x** stream from the Version Streams table in Security Configuration:

- Stream: 2.1.x
- Konflux Release Repo: git.example.com/rhtpa/rhtpa-release.0.3.z
- Local Path: /home/dev/repos/rhtpa-release.0.3.z

Triage is scoped to the 2.1.x stream only.

## Ecosystem Detection

The vulnerable library is **tokio**, a Rust crate. Based on the Ecosystem Mappings table in the 2.1.x stream's security-matrix.md, **Cargo** is the matching ecosystem.

- Category: Source dependency
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
- Upstream branch: `release/0.3.z`
- Remediation task count per stream: 2 (upstream backport + downstream propagation)

## Deployment Context Lookup

The affected repository is **rhtpa-backend** (matched from component label `pscomponent:org/rhtpa-server`). The Source Repositories table does not include a Deployment Context column, so the deployment context defaults to **upstream**.
