# Step 4.3 -- Cross-CVE Overlap Analysis: TC-8011

## Prerequisites Check

The following custom fields are configured in Security Configuration, enabling Step 4.3:

- Upstream Affected Component custom field: customfield_10632
- PS Component custom field: customfield_10669
- Stream custom field: customfield_10832

All three fields are present -- proceeding with cross-CVE overlap detection.

## Upstream Affected Component

The current issue TC-8011 has `customfield_10632` = **webpack**.

## JQL Search for Related CVE Jiras

Query:
```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

### Results

One related CVE Jira found:

| Related CVE | Issue Key | Status | PS Component | Stream |
|---|---|---|---|---|
| CVE-2026-43210 | TC-8012 | Closed (Done) | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

## Filter Validation

TC-8012 matches the current issue on both filtering criteria:
- **PS Component**: `pscomponent:org/rhtpa-ui` -- matches TC-8011
- **Stream**: `rhtpa-2.2` -- matches TC-8011

TC-8012 passes the filter and is relevant for overlap analysis.

## Remediation Task Traversal

TC-8012 has a linked remediation task via "Depend" link type:

| Remediation Task | Summary | Status | Bump Version |
|---|---|---|---|
| TC-8013 | Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2] | Closed (Done) | **5.96.1** |

From the task description: "Bump webpack from 5.95.0 to 5.96.1 to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."

## Coverage Comparison

| Parameter | Value |
|---|---|
| Current CVE (TC-8011) fix threshold | **>= 5.98.0** |
| Existing remediation (TC-8013) bump version | **5.96.1** |
| Coverage? | **NO** |

The existing remediation task TC-8013 bumps webpack to **5.96.1**, which is **below** the current CVE's fix threshold of **5.98.0**.

- 5.96.1 < 5.98.0 -- the existing remediation does **not** cover CVE-2026-45678.

## Overlap Analysis Conclusion

```
Related CVE Jiras found for webpack in the same stream (rhtpa-2.2):

| Related CVE    | Issue   | Remediation Task | Bump Version | Covers This CVE? |
|----------------|---------|------------------|--------------|-------------------|
| CVE-2026-43210 | TC-8012 | TC-8013          | 5.96.1       | No (threshold: 5.98.0) |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

The bump to 5.96.1 resolved CVE-2026-43210 (which required >= 5.96.0) but does NOT resolve CVE-2026-45678 (which requires >= 5.98.0). A new remediation task is required to bump webpack to at least 5.98.0.
