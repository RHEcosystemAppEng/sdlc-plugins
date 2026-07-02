# Step 0.7 -- Early Assignment Actions

## Proposed Actions

1. **Retrieve current user account ID:**
   ```
   jira.user_info()
   ```

2. **Assign TC-8001 to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```
   Rationale: TC-8001 is currently Unassigned. Assigning provides visibility into who is actively triaging.

3. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is "Assigned". Do not hardcode a transition ID.

4. **Transition TC-8001 from New to Assigned:**
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```
   Rationale: TC-8001 is currently in "New" status. Transitioning to "Assigned" signals active triage and enables Step 7 (Concurrent Triage Detection).

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

- Summary suffix: `[rhtpa-2.2]`
- Mapped stream: **2.2.x** (matches Version Streams row: 2.2.x at rhtpa-release.0.4.z)
- Issue stream scope: **2.2.x only** (scoped issue)

## Ecosystem Detection

- Library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
- Upstream branch (2.2.x stream): `release/0.4.z`
- Upstream branch (2.1.x stream): `release/0.3.z`

## Deployment Context

- Repository: rhtpa-backend
- Deployment context: **upstream** (default -- no Deployment Context column in Source Repositories table)
