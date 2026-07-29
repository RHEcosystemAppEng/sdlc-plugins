# Step 0.7 -- Early Assignment Actions

## Assign to Current User

Retrieve the current user's Jira account ID:

```
jira.user_info()
```

Assign TC-8001 to the current user:

```
jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
```

## Transition to Assigned

The issue is currently in **New** status. Discover the target transition dynamically:

```
jira.get_transitions("TC-8001")
```

Select the transition whose target status name is "Assigned" and execute:

```
jira.transition_issue("TC-8001", <assigned-transition-id>)
```

TC-8001 is now assigned to the current user and transitioned from New to Assigned status.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Stream scope | 2.2.x (mapped from summary suffix [rhtpa-2.2]) |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | versions before 0.11.14 (< 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo (Rust crate) |
| Ecosystem category | Source dependency (2 tasks per stream: upstream backport + downstream propagation) |
| Deployment context | upstream (default -- no Deployment Context column in Source Repositories table) |
