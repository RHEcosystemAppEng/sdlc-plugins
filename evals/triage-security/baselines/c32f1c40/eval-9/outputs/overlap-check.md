# Step 4.3 -- Cross-CVE Overlap Detection

## Prerequisites

The following custom fields are configured in Security Configuration and available on the current issue:

- **Upstream Affected Component custom field**: customfield_10632
- **PS Component custom field**: customfield_10669
- **Stream custom field**: customfield_10832

All three fields are configured -- proceeding with cross-CVE overlap detection.

## 1. Extract Upstream Affected Component

Extracted from TC-8011's customfield_10632: **webpack**

The field is populated -- proceeding with overlap search.

## 2. Search for related CVE Jiras

JQL query constructed:

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

Fields requested: `summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832`

**Search results**: 1 result returned.

| Issue | CVE | Summary | Status |
|-------|-----|---------|--------|
| TC-8012 | CVE-2026-43210 | webpack - ReDoS in chunk name validation [rhtpa-2.2] | Closed (Done) |

## 3. Filter by PS Component and Stream

Filtering TC-8012 against the current issue's PS Component and Stream values:

| Field | Current Issue (TC-8011) | Related Issue (TC-8012) | Match? |
|-------|------------------------|------------------------|--------|
| PS Component (customfield_10669) | pscomponent:org/rhtpa-ui | pscomponent:org/rhtpa-ui | YES |
| Stream (customfield_10832) | rhtpa-2.2 | rhtpa-2.2 | YES |

TC-8012 matches on both PS Component and Stream -- it is a relevant related CVE Jira for the same component in the same stream.

## 4. Traverse issue links on TC-8012

Inspecting TC-8012's `issuelinks` array for linked remediation Tasks with link type "Depend":

| Link Type | Linked Issue | Issue Type | Summary | Status |
|-----------|-------------|------------|---------|--------|
| Depend | TC-8013 | Task | Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2] | Closed (Done) |

Found 1 remediation Task linked via "Depend": **TC-8013**

### TC-8013 details

- **Summary**: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
- **Status**: Closed (Done)
- **Description excerpt**: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
- **Bump version extracted from description**: **5.96.1**

## 5. Compare remediation coverage

Comparing the remediation task's bump version against the current CVE's fix threshold:

| Parameter | Value |
|-----------|-------|
| Current CVE (TC-8011) fix threshold | **5.98.0** |
| Existing remediation (TC-8013) bump version | **5.96.1** |
| Comparison | 5.96.1 < 5.98.0 |
| **Verdict** | **NOT COVERED** -- the existing remediation does NOT meet the current CVE's fix threshold |

The existing remediation task TC-8013 bumps webpack to 5.96.1, but CVE-2026-45678 requires webpack >= 5.98.0. The bump falls short of the required fix threshold by a significant margin (5.96.1 vs 5.98.0).

## 6. Findings presented to engineer

Related CVE Jiras found for **webpack** in the same stream (rhtpa-2.2):

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | **No** (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold. Proceeding with new remediation task creation.

The existing remediation task TC-8013 bumps webpack to 5.96.1, which resolves CVE-2026-43210 (fix threshold 5.96.0) but does NOT resolve CVE-2026-45678 (fix threshold 5.98.0). A new remediation task is required to bump webpack to >= 5.98.0.
