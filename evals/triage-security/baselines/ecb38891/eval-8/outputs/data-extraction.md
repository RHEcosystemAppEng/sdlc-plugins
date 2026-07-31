# Step 0.7 — Assign and Transition to Assigned

Before extracting CVE data, assign the issue and transition it to Assigned status:

1. **Retrieve current user's Jira account ID:**
   ```
   jira.user_info() -> account ID: <current-user-account-id>
   ```

2. **Assign TC-8010 to the current user:**
   ```
   jira.edit_issue("TC-8010", assignee=<current-user-account-id>)
   ```

3. **Discover the Assigned transition:**
   ```
   jira.get_transitions("TC-8010")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8010", <assigned-transition-id>)
   ```

---

# Step 1 — Data Extraction

**Issue**: TC-8010
**Source**: `jira.get_issue("TC-8010")` and `jira.get_issue_remote_links("TC-8010")`

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-44492 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | axios |
| Affected version range | versions before 1.8.2 (< 1.8.2) |
| Fixed version | 1.8.2 |
| CVSS | 8.1 (High) |
| Upstream fix PR | _(not provided in remote links)_ |
| Advisory URL | https://github.com/advisories/GHSA-2026-ax91-r7pp |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-44492 |
| Due date | 2026-08-01 |
| Existing comments | _(none)_ |
| Reporter | _(from Jira issue reporter field)_ |
| Upstream Affected Component (customfield_10632) | axios |
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | rhtpa-2.2 |

## Stream Scope Resolution

- Issue summary contains stream suffix: `[rhtpa-2.2]`
- Mapped to Version Stream: **2.2.x** (Konflux release repo: rhtpa-release.0.4.z)
- Issue is **stream-scoped** to 2.2.x

## Ecosystem Detection

- Library: axios
- Ecosystem: **npm** (JavaScript/TypeScript HTTP client library)
- Category: **Source dependency** (produces 2 tasks per stream: upstream backport + downstream propagation)
- Lock file: `package-lock.json`
- Check command: per Ecosystem Mappings table

## Deployment Context Lookup

- Source Repositories table does not include a Deployment Context column
- Default: all repositories default to `upstream`
