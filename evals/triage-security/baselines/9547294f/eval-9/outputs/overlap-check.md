# Step 4.3 -- Cross-CVE Overlap Detection

## Upstream Affected Component

Extracted from customfield_10632 on TC-8011: **webpack**

## Search for Related CVE Jiras

Constructed JQL query:

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

Fields requested: `summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832`

### Search Results

| Issue | CVE | Status | Upstream Component | PS Component | Stream |
|-------|-----|--------|--------------------|--------------|--------|
| TC-8012 | CVE-2026-43210 | Closed (Done) | webpack | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## Filter by PS Component and Stream

Filtering results to match the current issue's PS Component (`pscomponent:org/rhtpa-ui`) and Stream (`rhtpa-2.2`):

- **TC-8012**: PS Component = `pscomponent:org/rhtpa-ui` (matches), Stream = `rhtpa-2.2` (matches) -- **included**

TC-8012 matches on both PS Component (customfield_10669 = pscomponent:org/rhtpa-ui) and Stream (customfield_10832 = rhtpa-2.2). This issue is relevant for cross-CVE overlap analysis.

## Traverse Issue Links on TC-8012

Inspecting issuelinks on TC-8012 for linked remediation Tasks with link type "Depend":

- **TC-8013** (linked via "Depend" from TC-8012)
  - Summary: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
  - Status: Closed (Done)
  - Description excerpt: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

## Compare Remediation Coverage

| Field | Value |
|-------|-------|
| Remediation Task | TC-8013 |
| Bump Version | 5.96.1 |
| Current CVE Fix Threshold | 5.98.0 |
| Comparison | 5.96.1 < 5.98.0 |
| **Covers This CVE?** | **No** |

The remediation task TC-8013 bumps webpack to **5.96.1**, but the current CVE (CVE-2026-45678) requires webpack >= **5.98.0**. The existing remediation does **not** cover this CVE because 5.96.1 is below the fix threshold of 5.98.0.

## Overlap Summary Table

Related CVE Jiras found for **webpack** in the same stream (rhtpa-2.2):

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | No (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold. **Proceeding with new remediation task creation.**

The existing remediation task TC-8013 (from CVE-2026-43210) bumps webpack to 5.96.1, which resolved its own CVE (fix threshold >= 5.96.0) but falls short of CVE-2026-45678's requirement of >= 5.98.0. A new remediation task must be created to bump webpack to at least 5.98.0.
