# Step 4.3 -- Cross-CVE Overlap Detection

## Upstream Affected Component Extraction

Extracted from **customfield_10632** on TC-8011:

- **Upstream Affected Component**: `webpack`

This value is used to search for related CVE Jiras that affect the same upstream component, regardless of CVE ID.

## JQL Search for Related CVE Jiras

Constructed JQL query:

```
project = TC AND issuetype = 10024 AND cf[10632] ~ 'webpack' AND key != TC-8011
```

**Raw search results**: 1 issue returned.

## Result Filtering

Each result is filtered by matching **PS Component** (customfield_10669) and **Stream** (customfield_10832) to ensure only issues tracking the same component in the same stream are considered:

| Related Issue | CVE ID | PS Component (customfield_10669) | Stream (customfield_10832) | Match? |
|---------------|--------|----------------------------------|---------------------------|--------|
| TC-8012 | CVE-2026-43210 | pscomponent:org/rhtpa-ui | rhtpa-2.2 | YES -- matches current issue (pscomponent:org/rhtpa-ui, rhtpa-2.2) |

**Filtered results**: 1 matching issue (TC-8012).

## Issue Link Traversal on TC-8012

Inspected `issuelinks` on TC-8012 for linked remediation Tasks with link type **Depend**:

| Link Type | Linked Issue | Issue Type | Summary | Status |
|-----------|-------------|------------|---------|--------|
| **Depend** | TC-8013 | Task | Bump webpack to 5.96.1 in rhtpa-ui [rhtpa-2.2] | Closed (Done) |

Found 1 remediation task via the Depend link type.

## Remediation Coverage Comparison

Extracted the target bump version from TC-8013's description:

- **TC-8013 description excerpt**: "Bump webpack from 5.95.0 to **5.96.1** to resolve CVE-2026-43210. The fix requires webpack >= 5.96.0."
- **Bump version (from TC-8013)**: **5.96.1**
- **Current CVE fix threshold (from TC-8011)**: **5.98.0**

Version comparison: **5.96.1 < 5.98.0**

The existing remediation task TC-8013 bumps webpack to 5.96.1, which is **below** the current CVE's fix threshold of 5.98.0. The existing remediation **does NOT cover** this CVE.

## Overlap Analysis Table

```
Related CVE Jiras found for webpack in the same stream (rhtpa-2.2):

| Related CVE | Issue | Remediation Task | Bump Version | Fix Threshold | Covers This CVE? |
|-------------|-------|------------------|--------------|---------------|-------------------|
| CVE-2026-43210 | TC-8012 | TC-8013 | 5.96.1 | 5.98.0 | No (5.96.1 < 5.98.0) |

No existing remediation covers this CVE's fix threshold. Proceeding with
new remediation task creation.
```

## Decision

Since the existing remediation task TC-8013 bumps webpack only to 5.96.1 -- which does not meet the current CVE's fix threshold of 5.98.0 -- the overlap check does **not** short-circuit the triage. New remediation tasks must be created for CVE-2026-45678 to bump webpack to >= 5.98.0.

No traceability links are created in this case because the existing remediation does not cover the current CVE. The Related/Depend link creation from Step 4.3 is only performed when a covering remediation is found.

Proceeding to Step 5 (Version Lifecycle Check) and then Step 8 (Remediation Task Creation).
