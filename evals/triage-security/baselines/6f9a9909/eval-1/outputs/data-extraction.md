# Step 0.7 -- Early Assignment Actions

## Assign to Current User

Action: Assign TC-8001 to the current user.

```
jira.user_info() -> retrieve current user account ID
jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
```

## Transition to Assigned

Action: Transition TC-8001 from New to Assigned status.

```
jira.get_transitions("TC-8001") -> discover transition ID for target status "Assigned"
jira.transition_issue("TC-8001", <assigned-transition-id>)
```

The issue is currently in New status, so the transition proceeds. Assignment provides
immediate visibility into who is actively triaging this issue and enables concurrent
triage detection in Step 7.

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
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | [quinn-rs/quinn#2048](https://github.com/quinn-rs/quinn/pull/2048) |
| Advisory URL | [GHSA-2026-qp73-x4mq](https://github.com/advisories/GHSA-2026-qp73-x4mq) |
| CVE record URL | [CVE-2026-31812](https://www.cve.org/CVERecord?id=CVE-2026-31812) |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to stream **2.2.x** from the Version Streams table.
This issue is **scoped** to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table
for both streams lists **Cargo** with lock file `Cargo.lock` and check command
`git show <tag>:Cargo.lock`. Cargo is a source dependency ecosystem, which means
remediation produces 2 tasks per stream (upstream backport + downstream propagation).
