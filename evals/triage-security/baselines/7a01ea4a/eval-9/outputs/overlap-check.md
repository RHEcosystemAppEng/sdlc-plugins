# Step 4.3 -- Cross-CVE Overlap Analysis: TC-8011

## Prerequisite Check

- Upstream Affected Component field (customfield_10632): **configured** -- value is `webpack`
- PS Component field (customfield_10669): **configured** -- value is `pscomponent:org/rhtpa-ui`
- Stream field (customfield_10832): **configured** -- value is `rhtpa-2.2`

All three fields are present. Step 4.3 proceeds.

## JQL Search for Related CVE Jiras

Query:
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

### Results

| Issue | CVE | Summary | Status | PS Component | Stream |
|-------|-----|---------|--------|--------------|--------|
| TC-8012 | CVE-2026-43210 | webpack - ReDoS in chunk name validation [rhtpa-2.2] | Closed (Done) | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

### Filtering

TC-8012 shares the same PS Component (`pscomponent:org/rhtpa-ui`) and same Stream
(`rhtpa-2.2`) as TC-8011. It is a relevant match for cross-CVE overlap analysis.

## Remediation Task Traversal

TC-8012 has the following issue links:

- **Depend**: TC-8013 (remediation Task)
  - Summary: "Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2]"
  - Status: Closed (Done)
  - Description excerpt: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

**Bump version extracted from TC-8013**: webpack **5.96.1**

## Coverage Comparison

| Field | Value |
|-------|-------|
| Current CVE (TC-8011) fix threshold | **5.98.0** |
| Existing remediation (TC-8013) bump target | **5.96.1** |
| Does TC-8013 cover TC-8011? | **NO** |

**Analysis**: The existing remediation task TC-8013 bumps webpack to 5.96.1, which
is **below** the current CVE's fix threshold of 5.98.0. Version 5.96.1 < 5.98.0,
so the existing remediation does **not** cover CVE-2026-45678.

## Findings Summary

```
Related CVE Jiras found for webpack in the same stream (rhtpa-2.2):

| Related CVE    | Issue   | Remediation Task | Bump Version | Covers This CVE? |
|----------------|---------|------------------|--------------|------------------|
| CVE-2026-43210 | TC-8012 | TC-8013          | 5.96.1       | No (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

## Conclusion

The cross-CVE overlap check found one related CVE Jira (TC-8012) affecting the
same upstream component (webpack) in the same stream (rhtpa-2.2). However, its
remediation task TC-8013 only bumps webpack to 5.96.1, which does **not** meet
the fix threshold of 5.98.0 required by CVE-2026-45678.

A **new remediation task** is required to bump webpack to >= 5.98.0 for stream 2.2.x.
