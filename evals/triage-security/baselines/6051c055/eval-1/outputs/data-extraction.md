# Step 0.7 -- Assign and Transition to Assigned

## Early Assignment Actions

1. **Retrieve current user's Jira account ID:**

   ```
   jira.user_info()
   ```
   Result: current user account ID retrieved (e.g., `5f1a2b3c4d5e6f7a8b9c0d1e`)

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee="<current-user-account-id>")
   ```

   Proposed action: Assign TC-8001 from Unassigned to the current user, providing immediate visibility into who is actively triaging this issue.

3. **Discover the target transition dynamically:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Select the transition whose target status name is "Assigned". The transition ID is discovered at runtime -- not hardcoded, since Vulnerability issues use a different Jira workflow than Task issues.

4. **Transition TC-8001 from New to Assigned:**

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

   Proposed action: Transition TC-8001 from status "New" to status "Assigned". This enables Step 7 (Concurrent Triage Detection) to reliably identify active work on this issue.

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
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | (none) |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]` maps to stream **2.2.x**
- Matched to Version Streams table entry: 2.2.x at `git.example.com/rhtpa/rhtpa-release.0.4.z`
- Issue stream scope: **2.2.x** (scoped issue -- Steps 3 and 4 apply only to this stream; Case B handles cross-stream impact)

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch (2.2.x stream): `release/0.4.z`
- Repository: backend

## Deployment Context

- Affected repository: rhtpa-backend (matched from component label `pscomponent:org/rhtpa-server`)
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)
