# Step 0.7 -- Early Assignment

Before extracting CVE data, assign the issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8021 to current user:**
   ```
   jira.edit_issue("TC-8021", assignee=<current-user-account-id>)
   ```

3. **Discover target transition:**
   ```
   jira.get_transitions("TC-8021")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8021", <assigned-transition-id>)
   ```

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-55123 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.1 (from summary suffix `[rhtpa-2.1]`) |
| Affects Versions (Jira field) | RHTPA 2.1.0, RHTPA 2.1.1 |
| Vulnerable library | tokio |
| Affected version range | < 1.42.0 |
| Fixed version | 1.42.0 |
| Ecosystem | Cargo (Rust crate) |
| CVSS | 8.1 (High) |
| Upstream fix PR | https://github.com/tokio-rs/tokio/pull/7001 |
| Advisory URL | https://github.com/advisories/GHSA-2026-tk91-v5pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-55123 |
| Due date | 2026-08-15 |
| Existing comments | None |

## Stream Scope Resolution

- Issue summary suffix: `[rhtpa-2.1]`
- Matched stream: **2.1.x** (from Version Streams table)
- Triage is scoped to the 2.1.x stream only

## Ecosystem Detection

- Library: tokio (Rust crate)
- Ecosystem: **Cargo** (source dependency)
- Remediation task structure: 2 tasks per stream (upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`

## Deployment Context Lookup

- Affected repository: rhtpa-backend
- Source Repositories table does not include a Deployment Context column
- Default: **upstream**

## Custom Fields

- Upstream Affected Component (customfield_10632): tokio
- PS Component (customfield_10669): pscomponent:org/rhtpa-server
- Stream (customfield_10832): rhtpa-2.1
