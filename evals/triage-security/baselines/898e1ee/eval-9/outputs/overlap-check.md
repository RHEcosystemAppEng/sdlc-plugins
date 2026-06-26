# Step 4.3 -- Cross-CVE Overlap Detection: TC-8011

## Prerequisite Check

The following custom fields are configured in Security Configuration and present on the current issue:

| Custom Field | Field ID | Configured? | Value on TC-8011 |
|---|---|---|---|
| Upstream Affected Component | customfield_10632 | Yes | webpack |
| PS Component | customfield_10669 | Yes | pscomponent:org/rhtpa-ui |
| Stream | customfield_10832 | Yes | rhtpa-2.2 |

All three fields are configured and populated. Step 4.3 proceeds.

## Step 1: Extract Upstream Affected Component

The current issue TC-8011 has `customfield_10632` (Upstream Affected Component) set to **webpack**.

## Step 2: Search for Related CVE Jiras

JQL query executed:

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

**Results**: 1 issue found.

| Issue Key | Summary | Status | CVE ID | customfield_10632 | customfield_10669 | customfield_10832 |
|---|---|---|---|---|---|---|
| TC-8012 | CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2] | Closed (Done) | CVE-2026-43210 | webpack | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## Step 3: Filter by PS Component and Stream

Filtering TC-8012 against the current issue's PS Component and Stream values:

- TC-8011 PS Component: `pscomponent:org/rhtpa-ui` -- TC-8012 PS Component: `pscomponent:org/rhtpa-ui` -- **Match**
- TC-8011 Stream: `rhtpa-2.2` -- TC-8012 Stream: `rhtpa-2.2` -- **Match**

TC-8012 passes the filter. It shares the same upstream component (webpack), same PS Component, and same Stream as TC-8011.

## Step 4: Traverse Issue Links on TC-8012

Inspecting `issuelinks` on TC-8012 for linked remediation Tasks with link type `"Depend"`:

| Link Type | Linked Issue | Issue Type | Summary | Status |
|---|---|---|---|---|
| Depend | TC-8013 | Task (remediation) | Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2] | Closed (Done) |

Found 1 linked remediation Task: **TC-8013**.

## Step 5: Compare Remediation Coverage

Fetched TC-8013 description excerpt:

> "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

**Comparison:**

| Parameter | Value |
|---|---|
| TC-8013 bump target version | 5.96.1 |
| TC-8011 (current CVE) fix threshold | 5.98.0 |
| Does 5.96.1 >= 5.98.0? | **No** |

The remediation task TC-8013 bumps webpack to **5.96.1**, which is **below** the current CVE's fix threshold of **5.98.0**. The existing remediation **does not** cover this CVE.

## Step 6: Findings Summary

Related CVE Jiras found for **webpack** in the same stream (**rhtpa-2.2**) and PS Component (**pscomponent:org/rhtpa-ui**):

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | No (threshold: 5.98.0) |

**No existing remediation covers this CVE's fix threshold.** Proceeding with new remediation task creation in Step 7.

The bump to 5.96.1 (performed for CVE-2026-43210) falls short of the 5.98.0 threshold required to remediate CVE-2026-45678. A new remediation task must be created that bumps webpack to at least 5.98.0.
