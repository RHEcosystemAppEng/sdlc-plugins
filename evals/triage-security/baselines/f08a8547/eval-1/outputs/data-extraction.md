# Step 0.7 -- Assign and Transition to Assigned

## Early Assignment Actions

1. **Retrieve current user's Jira account ID:**

   ```
   jira.user_info()
   ```

   Result: current user account ID retrieved (e.g., `712020:current-user-id`).

2. **Assign TC-8001 to the current user:**

   ```
   jira.edit_issue("TC-8001", assignee="712020:current-user-id")
   ```

   TC-8001 was previously Unassigned. Now assigned to the current user to provide
   visibility into who is actively triaging this issue.

3. **Discover the target transition dynamically:**

   ```
   jira.get_transitions("TC-8001")
   ```

   Inspected available transitions for TC-8001. Selected the transition whose
   target status name is "Assigned" (transition ID discovered at runtime -- not
   hardcoded).

4. **Transition TC-8001 from New to Assigned:**

   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

   TC-8001 is currently in "New" status. Transitioned to "Assigned" to signal
   active triage is underway. This enables Step 7 (Concurrent Triage Detection)
   to reliably identify that this issue is being worked on.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-31812 |
| Affected component | pscomponent:org/rhtpa-server |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
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

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the
configured Version Stream **2.2.x** (Konflux release repo:
`git.example.com/rhtpa/rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x

## Ecosystem Detection

The vulnerable library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

The Cargo ecosystem is listed in both streams' Ecosystem Mappings tables:
- Stream 2.1.x: Lock File = `Cargo.lock`, Check Command = `git show <tag>:Cargo.lock`, Upstream Branch = `release/0.3.z`
- Stream 2.2.x: Lock File = `Cargo.lock`, Check Command = `git show <tag>:Cargo.lock`, Upstream Branch = `release/0.4.z`

## Deployment Context Lookup

The affected component maps to repository `rhtpa-backend` from the Source
Repositories table. The Source Repositories table does not include a Deployment
Context column, so all repositories default to `upstream`.

Deployment context: **upstream** (default -- no Deployment Context column configured).
