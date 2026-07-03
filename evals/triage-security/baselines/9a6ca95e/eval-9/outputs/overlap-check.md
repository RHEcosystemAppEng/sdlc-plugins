# Step 4.3 -- Cross-CVE Overlap Analysis: TC-8011

## Prerequisites Check

All required custom fields are present and configured:

- **Upstream Affected Component** (customfield_10632): webpack -- present
- **PS Component** (customfield_10669): pscomponent:org/rhtpa-ui -- present
- **Stream** (customfield_10832): rhtpa-2.2 -- present

Step 4.3 is applicable. Proceeding with cross-CVE overlap detection.

## JQL Search

Search for Vulnerability issues affecting the same upstream component, filtered by matching PS Component and Stream:

```
project = TC AND issuetype = Vulnerability AND cf[10632] ~ "webpack"
```

### Results

| Key | CVE | Summary | Status | PS Component | Stream |
|-----|-----|---------|--------|--------------|--------|
| TC-8012 | CVE-2026-43210 | webpack - ReDoS in chunk name validation [rhtpa-2.2] | Closed (Done) | pscomponent:org/rhtpa-ui | rhtpa-2.2 |

**Match found**: TC-8012 shares the same upstream component (webpack), PS Component (pscomponent:org/rhtpa-ui), and Stream (rhtpa-2.2).

## Remediation Task Traversal

Traversing issue links of TC-8012 to find linked remediation Tasks (link type "Depend"):

| Remediation Task | Summary | Status | Dependency Bump |
|------------------|---------|--------|-----------------|
| TC-8013 | Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2] | Closed (Done) | webpack 5.95.0 -> 5.96.1 |

## Coverage Comparison

| Field | Value |
|-------|-------|
| **Current CVE fix threshold** | >= 5.98.0 |
| **Existing remediation target version** (TC-8013) | 5.96.1 |
| **Covers current CVE?** | **No** -- 5.96.1 < 5.98.0 |

The existing remediation task TC-8013 bumps webpack to 5.96.1, which resolved CVE-2026-43210 (which required >= 5.96.0). However, the current CVE-2026-45678 requires webpack >= 5.98.0. Since 5.96.1 is below the 5.98.0 fix threshold, the existing remediation does **not** cover this CVE.

## Cross-CVE Overlap Summary Table

| Related CVE Jira | CVE ID | Remediation Task | Bump Target | Current Fix Threshold | Covered? |
|-------------------|--------|-------------------|-------------|----------------------|----------|
| TC-8012 | CVE-2026-43210 | TC-8013 (webpack -> 5.96.1) | 5.96.1 | 5.98.0 | **No** |

## Decision

Related CVEs exist for the same upstream component (webpack) in the same stream, but no existing remediation covers the fix threshold for CVE-2026-45678. The existing bump to 5.96.1 falls short of the required 5.98.0.

**Action**: Proceed with new remediation task creation in Step 8. The new task should bump webpack to at least 5.98.0, which will also supersede the previous fix at 5.96.1. A "Related" link should be created between TC-8011 and TC-8012 to document the component overlap.
