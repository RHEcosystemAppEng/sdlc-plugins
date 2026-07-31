# Step 4.3 -- Cross-CVE Overlap Detection: TC-8011

## Prerequisite Check

All three required custom fields are configured in Security Configuration:

- Upstream Affected Component custom field: customfield_10632 -- **configured**
- PS Component custom field: customfield_10669 -- **configured**
- Stream custom field: customfield_10832 -- **configured**

Step 4.3 proceeds.

## 1. Extract Upstream Affected Component

Extracted from TC-8011's `customfield_10632`: **webpack**

The Upstream Affected Component field value is used to search for other CVE Jiras
that affect the same upstream library, regardless of CVE ID.

## 2. Search for Related CVE Jiras

JQL query executed:

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

**Results**: 1 issue returned

| Key | Summary | Status | CVE | customfield_10632 | customfield_10669 | customfield_10832 |
|-----|---------|--------|-----|-------------------|-------------------|-------------------|
| TC-8012 | CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2] | Closed (Done) | CVE-2026-43210 | webpack | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## 3. Filter Results by PS Component and Stream

Filtering criteria (from current issue TC-8011):
- PS Component (customfield_10669) must match: `pscomponent:org/rhtpa-ui`
- Stream (customfield_10832) must match: `rhtpa-2.2`

| Key | PS Component Match? | Stream Match? | Included? |
|-----|---------------------|---------------|-----------|
| TC-8012 | pscomponent:org/rhtpa-ui = pscomponent:org/rhtpa-ui -- YES | rhtpa-2.2 = rhtpa-2.2 -- YES | **YES** |

TC-8012 passes both filters and is included in the overlap analysis.

## 4. Traverse Issue Links on TC-8012

Inspecting TC-8012's `issuelinks` array for linked remediation Tasks with link type `Depend`:

| Link Type | Direction | Linked Issue | Summary | Status |
|-----------|-----------|--------------|---------|--------|
| Depend | outward | TC-8013 | Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2] | Closed (Done) |

Found remediation task: **TC-8013**
- Summary: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
- Status: Closed (Done)
- Description excerpt: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
- **Bump version extracted from description**: 5.96.1

## 5. Compare Remediation Coverage

Comparison of the remediation task's bump version against the current CVE's fix threshold:

| Parameter | Value |
|-----------|-------|
| Current CVE fix threshold (CVE-2026-45678) | **5.98.0** |
| Existing remediation bump version (TC-8013) | **5.96.1** |
| Comparison | 5.96.1 < 5.98.0 |
| **Covers this CVE?** | **No** |

The existing remediation task TC-8013 bumps webpack to 5.96.1, which is **below** the
current CVE's fix threshold of 5.98.0. The existing remediation does **not** cover
CVE-2026-45678.

## 6. Overlap Analysis Summary

Related CVE Jiras found for webpack in the same stream (rhtpa-2.2):

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | No (threshold: 5.98.0) |

**Conclusion**: No existing remediation covers this CVE's fix threshold (5.98.0).
Proceeding with new remediation task creation.
