# Step 0.7 -- Early Assignment

**Proposed actions:**

1. **Assign TC-8011** to the current user via `jira.edit_issue(TC-8011, assignee=<current-user-account-id>)`
2. **Transition TC-8011 to Assigned** via `jira.transition_issue(TC-8011, <assigned-transition-id>)` (discovered dynamically from `jira.get_transitions(TC-8011)`)

These actions provide immediate visibility into who is actively triaging the issue.

---

# Step 1 -- Data Extraction

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | versions before 5.98.0 (< 5.98.0) |
| Fixed version | 5.98.0 |
| Upstream fix PR | N/A |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Existing comments | None |
| CVSS | 7.8 (High) |

### Stream scope resolution

Issue summary contains stream suffix `[rhtpa-2.2]` -- mapped to stream **2.2.x** from the Version Streams table.

### Ecosystem detection

The library **webpack** is an npm JavaScript package. Ecosystem: **npm**.

### Custom Fields

- **customfield_10632** (Upstream Affected Component): webpack
- **customfield_10669** (PS Component): pscomponent:org/rhtpa-ui
- **customfield_10832** (Stream): rhtpa-2.2
