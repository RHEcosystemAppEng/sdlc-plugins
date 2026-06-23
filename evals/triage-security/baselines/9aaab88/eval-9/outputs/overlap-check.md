# Step 4.3 -- Cross-CVE Overlap Detection

## Prerequisite Check

All required custom fields are configured in Security Configuration:

| Field | Config Key | Value |
|-------|-----------|-------|
| Upstream Affected Component | customfield_10632 | Configured |
| PS Component | customfield_10669 | Configured |
| Stream | customfield_10832 | Configured |

Proceeding with cross-CVE overlap detection.

## 1. Extract Upstream Affected Component

From TC-8011's `customfield_10632`: **webpack**

Current issue's PS Component (`customfield_10669`): **pscomponent:org/rhtpa-ui**
Current issue's Stream (`customfield_10832`): **rhtpa-2.2**

## 2. Search for Related CVE Jiras

JQL query:
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

Fields requested: `summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832`

### Results

| Key | Summary | Status | CVE | customfield_10632 | customfield_10669 | customfield_10832 |
|-----|---------|--------|-----|-------------------|-------------------|-------------------|
| TC-8012 | CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2] | Closed (Done) | CVE-2026-43210 | webpack | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## 3. Filter by PS Component and Stream

Filtering for matches on:
- PS Component = `pscomponent:org/rhtpa-ui`
- Stream = `rhtpa-2.2`

TC-8012 matches on **both** PS Component and Stream. Proceeding to link traversal.

## 4. Traverse Issue Links

Inspecting TC-8012's `issuelinks` array for linked remediation Tasks with link type "Depend":

- **TC-8013** (link type: Depend)
  - Summary: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
  - Status: Closed (Done)
  - Description excerpt: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

## 5. Compare Remediation Coverage

| Parameter | Value |
|-----------|-------|
| Remediation task | TC-8013 |
| Library bumped | webpack |
| Bump target version | **5.96.1** |
| Current CVE fix threshold | **5.98.0** |
| Comparison | 5.96.1 < 5.98.0 |
| Covers this CVE? | **No** |

The existing remediation task TC-8013 bumps webpack to 5.96.1, which is **below** the current CVE's fix threshold of 5.98.0. The remediation for CVE-2026-43210 does **not** cover CVE-2026-45678.

## 6. Findings

Related CVE Jiras found for **webpack** in the same stream (rhtpa-2.2):

| Related CVE | Issue | Remediation Task | Bump Version | Fix Threshold | Covers This CVE? |
|-------------|-------|------------------|--------------|---------------|-------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | 5.98.0 | **No** (5.96.1 < 5.98.0) |

No existing remediation covers this CVE's fix threshold. Proceeding with new remediation task creation.
