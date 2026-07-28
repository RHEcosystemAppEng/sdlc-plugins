# Step 0.7 -- Early Assignment

**Proposed actions** (require confirmation):

1. **Assign TC-8011** to the current user via `jira.edit_issue(TC-8011, assignee=<current-user-account-id>)`
2. **Retrieve available transitions** via `jira.get_transitions(TC-8011)` and select the transition whose target status name is "Assigned"
3. **Transition TC-8011 to Assigned** via `jira.transition_issue(TC-8011, <assigned-transition-id>)`

The issue is currently in **New** status -- the transition to Assigned will proceed after confirmation.

---

# Step 1 -- Data Extraction

## Parsed CVE Data

| Field | Value |
|-------|-------|
| CVE ID | CVE-2026-45678 |
| Affected component | pscomponent:org/rhtpa-ui |
| Product version (PSIRT-claimed) | [rhtpa-2.2] |
| Affects Versions (Jira field) | RHTPA 2.2.0 |
| Vulnerable library | webpack |
| Affected version range | < 5.98.0 |
| Fixed version | 5.98.0 |
| CVSS | 7.8 (High) |
| Upstream fix PR | N/A |
| Advisory URL | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| CVE record URL | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| Due date | 2026-08-15 |
| Reporter | (PSIRT analyst) |
| Existing comments | None |

## Custom Fields

| Custom Field | Field ID | Value |
|-------------|----------|-------|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** stream in the Version Streams table. Triage is scoped to the 2.2.x stream only.

## Ecosystem Detection

The vulnerable library **webpack** is a JavaScript bundler. Based on the library name and component context, the detected ecosystem is **npm** (JavaScript/TypeScript packages).

The npm ecosystem is classified as a **source dependency** ecosystem per the ecosystem classification table. This means remediation produces **two tasks** per affected stream: an upstream backport task and a downstream propagation subtask with a Blocks dependency.

## Deployment Context Lookup

The affected repository is identified from the component label `pscomponent:org/rhtpa-ui`. Looking up `rhtpa-ui` in the Source Repositories table -- not found. The Source Repositories table does not have a Deployment Context column, so all repositories default to `upstream`.
