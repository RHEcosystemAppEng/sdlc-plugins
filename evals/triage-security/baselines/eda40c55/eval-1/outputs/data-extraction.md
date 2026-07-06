# Step 0.7 -- Early Assignment Actions

## Assign and Transition to Assigned

**Issue**: TC-8001
**Current Status**: New
**Current Assignee**: Unassigned

### Actions

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info()
   ```

2. **Assign the issue to the current user:**
   ```
   jira.edit_issue("TC-8001", assignee=<current-user-account-id>)
   ```

3. **Discover target transition:**
   ```
   jira.get_transitions("TC-8001")
   ```
   Select the transition whose target status name is `"Assigned"`.

4. **Transition to Assigned** (issue is in New status):
   ```
   jira.transition_issue("TC-8001", <assigned-transition-id>)
   ```

**Result**: TC-8001 assigned to the current user and transitioned from New to Assigned.

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
| Existing comments | (none) |

## Stream Scope Resolution

Summary suffix `[rhtpa-2.2]` maps to configured Version Stream **2.2.x** (Konflux release repo `rhtpa-release.0.4.z`).

**Issue stream scope**: 2.2.x

## Ecosystem Detection

Library `quinn-proto` is a Rust crate. Ecosystem: **Cargo**.

Lock file: `Cargo.lock`
Check command: `git show <tag>:Cargo.lock | grep -A2 'name = "quinn-proto"'`
Upstream Branch: `release/0.4.z` (from 2.2.x stream Ecosystem Mappings)

## Deployment Context

The Source Repositories table in the project CLAUDE.md does not include a Deployment Context column. Default deployment context: **upstream**.
