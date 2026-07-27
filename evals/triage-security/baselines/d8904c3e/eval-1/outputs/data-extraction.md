# Step 0.7 -- Assign and Transition to Assigned

## Early Assignment Actions

1. **Retrieve current user's Jira account ID:**

   ```
   jira.user_info()
   ```

   Result: current user account ID retrieved (e.g., `5f8b9c2d1a3e4f0012345678`)

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

   TC-8001 was previously Unassigned. Now assigned to the current user.

3. **Discover the target transition dynamically:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Select the transition whose target status name is "Assigned". The transition ID is discovered at runtime from the Vulnerability workflow (not hardcoded).

4. **Transition to Assigned:**

   TC-8001 is currently in "New" status. Transition to "Assigned":

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

   TC-8001 status: New --> Assigned

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
- Mapped stream: **2.2.x** (matches Version Streams table entry for `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x** (scoped issue -- Steps 3-8 apply to this stream; other streams checked for cross-stream impact)

## Ecosystem Detection

- Vulnerable library: quinn-proto (Rust crate)
- Ecosystem: **Cargo**
- Category: **Source dependency** (2 tasks per affected stream: upstream backport + downstream propagation)
- Lock file: `Cargo.lock`
- Check command: `git show <tag>:Cargo.lock`
