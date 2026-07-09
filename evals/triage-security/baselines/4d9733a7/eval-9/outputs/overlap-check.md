# Step 4.3 -- Cross-CVE Overlap Detection

## Prerequisites

All required custom fields are configured in Security Configuration:
- Upstream Affected Component: customfield_10632
- PS Component: customfield_10669
- Stream: customfield_10832

## 4.3.1 -- Extract Upstream Affected Component

From TC-8011's `customfield_10632`: **webpack**

## 4.3.2 -- Search for Related CVE Jiras

**Proposed JQL query:**

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

Fields requested: summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832

## 4.3.3 -- Filter Results

Search returned one result: **TC-8012**

Filtering by matching PS Component and Stream:
- TC-8012: customfield_10669 = `pscomponent:org/rhtpa-ui` -- **matches** current issue (pscomponent:org/rhtpa-ui)
- TC-8012: customfield_10832 = `rhtpa-2.2` -- **matches** current issue (rhtpa-2.2)

TC-8012 passes both filters.

## 4.3.4 -- Traverse Issue Links

Inspecting TC-8012's issuelinks for remediation Tasks linked via "Depend":

- **TC-8013** (link type: Depend)
  - Summary: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
  - Status: Closed (Done)
  - Description excerpt: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

## 4.3.5 -- Compare Remediation Coverage

| Field | Value |
|-------|-------|
| Remediation task | TC-8013 |
| Library | webpack |
| Bump version (from TC-8013) | 5.96.1 |
| Current CVE fix threshold | 5.98.0 |
| Comparison | 5.96.1 < 5.98.0 |
| **Covers this CVE?** | **No** |

The remediation task TC-8013 bumps webpack to 5.96.1, which is **below** the current CVE's fix threshold of 5.98.0. The existing remediation does **not** cover CVE-2026-45678.

## 4.3.6 -- Findings Presented to Engineer

Related CVE Jiras found for webpack in the same stream (rhtpa-2.2):

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | No (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold. **Proceeding with new remediation task creation.**
