# Step 4.3 — Cross-CVE Overlap Detection

## Upstream Affected Component Extraction

Extracted from **customfield_10632** on TC-8011: `webpack`

## Search for Related CVE Jiras

**JQL query constructed** (not executed — eval mode):
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

**Search results** (from fixture data):

| Related CVE | Issue | Status | PS Component | Stream |
|-------------|-------|--------|--------------|--------|
| CVE-2026-43210 | TC-8012 | Closed (Done) | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## Filtering by PS Component and Stream

- TC-8012 PS Component (`customfield_10669`): `pscomponent:org/rhtpa-ui` — **matches** current issue
- TC-8012 Stream (`customfield_10832`): `rhtpa-2.2` — **matches** current issue

TC-8012 passes the filter — same PS Component and same Stream as TC-8011.

## Traversing Issue Links on TC-8012

TC-8012 has the following issue links:
- **Depend**: TC-8013 (remediation Task)

Fetching TC-8013 details:
- **Summary**: Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]
- **Status**: Closed (Done)
- **Description excerpt**: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

## Remediation Coverage Comparison

Comparing the remediation task's bump version against this CVE's fix threshold:

| Field | Value |
|-------|-------|
| Current CVE fix threshold | 5.98.0 |
| TC-8013 bump version | 5.96.1 |
| Comparison | 5.96.1 < 5.98.0 |
| **Covers this CVE?** | **No** |

The existing remediation task TC-8013 bumps webpack to **5.96.1**, which is **below** the current CVE's fix threshold of **5.98.0**. The existing fix does **NOT** cover CVE-2026-45678.

## Cross-CVE Overlap Table

Related CVE Jiras found for `webpack` in the same stream (rhtpa-2.2):

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | **No** (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold. **Proceeding with new remediation task creation.**
