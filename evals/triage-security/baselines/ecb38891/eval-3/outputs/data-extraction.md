# Step 0.7 -- Early Assignment

Before extracting CVE data, assign and transition the issue:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8003 to the current user:**
   ```
   jira.edit_issue("TC-8003", assignee=<current-user-account-id>)
   ```

3. **Discover transitions:**
   ```
   jira.get_transitions("TC-8003")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8003", <assigned-transition-id>)
   ```

# Step 1 -- Data Extraction

## Proposed Jira API Calls

```
jira.get_issue("TC-8003")
jira.get_issue_remote_links("TC-8003")
```

## Extracted CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 (versions before 0.11.14) |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | _(none in remote links)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`. Mapped to configured Version Stream **2.2.x** from Security Configuration. The issue is **stream-scoped** to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **quinn-proto**, a Rust crate. Based on the Ecosystem Mappings table in the 2.2.x stream's security-matrix.md, this maps to the **Cargo** ecosystem.

- Lock File: `Cargo.lock`
- Check Command: `git show <tag>:Cargo.lock`
- Upstream Branch: `release/0.4.z`
- Ecosystem category: **Source dependency** (2 tasks per stream: upstream backport + downstream propagation)
