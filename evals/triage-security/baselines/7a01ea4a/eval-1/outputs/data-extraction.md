# Step 0.7 -- Early Assignment Actions

## Assign to Current User

Action: Assign TC-8001 to the current user.

```
jira.user_info() -> retrieve current user account ID
jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
```

## Transition to Assigned

The issue is currently in **New** status. Discover the Assigned transition dynamically
and transition to Assigned.

```
jira.get_transitions("TC-8001") -> find transition with target status "Assigned"
jira.transition_issue("TC-8001", <assigned-transition-id>)
```

Result: TC-8001 is now assigned to the current user and in **Assigned** status.

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

The issue summary contains the stream suffix `[rhtpa-2.2]`, which maps to the
configured **2.2.x** version stream (Konflux release repo: `rhtpa-release.0.4.z`).

This issue is **scoped** to stream 2.2.x. Steps 3 and 8 will apply only to versions
within this stream.

## Ecosystem Detection

The vulnerable library **quinn-proto** is a Rust crate. The ecosystem is **Cargo**.

From the 2.2.x stream's Ecosystem Mappings:
- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Repository: backend

## Deployment Context

The affected repository (rhtpa-backend) is found in the Source Repositories table.
No Deployment Context column is configured -- defaulting to `upstream`.
