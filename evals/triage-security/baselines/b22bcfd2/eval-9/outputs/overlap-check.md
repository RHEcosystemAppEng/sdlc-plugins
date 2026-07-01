# Step 4.3 -- Cross-CVE Overlap Detection

## Prerequisite Check

The following custom fields are configured and available for cross-CVE overlap detection:

| Custom Field | Configured | Value on TC-8011 |
|-------------|-----------|-----------------|
| Upstream Affected Component (customfield_10632) | Yes | webpack |
| PS Component (customfield_10669) | Yes | pscomponent:org/rhtpa-ui |
| Stream (customfield_10832) | Yes | rhtpa-2.2 |

All prerequisite fields are present. Proceeding with Step 4.3.

## Step 4.3.1 -- Extract Upstream Affected Component

Extracted from TC-8011's `customfield_10632`: **webpack**

## Step 4.3.2 -- Search for Related CVE Jiras

Proposed JQL query:

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

Fields requested: `summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832`

### Search Results

| Issue | Summary | Status | Labels | Upstream Component | PS Component | Stream |
|-------|---------|--------|--------|--------------------|-------------|--------|
| TC-8012 | CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2] | Closed (Done) | CVE-2026-43210, pscomponent:org/rhtpa-ui | webpack | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## Step 4.3.3 -- Filter by PS Component and Stream

Filtering results to match the current issue's PS Component and Stream:

- Current issue PS Component: `pscomponent:org/rhtpa-ui`
- Current issue Stream: `rhtpa-2.2`

| Issue | PS Component Match? | Stream Match? | Included? |
|-------|-------------------|--------------|-----------|
| TC-8012 | Yes (`pscomponent:org/rhtpa-ui` = `pscomponent:org/rhtpa-ui`) | Yes (`rhtpa-2.2` = `rhtpa-2.2`) | Yes |

**TC-8012 passes the filter** -- same PS Component and same Stream as TC-8011.

## Step 4.3.4 -- Traverse Issue Links on TC-8012

Inspecting TC-8012's `issuelinks` array for linked remediation Tasks with link type `Depend`:

| Link Type | Direction | Linked Issue | Issue Type | Status |
|-----------|-----------|-------------|------------|--------|
| Depend | outward | TC-8013 | Task | Closed (Done) |

Found **one** linked remediation Task: **TC-8013**.

### TC-8013 -- Remediation Task Details

- **Summary**: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
- **Status**: Closed (Done)
- **Description excerpt**: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
- **Bump version extracted from description**: **5.96.1**

## Step 4.3.5 -- Compare Remediation Coverage

Comparing TC-8013's bump version against the current CVE's fix threshold:

| Parameter | Value |
|-----------|-------|
| Current CVE (TC-8011) fix threshold | 5.98.0 |
| TC-8013 bump version | 5.96.1 |
| Comparison | 5.96.1 < 5.98.0 |
| **Covers this CVE?** | **No** |

The existing remediation task TC-8013 bumps webpack to **5.96.1**, which is **below** the current CVE's fix threshold of **5.98.0**. The existing remediation does **not** cover CVE-2026-45678.

## Step 4.3.6 -- Overlap Table (Presented to Engineer)

Related CVE Jiras found for **webpack** in the same stream (rhtpa-2.2):

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | **No** (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold (**5.98.0**). Proceeding with new remediation task creation.

**Note**: TC-8013 resolved CVE-2026-43210 by bumping webpack to 5.96.1 (which required >= 5.96.0). However, CVE-2026-45678 requires webpack >= 5.98.0, meaning the previous bump is insufficient. A new remediation task must bump webpack further to at least 5.98.0.
