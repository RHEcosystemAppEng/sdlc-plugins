# Step 0.7 -- Early Assignment

**Proposed actions** (require confirmation):

1. **Assign** TC-8011 to the current user via `jira.edit_issue(TC-8011, assignee=<current-user-account-id>)`
2. **Transition** TC-8011 from New to Assigned status via `jira.transition_issue(TC-8011, <assigned-transition-id>)` (transition ID discovered dynamically from `jira.get_transitions(TC-8011)`)

These actions provide immediate visibility into who is actively triaging the issue and enable Step 7 (Concurrent Triage Detection).

---

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-45678 |
| **Affected component** | pscomponent:org/rhtpa-ui |
| **Product version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable library** | webpack |
| **Affected version range** | versions before 5.98.0 (< 5.98.0) |
| **Fixed version** | 5.98.0 |
| **CVSS** | 7.8 (High) |
| **Upstream fix PR** | _(not provided in remote links)_ |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| **CVE record URL** | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| **Due date** | 2026-08-15 |
| **Existing comments** | None |
| **Assignee** | Unassigned |
| **Existing issue links** | None |

## Stream Scope Resolution

- Summary suffix: `[rhtpa-2.2]`
- Mapped to stream: **2.2.x** (matches Version Streams table row for `rhtpa-release.0.4.z`)
- Issue stream scope: **2.2.x only**

## Ecosystem Detection

- Library: **webpack** -- this is a JavaScript/TypeScript package
- Detected ecosystem: **npm** (JavaScript/TypeScript packages)
- Ecosystem category: **Source dependency** -- remediation creates 2 tasks per stream (upstream backport + downstream propagation)

## Custom Fields

| Custom Field | Value |
|--------------|-------|
| customfield_10632 (Upstream Affected Component) | webpack |
| customfield_10669 (PS Component) | pscomponent:org/rhtpa-ui |
| customfield_10832 (Stream) | rhtpa-2.2 |
