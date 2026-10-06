# Step 4.3 -- Cross-CVE Overlap Analysis: TC-8011

## Prerequisite Check

- **Upstream Affected Component custom field** (customfield_10632): Configured -- value is `webpack`
- **PS Component custom field** (customfield_10669): Configured -- value is `pscomponent:org/rhtpa-ui`
- **Stream custom field** (customfield_10832): Configured -- value is `rhtpa-2.2`

All required fields are configured and populated. Proceeding with cross-CVE overlap detection.

## JQL Search for Related CVE Jiras

Query:
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

Fields requested: summary, status, labels, issuelinks, customfield_10632, customfield_10669, customfield_10832

### Results

| Issue | Summary | Status | Labels | Upstream Component | PS Component | Stream |
|-------|---------|--------|--------|--------------------|--------------|--------|
| TC-8012 | CVE-2026-43210 webpack - ReDoS in chunk name validation [rhtpa-2.2] | Closed (Done) | CVE-2026-43210, pscomponent:org/rhtpa-ui | webpack | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## Filtering

TC-8012 matches on all three criteria:
- Same Upstream Affected Component: `webpack` -- MATCH
- Same PS Component: `pscomponent:org/rhtpa-ui` -- MATCH
- Same Stream: `rhtpa-2.2` -- MATCH

TC-8012 passes the filter and is relevant for overlap analysis.

## Remediation Task Traversal

TC-8012 has the following issue links:
- **Depend**: TC-8013 (remediation Task)

### TC-8013 Details

| Field | Value |
|-------|-------|
| **Key** | TC-8013 |
| **Summary** | Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2] |
| **Status** | Closed (Done) |
| **Description excerpt** | "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0." |
| **Bump target version** | 5.96.1 |

## Coverage Comparison

| Parameter | Value |
|-----------|-------|
| **Current CVE fix threshold** | 5.98.0 (from TC-8011 -- CVE-2026-45678) |
| **Existing remediation bump version** | 5.96.1 (from TC-8013, linked to TC-8012 -- CVE-2026-43210) |
| **Comparison** | 5.96.1 < 5.98.0 |
| **Covers this CVE?** | **No** |

The existing remediation task TC-8013 bumps webpack to 5.96.1, which is **below** the current CVE's fix threshold of 5.98.0. The existing remediation does **not** cover CVE-2026-45678.

## Overlap Summary Table

| Related CVE | Issue | Remediation Task | Bump Version | Covers This CVE? |
|-------------|-------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | No (threshold: 5.98.0) |

## Conclusion

Related CVE Jiras found for webpack in the same stream (rhtpa-2.2):

No existing remediation covers this CVE's fix threshold. The bump to 5.96.1 from TC-8013 is insufficient -- CVE-2026-45678 requires webpack >= 5.98.0.

**Proceeding with new remediation task creation.** A new remediation task must be created to bump webpack to at least 5.98.0.
