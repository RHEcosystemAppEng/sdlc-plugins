# Step 0.7 -- Early Assignment

Before data extraction, assign the CVE issue and transition to Assigned status:

1. **Retrieve current user's Jira account ID**:
   ```
   jira.user_info() -> current user account ID
   ```

2. **Assign TC-8011 to the current user**:
   ```
   jira.edit_issue("TC-8011", assignee=<current-user-account-id>)
   ```

3. **Discover the target transition dynamically**:
   ```
   jira.get_transitions("TC-8011")
   ```
   Select the transition whose target status name is "Assigned".

4. **Transition to Assigned** (issue is currently in New status):
   ```
   jira.transition_issue("TC-8011", <assigned-transition-id>)
   ```

# Step 1 -- Data Extraction

## Parsed CVE Data Table

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-45678 |
| **Affected component** | pscomponent:org/rhtpa-ui |
| **Product version (PSIRT-claimed)** | rhtpa-2.2 (from summary suffix `[rhtpa-2.2]`) |
| **Affects Versions (Jira field)** | RHTPA 2.2.0 |
| **Vulnerable library** | webpack |
| **Affected version range** | < 5.98.0 |
| **Fixed version** | 5.98.0 |
| **CVSS** | 7.8 (High) |
| **Upstream fix PR** | N/A |
| **Advisory URL** | https://github.com/advisories/GHSA-2026-wk55-m3rr |
| **CVE record URL** | https://www.cve.org/CVERecord?id=CVE-2026-45678 |
| **Due date** | 2026-08-15 |
| **Existing comments** | None |
| **Existing issue links** | None |

## Custom Fields

| Custom Field | Field ID | Value |
|---|---|---|
| Upstream Affected Component | customfield_10632 | webpack |
| PS Component | customfield_10669 | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | rhtpa-2.2 |

## Stream Scope Resolution

The issue summary contains stream suffix `[rhtpa-2.2]`, which maps to the **2.2.x** version stream from the Version Streams table. Triage is scoped to the 2.2.x stream.

## Ecosystem Detection

The vulnerable library is **webpack**, which is an npm (JavaScript/TypeScript) package. The ecosystem is detected as **npm** based on the library name and component context.

## Deployment Context Lookup

The affected repository is identified from the component label `pscomponent:org/rhtpa-ui`. The Source Repositories table does not have a Deployment Context column, so the default deployment context is **upstream**.
