# Step 0.7 -- Assign and Transition to Assigned

## Actions

1. **Retrieve current user's Jira account ID:**

   ```
   jira.user_info()
   ```

   Result: current user account ID retrieved (e.g., `5f1a2b3c4d5e6f7a8b9c0d1e`).

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

   TC-8001 was previously Unassigned. Now assigned to the current user.

3. **Discover the Assigned transition:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Select the transition whose target status name is `"Assigned"`.

4. **Transition TC-8001 from New to Assigned:**

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

   TC-8001 status: New --> Assigned.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | rhtpa-2.2 |
| Stream scope | 2.2.x |
| Affects Versions (Jira field) | RHTPA 2.0.0 |
| Vulnerable library | quinn-proto |
| Affected version range | < 0.11.14 |
| Fixed version | 0.11.14 |
| CVSS | 7.5 (High) |
| Upstream fix PR | https://github.com/quinn-rs/quinn/pull/2048 |
| Advisory URL | https://github.com/advisories/GHSA-2026-qp73-x4mq |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-31812 |
| Due date | 2026-07-15 |
| Existing comments | None |
| Ecosystem | Cargo |
| Deployment context | upstream (default -- no Deployment Context column in Source Repositories) |

### Stream scope resolution

The issue summary contains the suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream
in the Version Streams table. This issue is scoped to the 2.2.x stream only.

### Ecosystem detection

The vulnerable library `quinn-proto` is a Rust crate. The Ecosystem Mappings table for
the 2.2.x stream lists **Cargo** as a configured ecosystem with lock file `Cargo.lock`
and check command `git show <tag>:Cargo.lock`. Classification: **source dependency**
(2 tasks per stream: upstream fix + downstream propagation).
